#!/usr/bin/env python3
"""
GBP/USD Swing Trading Backtester
Fetches ~2 years of daily data, runs all 9 pattern detectors on the full history,
measures outcomes at 5 / 10 / 20 candle horizons, and writes Trading/backtesting.md.

Usage:
    cd SwingTrading/
    TWELVE_DATA_API_KEY=xxx python Trading/backtest.py

Output:
    Trading/backtesting.md

Requires:
    TWELVE_DATA_API_KEY environment variable (or .env file in repo root)
    pip install pandas numpy requests python-dotenv
"""

import os
import sys
import json
import requests
from datetime import datetime, timezone
from collections import defaultdict

# ── Path setup ────────────────────────────────────────────────────────────────
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)

try:
    from dotenv import load_dotenv
    load_dotenv(os.path.join(ROOT, '.env'))
except ImportError:
    pass

if sys.stdout.encoding and sys.stdout.encoding.lower() not in ('utf-8', 'utf-8-sig'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

try:
    import pandas as pd
    import numpy as np
except ImportError:
    print("ERROR: pip install pandas numpy")
    sys.exit(1)

API_KEY   = os.environ.get('TWELVE_DATA_API_KEY', '')
SYMBOL    = 'GBP/USD'
OUTPUT_MD = os.path.join(HERE, 'backtesting.md')
HOLD_PERIODS = [5, 10, 20]  # candles


# ── Indicators ────────────────────────────────────────────────────────────────

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

def classify_regime(price, ema50, ema200):
    sep = abs(ema50 - ema200) / price * 100
    if sep >= 0.3:
        return 'Trending ↑' if ema50 > ema200 else 'Trending ↓'
    if sep <= 0.10:
        return 'Ranging'
    return 'Consolidating'


# ── Pattern detection (full history) ─────────────────────────────────────────

def detect_all_patterns(df):
    """
    Runs all 9 pattern detectors across the full DataFrame.
    Returns list of dicts: {idx, date, year, name, signal, strength, regime, rsi, atr}
    """
    results = []
    n = len(df)

    for i in range(3, n):
        c = df.iloc[i]
        body = abs(c['close'] - c['open'])
        rng  = c['high'] - c['low']
        if rng < 0.00005:
            continue

        upper_wick = c['high'] - max(c['open'], c['close'])
        lower_wick = min(c['open'], c['close']) - c['low']
        is_bullish = c['close'] >= c['open']
        is_bearish = not is_bullish
        body_ratio = body / rng

        date   = c['datetime'].strftime('%Y-%m-%d')
        year   = c['datetime'].year
        regime = classify_regime(float(c['close']), float(c['ema50']), float(c['ema200']))
        rsi    = float(c['rsi']) if not pd.isna(c['rsi']) else 50.0
        atr    = float(c['atr']) if not pd.isna(c['atr']) else 0.0

        def emit(name, signal, strength):
            results.append({
                'idx':      i,
                'date':     date,
                'year':     year,
                'name':     name,
                'signal':   signal,
                'strength': strength,
                'regime':   regime,
                'rsi':      round(rsi, 1),
                'atr_pips': round(atr * 10000),
            })

        # Doji
        if body_ratio <= 0.05:
            emit('Doji', 'INDECISION', 2)
            continue

        # Hammer / Hanging Man
        if body_ratio <= 0.30 and lower_wick >= 2.2 * body and upper_wick < body:
            down = df['close'].iloc[i-3:i].iloc[-1] < df['close'].iloc[i-3:i].iloc[0]
            if down:
                emit('Hammer',      'BULLISH REVERSAL', 3)
            else:
                emit('Hanging Man', 'BEARISH REVERSAL', 3)

        # Shooting Star / Inverted Hammer
        elif body_ratio <= 0.30 and upper_wick >= 2.2 * body and lower_wick < body:
            up = df['close'].iloc[i-3:i].iloc[-1] > df['close'].iloc[i-3:i].iloc[0]
            if up:
                emit('Shooting Star',    'BEARISH REVERSAL', 3)
            else:
                emit('Inverted Hammer',  'BULLISH REVERSAL', 3)

        # Engulfing (check previous candle)
        if i >= 1:
            p = df.iloc[i-1]
            p_top = max(p['open'], p['close'])
            p_bot = min(p['open'], p['close'])
            c_top = max(c['open'], c['close'])
            c_bot = min(c['open'], c['close'])
            if is_bullish and p['close'] < p['open'] and c_top > p_top and c_bot < p_bot:
                emit('Bullish Engulfing', 'STRONG BULLISH', 4)
            if is_bearish and p['close'] > p['open'] and c_top > p_top and c_bot < p_bot:
                emit('Bearish Engulfing', 'STRONG BEARISH', 4)

        # Morning Star / Evening Star (3-candle)
        if i >= 2:
            c0, c1, c2 = df.iloc[i-2], df.iloc[i-1], c
            c1r = abs(c1['close'] - c1['open']) / max(c1['high'] - c1['low'], 0.0001)
            mid = (c0['open'] + c0['close']) / 2
            if c0['close'] < c0['open'] and c1r <= 0.35 and c2['close'] > c2['open'] and c2['close'] >= mid:
                emit('Morning Star', 'STRONG BULLISH REVERSAL', 5)
            if c0['close'] > c0['open'] and c1r <= 0.35 and c2['close'] < c2['open'] and c2['close'] <= mid:
                emit('Evening Star', 'STRONG BEARISH REVERSAL', 5)

    return results


# ── Outcome measurement ───────────────────────────────────────────────────────

def measure_outcome(df, idx, signal, hold):
    """
    Measure whether price moved in the signal direction after `hold` candles.
    Returns None if not enough future data or signal is INDECISION.
    """
    n = len(df)
    if idx + hold >= n:
        return None

    is_bullish = 'BULLISH' in signal
    is_bearish = 'BEARISH' in signal
    if not (is_bullish or is_bearish):
        return None  # INDECISION — skip

    entry = float(df['close'].iloc[idx])
    exit_ = float(df['close'].iloc[idx + hold])
    pct   = (exit_ - entry) / entry * 100

    win      = (exit_ > entry) if is_bullish else (exit_ < entry)
    dir_move = pct if is_bullish else -pct  # positive = moved in signal direction

    return {'win': win, 'pct': pct, 'dir_move': dir_move}


# ── Stats calculator ──────────────────────────────────────────────────────────

def stats(entries):
    if not entries:
        return {'n': 0, 'win_rate': 0.0, 'avg_win': 0.0, 'avg_loss': 0.0, 'expectancy': 0.0}
    n      = len(entries)
    wins   = [e for e in entries if e['win']]
    losses = [e for e in entries if not e['win']]
    wr     = len(wins) / n * 100
    aw     = sum(e['dir_move'] for e in wins)   / len(wins)   if wins   else 0.0
    al     = sum(e['dir_move'] for e in losses) / len(losses) if losses else 0.0
    exp    = (wr / 100 * aw) + ((1 - wr / 100) * al)
    return {
        'n':          n,
        'win_rate':   round(wr,  1),
        'avg_win':    round(aw,  3),
        'avg_loss':   round(al,  3),
        'expectancy': round(exp, 3),
    }


# ── Fetch 2yr data ────────────────────────────────────────────────────────────

def fetch_ohlc(outputsize=730):
    if not API_KEY:
        raise ValueError("TWELVE_DATA_API_KEY not set.")
    url = (
        f"https://api.twelvedata.com/time_series"
        f"?symbol={SYMBOL}&interval=1day&outputsize={outputsize}"
        f"&apikey={API_KEY}&format=JSON"
    )
    print(f"Fetching {outputsize} candles for {SYMBOL} ...")
    resp = requests.get(url, timeout=60)
    resp.raise_for_status()
    data = resp.json()
    if data.get('status') == 'error':
        raise ValueError(f"Twelve Data: {data.get('message')}")
    values = data.get('values', [])
    if not values:
        raise ValueError("No values returned")
    df = pd.DataFrame(values)
    df['datetime'] = pd.to_datetime(df['datetime'])
    df[['open', 'high', 'low', 'close']] = df[['open', 'high', 'low', 'close']].astype(float)
    df = df.sort_values('datetime').reset_index(drop=True)
    print(f"  {len(df)} candles  ({df['datetime'].iloc[0].date()} to {df['datetime'].iloc[-1].date()})")
    return df


# ── Markdown writer ───────────────────────────────────────────────────────────

def write_markdown(df, all_results_by_hold, hold_periods, generated_at):
    """Write full backtesting.md with results for each hold period."""

    # Use the 5-candle results as the primary view
    primary = all_results_by_hold[hold_periods[0]]

    by_pattern = defaultdict(list)
    by_regime  = defaultdict(list)
    by_year    = defaultdict(list)
    for r in primary:
        by_pattern[r['name']].append(r)
        by_regime[r['regime']].append(r)
        by_year[r['year']].append(r)

    # ── Header ──
    lines = [
        f"# GBP/USD Backtesting Results",
        f"",
        f"> **Auto-generated** by `Trading/backtest.py` — {generated_at[:10]}",
        f"> Data window: **{df['datetime'].iloc[0].date()}** → **{df['datetime'].iloc[-1].date()}** ({len(df)} daily candles, ≈ 2 years)",
        f"> Method: Pattern detected at candle close → outcome measured at 5 / 10 / 20 candles later",
        f"> Total signals (5-candle basis): **{len(primary)}**",
        f"",
        f"---",
        f"",
    ]

    # ── Section 1: by Pattern (primary hold) ──
    lines += [
        f"## 1. Results by Pattern  *(5-candle hold)*",
        f"",
        f"| Pattern | Strength | Signals | Win Rate | Avg Win | Avg Loss | Expectancy |",
        f"|---------|----------|---------|----------|---------|----------|------------|",
    ]

    strength_map = {
        'Doji': 2, 'Hammer': 3, 'Hanging Man': 3, 'Inverted Hammer': 3,
        'Shooting Star': 3, 'Bullish Engulfing': 4, 'Bearish Engulfing': 4,
        'Morning Star': 5, 'Evening Star': 5,
    }

    for name, entries in sorted(by_pattern.items(), key=lambda x: -stats(x[1])['win_rate']):
        s  = stats(entries)
        st = strength_map.get(name, '—')
        lines.append(
            f"| **{name}** | {'★' * st} | {s['n']} | **{s['win_rate']}%** |"
            f" +{s['avg_win']:.3f}% | {s['avg_loss']:.3f}% | {s['expectancy']:.3f}% |"
        )

    lines += [
        f"",
        f"*Win = price moved in the signal direction {hold_periods[0]} candles after the pattern.  "
        f"Avg Win/Loss = directional % move (positive = correct direction).  "
        f"Expectancy = (WinRate × AvgWin) + ((1 - WinRate) × AvgLoss).*",
        f"",
        f"---",
        f"",
    ]

    # ── Section 2: Win Rate by Hold Period ──
    lines += [
        f"## 2. Win Rate by Hold Period",
        f"",
        f"| Pattern | 5 candles | 10 candles | 20 candles |",
        f"|---------|-----------|------------|------------|",
    ]

    all_names = sorted(set(r['name'] for r in primary))
    for name in all_names:
        row = f"| **{name}** |"
        for h in hold_periods:
            entries = [r for r in all_results_by_hold[h] if r['name'] == name]
            s = stats(entries)
            row += f" {s['win_rate']}% ({s['n']}) |"
        lines.append(row)

    lines += ["", "*Format: WinRate% (N signals)*", "", "---", ""]

    # ── Section 3: Results by Regime ──
    lines += [
        f"## 3. Results by Regime  *(5-candle hold)*",
        f"",
        f"| Regime | Signals | Win Rate | Avg Win | Avg Loss | Expectancy |",
        f"|--------|---------|----------|---------|----------|------------|",
    ]

    for regime, entries in sorted(by_regime.items(), key=lambda x: -stats(x[1])['win_rate']):
        s = stats(entries)
        lines.append(
            f"| **{regime}** | {s['n']} | **{s['win_rate']}%** |"
            f" +{s['avg_win']:.3f}% | {s['avg_loss']:.3f}% | {s['expectancy']:.3f}% |"
        )

    lines += ["", "---", ""]

    # ── Section 4: Pattern × Regime Matrix ──
    lines += [
        f"## 4. Pattern × Regime Matrix  *(5-candle win rate)*",
        f"",
    ]

    regimes = sorted(by_regime.keys())
    header  = "| Pattern | " + " | ".join(regimes) + " |"
    sep     = "|---------|" + "|".join(["----------"] * len(regimes)) + "|"
    lines  += [header, sep]

    matrix = defaultdict(lambda: defaultdict(list))
    for r in primary:
        matrix[r['name']][r['regime']].append(r)

    for name in all_names:
        row = f"| **{name}** |"
        for reg in regimes:
            entries = matrix[name][reg]
            if entries:
                s = stats(entries)
                row += f" {s['win_rate']}% ({s['n']}) |"
            else:
                row += " — |"
        lines.append(row)

    lines += ["", "*Format: WinRate% (N signals)*", "", "---", ""]

    # ── Section 5: Year-by-Year ──
    lines += [
        f"## 5. Year-by-Year Summary",
        f"",
        f"| Year | Signals | Win Rate | Best Pattern |",
        f"|------|---------|----------|--------------|",
    ]

    for yr in sorted(by_year.keys()):
        entries = by_year[yr]
        s = stats(entries)
        yr_by_pat = defaultdict(list)
        for r in entries:
            yr_by_pat[r['name']].append(r)
        best = max(yr_by_pat.items(), key=lambda x: stats(x[1])['win_rate'], default=('—', []))
        bs = stats(best[1])
        lines.append(f"| {yr} | {s['n']} | {s['win_rate']}% | {best[0]} ({bs['win_rate']}%) |")

    lines += ["", "---", ""]

    # ── Section 6: Key Findings ──
    all_s = {name: stats(entries) for name, entries in by_pattern.items() if stats(entries)['n'] >= 5}
    best_p  = max(all_s.items(), key=lambda x: x[1]['win_rate'], default=('—', {'win_rate': 0, 'n': 0}))
    worst_p = min(all_s.items(), key=lambda x: x[1]['win_rate'], default=('—', {'win_rate': 0, 'n': 0}))
    best_exp = max(all_s.items(), key=lambda x: x[1]['expectancy'], default=('—', {'expectancy': 0, 'n': 0}))

    reg_s   = {r: stats(e) for r, e in by_regime.items() if stats(e)['n'] >= 5}
    best_r  = max(reg_s.items(), key=lambda x: x[1]['win_rate'], default=('—', {'win_rate': 0}))
    worst_r = min(reg_s.items(), key=lambda x: x[1]['win_rate'], default=('—', {'win_rate': 0}))

    lines += [
        f"## 6. Key Findings",
        f"",
        f"- **Highest win rate:** {best_p[0]} — {best_p[1].get('win_rate', '?')}% "
        f"over {best_p[1].get('n', '?')} signals (5-candle hold)",
        f"- **Lowest win rate:** {worst_p[0]} — {worst_p[1].get('win_rate', '?')}% "
        f"over {worst_p[1].get('n', '?')} signals",
        f"- **Best expectancy:** {best_exp[0]} — {best_exp[1].get('expectancy', '?')}% per trade",
        f"- **Best regime:** {best_r[0]} — {best_r[1].get('win_rate', '?')}% win rate",
        f"- **Worst regime:** {worst_r[0]} — {worst_r[1].get('win_rate', '?')}% win rate",
        f"- **Total signals tested:** {len(primary)} across {len(by_year)} years",
        f"",
        f"---",
        f"",
        f"## Notes",
        f"",
        f"- **No transaction costs** (spread, commission, or swap) applied",
        f"- **No stop-loss or take-profit** — holds for exactly N candles",
        f"- **ATR context** — entries at high-ATR periods are not separately isolated",
        f"- **Doji excluded from win/loss** — INDECISION signals are counted but not scored",
        f"- Patterns can overlap (e.g. Engulfing and Hanging Man on same candle)",
        f"",
        f"*Past performance does not guarantee future results. Educational use only.*",
    ]

    md = '\n'.join(lines) + '\n'
    with open(OUTPUT_MD, 'w', encoding='utf-8') as f:
        f.write(md)
    print(f"\nWritten: {OUTPUT_MD}")


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print(f"GBP/USD Backtester  —  {SYMBOL}")
    print("=" * 60)

    df = fetch_ohlc(outputsize=730)
    df = add_indicators(df)

    print(f"Detecting patterns across {len(df)} candles ...")
    raw = detect_all_patterns(df)
    print(f"  {len(raw)} raw pattern occurrences found")

    # Build results for each hold period
    all_results_by_hold = {}
    for hold in HOLD_PERIODS:
        results = []
        for pat in raw:
            outcome = measure_outcome(df, pat['idx'], pat['signal'], hold)
            if outcome is None:
                continue
            results.append({**pat, **outcome})
        all_results_by_hold[hold] = results
        print(f"  Hold {hold:2d}: {len(results)} signals with measurable outcomes")

    generated_at = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    write_markdown(df, all_results_by_hold, HOLD_PERIODS, generated_at)

    # Console summary
    primary = all_results_by_hold[HOLD_PERIODS[0]]
    by_pattern = defaultdict(list)
    for r in primary:
        by_pattern[r['name']].append(r)

    print(f"\n{'Pattern':<22}  {'N':>4}  {'WinRate':>8}  {'Expect':>8}")
    print("-" * 48)
    for name, entries in sorted(by_pattern.items(), key=lambda x: -stats(x[1])['win_rate']):
        s = stats(entries)
        print(f"  {name:<20}  {s['n']:>4}  {s['win_rate']:>7.1f}%  {s['expectancy']:>+7.3f}%")

    print("\nDone.")


if __name__ == '__main__':
    main()
