#!/usr/bin/env python3
"""
GBP/USD OHLC Auto-Calculator
Calculates RSI(14), MACD(12,26,9), EMA(50/200), ATR(14)
and detects candlestick patterns from OHLC JSON data.

Usage:
    python ohlc_calculator.py              # reads ohlc_data.json
    python ohlc_calculator.py mydata.json  # reads specified file

Output:
    Prints analysis to console + saves to analysis_output.txt
    The "AI Prompt Ready" block at the bottom is pre-filled — copy and
    append your OHLC JSON, then paste to Claude or ChatGPT.
"""

import json
import sys
import os
from datetime import datetime

if sys.stdout.encoding and sys.stdout.encoding.lower() not in ('utf-8', 'utf-8-sig'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

try:
    import pandas as pd
    import numpy as np
except ImportError:
    print("ERROR: pandas and numpy are required.")
    print("Run:  pip install pandas numpy")
    sys.exit(1)


# ── Data loading ───────────────────────────────────────────────────────────────

def load_ohlc(filepath):
    """Load OHLC JSON in Twelve Data or Alpha Vantage format."""
    with open(filepath, 'r') as f:
        raw = json.load(f)

    # Twelve Data format: { "symbol": "...", "values": [...] }
    if 'values' in raw:
        values = raw['values']
        symbol = raw.get('symbol', 'GBP/USD')

    # Alpha Vantage format: { "Time Series FX (Daily)": { "YYYY-MM-DD": {...} } }
    elif 'Time Series FX (Daily)' in raw:
        ts = raw['Time Series FX (Daily)']
        symbol = 'GBP/USD'
        values = [
            {
                'datetime': date,
                'open':  v['1. open'],
                'high':  v['2. high'],
                'low':   v['3. low'],
                'close': v['4. close'],
            }
            for date, v in ts.items()
        ]

    else:
        raise ValueError(
            "Unrecognised JSON format.\n"
            "Expected Twelve Data  → { 'symbol': ..., 'values': [...] }\n"
            "or Alpha Vantage      → { 'Time Series FX (Daily)': { ... } }"
        )

    df = pd.DataFrame(values)
    df['datetime'] = pd.to_datetime(df['datetime'])
    df[['open', 'high', 'low', 'close']] = df[['open', 'high', 'low', 'close']].astype(float)
    df = df.sort_values('datetime').reset_index(drop=True)
    return df, symbol


# ── Indicators ─────────────────────────────────────────────────────────────────

def calc_ema(series, period):
    return series.ewm(span=period, adjust=False).mean()


def calc_rsi(close, period=14):
    """Wilder's smoothed RSI."""
    delta = close.diff()
    gain  = delta.clip(lower=0)
    loss  = (-delta).clip(lower=0)
    avg_gain = gain.ewm(alpha=1 / period, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1 / period, adjust=False).mean()
    rs = avg_gain / avg_loss.replace(0, np.nan)
    return 100 - (100 / (1 + rs))


def calc_macd(close, fast=12, slow=26, signal=9):
    macd_line   = calc_ema(close, fast) - calc_ema(close, slow)
    signal_line = calc_ema(macd_line, signal)
    histogram   = macd_line - signal_line
    return macd_line, signal_line, histogram


def calc_atr(high, low, close, period=14):
    """Wilder's ATR using True Range."""
    tr = pd.concat([
        high - low,
        (high - close.shift()).abs(),
        (low  - close.shift()).abs(),
    ], axis=1).max(axis=1)
    return tr.ewm(alpha=1 / period, adjust=False).mean()


def add_indicators(df):
    df = df.copy()
    df['ema50']       = calc_ema(df['close'], 50)
    df['ema200']      = calc_ema(df['close'], 200)
    df['rsi']         = calc_rsi(df['close'])
    df['macd_line'], df['macd_signal'], df['macd_hist'] = calc_macd(df['close'])
    df['atr']         = calc_atr(df['high'], df['low'], df['close'])
    return df


# ── Candlestick pattern detection ──────────────────────────────────────────────

def detect_patterns(df):
    """
    Detect patterns on the last 5 candles.
    Returns list of (date_str, pattern_name, signal, strength) tuples.
    Rules match encyclopedia.md Section 1.
    """
    results = []
    n = len(df)

    for i in range(max(0, n - 5), n):
        c    = df.iloc[i]
        date = c['datetime'].strftime('%Y-%m-%d')
        body = abs(c['close'] - c['open'])
        rng  = c['high'] - c['low']
        if rng < 0.0001:
            continue

        upper_wick = c['high'] - max(c['open'], c['close'])
        lower_wick = min(c['open'], c['close']) - c['low']
        is_bullish = c['close'] >= c['open']
        is_bearish = c['close'] <  c['open']
        body_ratio = body / rng

        # Doji — body ≤ 5% of range
        if body_ratio <= 0.05:
            results.append((date, 'Doji', 'INDECISION', 2))
            continue

        # Hammer / Hanging Man — long lower wick
        if body_ratio <= 0.30 and lower_wick >= 2.2 * body and upper_wick < body:
            if i >= 3:
                window = df['close'].iloc[i - 3:i]
                downtrend = window.iloc[-1] < window.iloc[0]
                if downtrend:
                    results.append((date, 'Hammer',      'BULLISH REVERSAL', 3))
                else:
                    results.append((date, 'Hanging Man', 'BEARISH REVERSAL', 3))

        # Shooting Star / Inverted Hammer — long upper wick
        elif body_ratio <= 0.30 and upper_wick >= 2.2 * body and lower_wick < body:
            if i >= 3:
                window = df['close'].iloc[i - 3:i]
                uptrend = window.iloc[-1] > window.iloc[0]
                if uptrend:
                    results.append((date, 'Shooting Star',    'BEARISH REVERSAL', 3))
                else:
                    results.append((date, 'Inverted Hammer',  'BULLISH REVERSAL', 3))

        # Engulfing — requires previous candle
        if i >= 1:
            prev = df.iloc[i - 1]
            p_top = max(prev['open'], prev['close'])
            p_bot = min(prev['open'], prev['close'])
            c_top = max(c['open'],    c['close'])
            c_bot = min(c['open'],    c['close'])

            if is_bullish and prev['close'] < prev['open']:
                if c_top > p_top and c_bot < p_bot:
                    results.append((date, 'Bullish Engulfing', 'STRONG BULLISH', 4))

            if is_bearish and prev['close'] > prev['open']:
                if c_top > p_top and c_bot < p_bot:
                    results.append((date, 'Bearish Engulfing', 'STRONG BEARISH', 4))

        # Morning Star / Evening Star — 3-candle pattern
        if i >= 2:
            c0 = df.iloc[i - 2]
            c1 = df.iloc[i - 1]
            c2 = c

            c1_body = abs(c1['close'] - c1['open'])
            c1_rng  = c1['high'] - c1['low']
            c1_ratio = c1_body / max(c1_rng, 0.0001)
            c0_mid   = (c0['open'] + c0['close']) / 2

            # Morning Star: big bearish → small/doji → big bullish closing ≥ midpoint
            if (c0['close'] < c0['open'] and
                    c1_ratio <= 0.35 and
                    c2['close'] > c2['open'] and
                    c2['close'] >= c0_mid):
                results.append((date, 'Morning Star', 'STRONG BULLISH REVERSAL', 5))

            # Evening Star: big bullish → small/doji → big bearish closing ≤ midpoint
            if (c0['close'] > c0['open'] and
                    c1_ratio <= 0.35 and
                    c2['close'] < c2['open'] and
                    c2['close'] <= c0_mid):
                results.append((date, 'Evening Star', 'STRONG BEARISH REVERSAL', 5))

    # Deduplicate (same date + same pattern)
    seen = set()
    unique = []
    for r in results:
        key = (r[0], r[1])
        if key not in seen:
            seen.add(key)
            unique.append(r)

    return unique


# ── RSI divergence ─────────────────────────────────────────────────────────────

def detect_rsi_divergence(df, lookback=20):
    """Identify bullish or bearish RSI divergence over the last `lookback` candles."""
    sub = df.tail(lookback).reset_index(drop=True)

    highs, lows = [], []
    for i in range(1, len(sub) - 1):
        if sub['close'].iloc[i] > sub['close'].iloc[i-1] and sub['close'].iloc[i] > sub['close'].iloc[i+1]:
            highs.append(i)
        if sub['close'].iloc[i] < sub['close'].iloc[i-1] and sub['close'].iloc[i] < sub['close'].iloc[i+1]:
            lows.append(i)

    if len(highs) >= 2:
        h1, h2 = highs[-2], highs[-1]
        if (sub['close'].iloc[h2] > sub['close'].iloc[h1] and
                sub['rsi'].iloc[h2]   < sub['rsi'].iloc[h1]):
            return 'BEARISH (price higher high, RSI lower high → SELL signal)'

    if len(lows) >= 2:
        l1, l2 = lows[-2], lows[-1]
        if (sub['close'].iloc[l2] < sub['close'].iloc[l1] and
                sub['rsi'].iloc[l2]   > sub['rsi'].iloc[l1]):
            return 'BULLISH (price lower low, RSI higher low → BUY signal)'

    return 'None detected'


# ── Signal scoring ─────────────────────────────────────────────────────────────

def score_setup(rsi_val, patterns, divergence, hist_tail):
    """
    Score the setup 0-10 per encyclopedia.md Section 7.
    Returns (score, [reason strings]).
    """
    score   = 0
    reasons = []

    # Pattern (strongest found)
    if patterns:
        best = max(patterns, key=lambda x: x[3])
        pts  = 4 if best[3] >= 4 else 2
        score += pts
        reasons.append(f"{best[1]} (+{pts})")

    # RSI extreme
    if rsi_val < 30 or rsi_val > 70:
        score += 2
        reasons.append(f"RSI extreme at {rsi_val:.1f} (+2)")

    # RSI divergence
    if divergence != 'None detected':
        score += 3
        reasons.append(f"RSI divergence (+3)")

    # MACD histogram turning (bonus point)
    if len(hist_tail) >= 2:
        h_prev, h_last = hist_tail.iloc[-2], hist_tail.iloc[-1]
        if h_prev < 0 and h_last > h_prev:
            score += 1
            reasons.append("MACD histogram recovering from negative (+1)")
        elif h_prev > 0 and h_last < h_prev:
            score += 1
            reasons.append("MACD histogram declining from positive (+1)")

    score = min(score, 10)

    if score >= 8:
        verdict = 'STRONG BUY/SELL — take trade'
    elif score >= 5:
        verdict = 'WATCH — wait for confirmation candle'
    else:
        verdict = 'NO TRADE — insufficient signals'

    return score, verdict, reasons


# ── Report builder ─────────────────────────────────────────────────────────────

def build_report(df, symbol, patterns, divergence):
    last = df.iloc[-1]
    prev = df.iloc[-2] if len(df) >= 2 else last

    price = last['close']
    e50   = last['ema50']
    e200  = last['ema200']
    rsi_v = last['rsi']
    ml    = last['macd_line']
    ms    = last['macd_signal']
    mh    = last['macd_hist']
    atr_v = last['atr']

    # Trend
    if price > e50 > e200:
        trend = 'STRONG UPTREND  (Price > EMA50 > EMA200)'
    elif price < e50 < e200:
        trend = 'STRONG DOWNTREND  (Price < EMA50 < EMA200)'
    elif e50 > e200:
        trend = 'BULLISH BIAS  (EMA50 > EMA200, Golden Cross alignment)'
    elif e50 < e200:
        trend = 'BEARISH BIAS  (EMA50 < EMA200, Death Cross alignment)'
    else:
        trend = 'NEUTRAL'

    ema_event = ''
    if prev['ema50'] <= prev['ema200'] and e50 > e200:
        ema_event = '  ** FRESH GOLDEN CROSS this candle!'
    elif prev['ema50'] >= prev['ema200'] and e50 < e200:
        ema_event = '  ** FRESH DEATH CROSS this candle!'

    # RSI
    if rsi_v > 70:
        rsi_label = f'OVERBOUGHT ({rsi_v:.1f})'
    elif rsi_v < 30:
        rsi_label = f'OVERSOLD ({rsi_v:.1f})'
    else:
        rsi_label = f'Neutral ({rsi_v:.1f})'

    # MACD
    macd_dir = 'Bullish (line > signal)' if ml > ms else 'Bearish (line < signal)'
    macd_label = f'{macd_dir}  |  Histogram: {mh:+.5f}'

    # Score
    hist_tail = df['macd_hist'].tail(3)
    score, verdict, reasons = score_setup(rsi_v, patterns, divergence, hist_tail)

    # Pattern summary
    pat_names = ', '.join(p[1] for p in patterns) if patterns else 'None'

    W = 60
    DIV = '─' * W

    lines = [
        '=' * W,
        f'  {symbol} ANALYSIS  -  {last["datetime"].strftime("%Y-%m-%d")}',
        '=' * W,
        '',
        f'  Price   {price:.4f}',
        f'  ATR(14) {atr_v:.4f}  ≈ {round(atr_v * 10000):.0f} pips',
        '',
        f'  {DIV}',
        '  TREND',
        f'  {DIV}',
        f'  {trend}{ema_event}',
        f'  EMA 50 :  {e50:.5f}',
        f'  EMA 200:  {e200:.5f}',
        '',
        f'  {DIV}',
        '  MOMENTUM',
        f'  {DIV}',
        f'  RSI(14)   {rsi_label}',
        f'  Divergence  {divergence}',
        f'  MACD      {macd_label}',
        '',
        f'  {DIV}',
        '  CANDLESTICK PATTERNS  (last 5 candles)',
        f'  {DIV}',
    ]

    if patterns:
        for date, name, signal, strength in patterns:
            lines.append(f'  {date}  {name:<22}  {signal}  [{strength}/5]')
    else:
        lines.append('  None detected')

    lines += [
        '',
        f'  {DIV}',
        f'  SIGNAL SCORE  ->  {score}/10  -  {verdict}',
        f'  {DIV}',
    ]
    for r in reasons:
        lines.append(f'    +  {r}')
    if not reasons:
        lines.append('    (no contributing factors)')

    # Pre-filled AI prompt block
    lines += [
        '',
        '=' * W,
        '  AI PROMPT  (copy everything inside the box)',
        '=' * W,
        '',
        '  +' + '-' * (W - 2),
        f'  |Pre-calculated indicators for {symbol}',
        f'  |Date: {last["datetime"].strftime("%Y-%m-%d")}',
        '  |',
        f'  |Price:      {price:.5f}',
        f'  |ATR(14):    {atr_v:.5f} ({round(atr_v * 10000):.0f} pips)',
        f'  |EMA 50:     {e50:.5f}',
        f'  |EMA 200:    {e200:.5f}',
        f'  |Trend:      {trend}',
        f'  |RSI(14):    {rsi_label}',
        f'  |RSI div:    {divergence}',
        f'  |MACD:       {macd_label}',
        f'  |Patterns:   {pat_names}',
        f'  |Score:      {score}/10 — {verdict}',
        '  |',
        '  |Using the encyclopedia detection rules, please also:',
        '  |  1. Identify any chart patterns (triangles, flags, H&S)',
        '  |  2. Mark key support and resistance levels',
        '  |  3. Confirm or revise the signal score',
        '  |  4. Provide: entry zone, stop loss, target',
        '  |  5. Final verdict: BUY / SELL / WAIT',
        '  |',
        '  |[PASTE YOUR OHLC JSON BELOW THIS LINE]',
        '  +' + '-' * (W - 2),
        '',
        '=' * W,
    ]

    return '\n'.join(lines)


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    filepath = sys.argv[1] if len(sys.argv) > 1 else 'ohlc_data.json'

    if not os.path.exists(filepath):
        print(f"\nERROR: '{filepath}' not found.")
        print("  1. Fetch GBP/USD daily data from Twelve Data or Alpha Vantage")
        print("  2. Save as ohlc_data.json in this folder")
        print("  3. Re-run:  python ohlc_calculator.py")
        sys.exit(1)

    print(f"\nLoading {filepath} ...")
    df, symbol = load_ohlc(filepath)
    n = len(df)
    date_range = f"{df['datetime'].iloc[0].date()} to {df['datetime'].iloc[-1].date()}"
    print(f"  {n} candles  ({date_range})")

    if n < 26:
        print("  WARNING: fewer than 26 candles — MACD values will be unreliable.")
    if n < 200:
        print(f"  NOTE: {n} candles loaded — EMA200 fully converges at 200+ candles.")

    print("Calculating indicators ...")
    df = add_indicators(df)

    print("Detecting patterns ...")
    patterns = detect_patterns(df)

    print("Checking RSI divergence ...")
    divergence = detect_rsi_divergence(df)

    report = build_report(df, symbol, patterns, divergence)

    print('\n' + report)

    out_file = 'analysis_output.txt'
    with open(out_file, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"\nSaved → {out_file}\n")


if __name__ == '__main__':
    main()
