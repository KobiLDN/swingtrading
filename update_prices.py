#!/usr/bin/env python3
"""
Multi-Asset Price Updater
Fetches 200 daily candles from Twelve Data, calculates indicators, writes prices-data-{slug}.js

Usage:
    ASSET="GBP/USD"   python update_prices.py
    ASSET="XAU/USD"   python update_prices.py
    ASSET="SPX500USD" python update_prices.py
    python update_prices.py          # defaults to GBP/USD

Requires:
    TWELVE_DATA_API_KEY environment variable (or .env file)
    ASSET environment variable (optional, default GBP/USD)
    pip install pandas numpy requests python-dotenv
"""

import os
import sys
import json
import requests
from datetime import datetime, timezone

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

if sys.stdout.encoding and sys.stdout.encoding.lower() not in ('utf-8', 'utf-8-sig'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

try:
    import pandas as pd
    import numpy as np
except ImportError:
    print("ERROR: pip install pandas numpy requests")
    sys.exit(1)


# ── Asset config ───────────────────────────────────────────────────────────────

ASSET_CONFIG = {
    'GBP/USD': {
        'slug':      'gbpusd',
        'decimals':  5,
        'pip_mult':  10000,   # atr * pip_mult = atr in pips
        'pip_label': 'pips',
        'pip_value': 0.0001,  # USD per unit per pip (quote currency = USD)
    },
    'XAU/USD': {
        'slug':      'xauusd',
        'decimals':  2,
        'pip_mult':  1,       # ATR already in USD/oz
        'pip_label': 'pts',
        'pip_value': 1.0,     # $1 per oz per point
    },
    'SPX500USD': {
        'slug':      'spx',
        'decimals':  2,
        'pip_mult':  1,       # ATR already in index points
        'pip_label': 'pts',
        'pip_value': 1.0,     # $1 per unit per point (micro CFD basis)
    },
    'SPY': {
        'slug':      'spx',
        'decimals':  2,
        'pip_mult':  1,       # ATR already in USD
        'pip_label': 'pts',
        'pip_value': 1.0,     # $1 per share per point
    },
    'WTI/USD': {
        'slug':      'oil',
        'decimals':  2,
        'pip_mult':  1,       # ATR already in USD/barrel
        'pip_label': 'pts',
        'pip_value': 1.0,     # $1 per barrel per point
    },
}

SYMBOL     = os.environ.get('ASSET', 'GBP/USD')
API_KEY    = os.environ.get('TWELVE_DATA_API_KEY', '')
OUTPUTSIZE = 200
INTERVAL   = '1day'

cfg       = ASSET_CONFIG.get(SYMBOL, ASSET_CONFIG['GBP/USD'])
SLUG      = cfg['slug']
DECIMALS  = cfg['decimals']
PIP_MULT  = cfg['pip_mult']
PIP_LABEL = cfg['pip_label']
PIP_VALUE = cfg['pip_value']

OUTPUT_JS   = f'prices-data-{SLUG}.js'
OUTPUT_JSON = f'prices-{SLUG}.json'


# ── Indicators ─────────────────────────────────────────────────────────────────

def calc_ema(series, period):
    return series.ewm(span=period, adjust=False).mean()

def calc_rsi(close, period=14):
    delta    = close.diff()
    gain     = delta.clip(lower=0)
    loss     = (-delta).clip(lower=0)
    avg_gain = gain.ewm(alpha=1/period, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1/period, adjust=False).mean()
    rs = avg_gain / avg_loss.replace(0, np.nan)
    return 100 - (100 / (1 + rs))

def calc_macd(close, fast=12, slow=26, signal=9):
    macd_line   = calc_ema(close, fast) - calc_ema(close, slow)
    signal_line = calc_ema(macd_line, signal)
    return macd_line, signal_line, macd_line - signal_line

def calc_atr(high, low, close, period=14):
    tr = pd.concat([
        high - low,
        (high - close.shift()).abs(),
        (low  - close.shift()).abs(),
    ], axis=1).max(axis=1)
    return tr.ewm(alpha=1/period, adjust=False).mean()

def add_indicators(df):
    df = df.copy()
    df['ema50']       = calc_ema(df['close'], 50)
    df['ema200']      = calc_ema(df['close'], 200)
    df['rsi']         = calc_rsi(df['close'])
    df['macd_line'], df['macd_signal'], df['macd_hist'] = calc_macd(df['close'])
    df['atr']         = calc_atr(df['high'], df['low'], df['close'])
    return df


# ── Pattern detection ──────────────────────────────────────────────────────────

def detect_patterns(df):
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
        is_bearish = not is_bullish
        body_ratio = body / rng

        if body_ratio <= 0.05:
            results.append({'date': date, 'name': 'Doji', 'signal': 'INDECISION', 'strength': 2})
            continue

        if body_ratio <= 0.30 and lower_wick >= 2.2 * body and upper_wick < body and i >= 3:
            down = df['close'].iloc[i-3:i].iloc[-1] < df['close'].iloc[i-3:i].iloc[0]
            name = 'Hammer' if down else 'Hanging Man'
            sig  = 'BULLISH REVERSAL' if down else 'BEARISH REVERSAL'
            results.append({'date': date, 'name': name, 'signal': sig, 'strength': 3})

        elif body_ratio <= 0.30 and upper_wick >= 2.2 * body and lower_wick < body and i >= 3:
            up = df['close'].iloc[i-3:i].iloc[-1] > df['close'].iloc[i-3:i].iloc[0]
            name = 'Shooting Star' if up else 'Inverted Hammer'
            sig  = 'BEARISH REVERSAL' if up else 'BULLISH REVERSAL'
            results.append({'date': date, 'name': name, 'signal': sig, 'strength': 3})

        if i >= 1:
            p = df.iloc[i-1]
            p_top, p_bot = max(p['open'], p['close']), min(p['open'], p['close'])
            c_top, c_bot = max(c['open'], c['close']), min(c['open'], c['close'])
            if is_bullish and p['close'] < p['open'] and c_top > p_top and c_bot < p_bot:
                results.append({'date': date, 'name': 'Bullish Engulfing', 'signal': 'STRONG BULLISH', 'strength': 4})
            if is_bearish and p['close'] > p['open'] and c_top > p_top and c_bot < p_bot:
                results.append({'date': date, 'name': 'Bearish Engulfing', 'signal': 'STRONG BEARISH', 'strength': 4})

        if i >= 2:
            c0, c1, c2 = df.iloc[i-2], df.iloc[i-1], c
            c1r = abs(c1['close'] - c1['open']) / max(c1['high'] - c1['low'], 0.0001)
            mid = (c0['open'] + c0['close']) / 2
            if c0['close'] < c0['open'] and c1r <= 0.35 and c2['close'] > c2['open'] and c2['close'] >= mid:
                results.append({'date': date, 'name': 'Morning Star', 'signal': 'STRONG BULLISH REVERSAL', 'strength': 5})
            if c0['close'] > c0['open'] and c1r <= 0.35 and c2['close'] < c2['open'] and c2['close'] <= mid:
                results.append({'date': date, 'name': 'Evening Star', 'signal': 'STRONG BEARISH REVERSAL', 'strength': 5})

    seen, unique = set(), []
    for r in results:
        key = (r['date'], r['name'])
        if key not in seen:
            seen.add(key)
            unique.append(r)
    return unique

def detect_rsi_divergence(df, lookback=20):
    sub = df.tail(lookback).reset_index(drop=True)
    highs, lows = [], []
    for i in range(1, len(sub) - 1):
        if sub['close'].iloc[i] > sub['close'].iloc[i-1] and sub['close'].iloc[i] > sub['close'].iloc[i+1]:
            highs.append(i)
        if sub['close'].iloc[i] < sub['close'].iloc[i-1] and sub['close'].iloc[i] < sub['close'].iloc[i+1]:
            lows.append(i)
    if len(highs) >= 2:
        h1, h2 = highs[-2], highs[-1]
        if sub['close'].iloc[h2] > sub['close'].iloc[h1] and sub['rsi'].iloc[h2] < sub['rsi'].iloc[h1]:
            return 'BEARISH'
    if len(lows) >= 2:
        l1, l2 = lows[-2], lows[-1]
        if sub['close'].iloc[l2] < sub['close'].iloc[l1] and sub['rsi'].iloc[l2] > sub['rsi'].iloc[l1]:
            return 'BULLISH'
    return 'None'

def score_setup(rsi_val, patterns, divergence, hist_tail):
    score = 0
    if patterns:
        best = max(patterns, key=lambda x: x['strength'])
        score += 4 if best['strength'] >= 4 else 2
    if rsi_val < 30 or rsi_val > 70:
        score += 2
    if divergence != 'None':
        score += 3
    if len(hist_tail) >= 2:
        h_prev, h_last = float(hist_tail.iloc[-2]), float(hist_tail.iloc[-1])
        if h_prev < 0 and h_last > h_prev:
            score += 1
        elif h_prev > 0 and h_last < h_prev:
            score += 1
    score = min(score, 10)
    verdict = 'BUY/SELL' if score >= 8 else 'WATCH' if score >= 5 else 'NO TRADE'
    return score, verdict


# ── Fetch ──────────────────────────────────────────────────────────────────────

def fetch_ohlc():
    if not API_KEY:
        raise ValueError(
            "TWELVE_DATA_API_KEY not set.\n"
            "  Local: create a .env file with TWELVE_DATA_API_KEY=your_key\n"
            "  GitHub Actions: add it as a repository secret"
        )
    url = (
        f"https://api.twelvedata.com/time_series"
        f"?symbol={SYMBOL}&interval={INTERVAL}&outputsize={OUTPUTSIZE}"
        f"&apikey={API_KEY}&format=JSON"
    )
    print(f"Fetching {OUTPUTSIZE} candles for {SYMBOL} ({SLUG}) ...")
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    data = resp.json()

    if data.get('status') == 'error':
        raise ValueError(f"Twelve Data error: {data.get('message', 'unknown')}")

    values = data.get('values', [])
    if not values:
        raise ValueError("No values returned from API")

    df = pd.DataFrame(values)
    df['datetime'] = pd.to_datetime(df['datetime'])
    df[['open','high','low','close']] = df[['open','high','low','close']].astype(float)
    df = df.sort_values('datetime').reset_index(drop=True)
    print(f"  {len(df)} candles  ({df['datetime'].iloc[0].date()} to {df['datetime'].iloc[-1].date()})")
    return df


# ── Write outputs ──────────────────────────────────────────────────────────────

def write_outputs(payload):
    var_name = f'PRICES_DATA_{SLUG.upper()}'

    js = f"window.{var_name} = {json.dumps(payload, indent=2)};\n"
    with open(OUTPUT_JS, 'w', encoding='utf-8') as f:
        f.write(js)
    print(f"  Written: {OUTPUT_JS}  (window.{var_name})")

    with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
        json.dump(payload, f, indent=2)
    print(f"  Written: {OUTPUT_JSON}")

    # Backward compat: GBP/USD also writes the legacy un-suffixed files
    if SLUG == 'gbpusd':
        compat_js = f"window.PRICES_DATA = {json.dumps(payload, indent=2)};\n"
        with open('prices-data.js', 'w', encoding='utf-8') as f:
            f.write(compat_js)
        with open('prices.json', 'w', encoding='utf-8') as f:
            json.dump(payload, f, indent=2)
        print("  Written: prices-data.js + prices.json  (backward compat)")


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    df = fetch_ohlc()

    print("Calculating indicators ...")
    df = add_indicators(df)

    print("Detecting patterns ...")
    patterns = detect_patterns(df)

    print("Checking RSI divergence ...")
    divergence = detect_rsi_divergence(df)

    last  = df.iloc[-1]
    price = float(last['close'])
    e50   = float(last['ema50'])
    e200  = float(last['ema200'])
    rsi_v = float(last['rsi'])
    atr_v = float(last['atr'])

    if price > e50 > e200:     trend = 'STRONG UPTREND'
    elif price < e50 < e200:   trend = 'STRONG DOWNTREND'
    elif e50 > e200:           trend = 'BULLISH BIAS'
    elif e50 < e200:           trend = 'BEARISH BIAS'
    else:                       trend = 'NEUTRAL'

    score, verdict = score_setup(rsi_v, patterns, divergence, df['macd_hist'].tail(3))

    candles = [
        {
            'date':  r['datetime'].strftime('%Y-%m-%d'),
            'open':  round(float(r['open']),  DECIMALS),
            'high':  round(float(r['high']),  DECIMALS),
            'low':   round(float(r['low']),   DECIMALS),
            'close': round(float(r['close']), DECIMALS),
        }
        for _, r in df.tail(100).iterrows()
    ]

    payload = {
        'symbol':      SYMBOL,
        'slug':        SLUG,
        'generated':   datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
        'date':        last['datetime'].strftime('%Y-%m-%d'),
        'price':       round(price, DECIMALS),
        'atr':         round(atr_v, DECIMALS),
        'atr_pips':    round(atr_v * PIP_MULT),
        'pip_label':   PIP_LABEL,
        'pip_mult':    PIP_MULT,
        'pip_value':   PIP_VALUE,
        'decimals':    DECIMALS,
        'ema50':       round(e50,   DECIMALS),
        'ema200':      round(e200,  DECIMALS),
        'rsi':         round(rsi_v, 2),
        'macd_line':   round(float(last['macd_line']),   6),
        'macd_signal': round(float(last['macd_signal']), 6),
        'macd_hist':   round(float(last['macd_hist']),   6),
        'trend':       trend,
        'divergence':  divergence,
        'patterns':    patterns,
        'score':       score,
        'verdict':     verdict,
        'candles':     candles,
    }

    write_outputs(payload)

    print(f"\n  {SYMBOL}  {last['datetime'].strftime('%Y-%m-%d')}")
    print(f"  Price: {price:.{DECIMALS}f}  |  Trend: {trend}")
    print(f"  RSI: {rsi_v:.1f}  |  Score: {score}/10  ->  {verdict}")
    for p in patterns:
        print(f"  Pattern: {p['name']} ({p['signal']})")
    print("\nDone.")


if __name__ == '__main__':
    main()
