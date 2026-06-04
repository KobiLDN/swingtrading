#!/usr/bin/env python3
"""
GBP/USD AI Analysis Generator
Reads prices-data.js, builds a prompt, calls OpenRouter (DeepSeek),
writes analysis-data.js and last_analysis.md.

Usage:
    python generate_analysis.py

Requires:
    OPENROUTER_API_KEY environment variable (or in .env file)
    prices.json must exist (run update_prices.py first)
    pip install requests python-dotenv
"""

import os
import sys
import json
import re
import requests
from datetime import datetime, timezone

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

if sys.stdout.encoding and sys.stdout.encoding.lower() not in ('utf-8', 'utf-8-sig'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')


# ── Config ─────────────────────────────────────────────────────────────────────

API_KEY        = os.environ.get("OPENROUTER_API_KEY", "")
MODEL          = "deepseek/deepseek-v4-flash"
PRICES_JSON    = "prices.json"
OUTPUT_JS      = "analysis-data.js"
OUTPUT_MD      = "last_analysis.md"
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"


# ── Prompt builder ─────────────────────────────────────────────────────────────

def build_prompt(d):
    patterns_str = (
        ', '.join(p['name'] for p in d['patterns'])
        if d['patterns'] else 'None detected'
    )

    rsi_v = d['rsi']
    if rsi_v > 70:
        rsi_label = f"OVERBOUGHT ({rsi_v})"
    elif rsi_v < 30:
        rsi_label = f"OVERSOLD ({rsi_v})"
    else:
        rsi_label = f"Neutral ({rsi_v})"

    macd_dir = "Bullish (line above signal)" if d['macd_line'] > d['macd_signal'] else "Bearish (line below signal)"

    prompt = f"""You are a professional GBP/USD swing trader. Analyse the following pre-calculated technical indicators and provide a structured trading decision.

## Pre-calculated Indicators — {d['symbol']} Daily Chart ({d['date']})

- Price: {d['price']}
- ATR(14): {d['atr']} ({d['atr_pips']} pips)
- EMA 50: {d['ema50']}
- EMA 200: {d['ema200']}
- Trend: {d['trend']}
- RSI(14): {rsi_label}
- RSI Divergence: {d['divergence']}
- MACD(12,26,9): {macd_dir} | Histogram: {d['macd_hist']:+.6f}
- Candlestick patterns (last 5 candles): {patterns_str}
- Signal score: {d['score']}/10

## Your analysis must cover

1. Trend confirmation — does price action confirm the EMA trend?
2. Any additional chart patterns you can infer (triangles, flags, double tops/bottoms)?
3. Key support and resistance levels near current price
4. RSI and MACD confluence — do they agree with the trend?
5. The single best trade setup right now (if any)
6. Risk assessment

## Output format (use exactly these labels)

DECISION: [BUY / SELL / WAIT]
CONFIDENCE: [LOW / MEDIUM / HIGH]
ENTRY: [price or "N/A"]
STOP_LOSS: [price or "N/A"]
TARGET_1: [price or "N/A"]
TARGET_2: [price or "N/A"]
RISK_REWARD: [ratio or "N/A"]
SCORE: [{d['score']}/10 confirmed or revised score/10]
SUPPORT_LEVELS: [up to 3 prices nearest below current price, comma-separated, e.g. 1.3412, 1.3350]
RESISTANCE_LEVELS: [up to 3 prices nearest above current price, comma-separated, e.g. 1.3458, 1.3500]

ANALYSIS:
[2-4 paragraphs of reasoning]

INVALIDATION:
[One sentence — what price action would cancel this setup]"""

    return prompt


# ── Call OpenRouter ─────────────────────────────────────────────────────────────

def call_openrouter(prompt):
    if not API_KEY:
        raise ValueError(
            "OPENROUTER_API_KEY not set.\n"
            "  Local: add OPENROUTER_API_KEY=your_key to .env\n"
            "  GitHub Actions: add it as a repository secret"
        )

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type":  "application/json",
        "HTTP-Referer":  "https://github.com/KobiLDN/swingtrading",
        "X-Title":       "GBP/USD Swing Trading",
    }
    body = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.3,
        "max_tokens":  1500,
    }

    print(f"Calling OpenRouter ({MODEL}) ...")
    resp = requests.post(OPENROUTER_URL, headers=headers, json=body, timeout=120)
    if not resp.ok:
        print(f"  HTTP {resp.status_code}: {resp.text[:500]}")
        resp.raise_for_status()
    data = resp.json()

    if 'error' in data:
        raise ValueError(f"OpenRouter error: {data['error']}")

    return data['choices'][0]['message']['content']


# ── Parse response ─────────────────────────────────────────────────────────────

def parse_response(text):
    def extract(label):
        m = re.search(rf'^{label}:\s*(.+)$', text, re.MULTILINE | re.IGNORECASE)
        return m.group(1).strip() if m else 'N/A'

    analysis_m = re.search(r'ANALYSIS:\s*\n(.*?)(?=\nINVALIDATION:|\Z)', text, re.DOTALL | re.IGNORECASE)
    analysis   = analysis_m.group(1).strip() if analysis_m else text

    invalid_m  = re.search(r'INVALIDATION:\s*\n(.+)', text, re.DOTALL | re.IGNORECASE)
    invalidation = invalid_m.group(1).strip() if invalid_m else 'N/A'

    def parse_levels(label):
        m = re.search(rf'^{label}:\s*(.+)$', text, re.MULTILINE | re.IGNORECASE)
        if not m:
            return []
        raw = m.group(1).strip().strip('[]')
        parts = [p.strip() for p in raw.split(',')]
        levels = []
        for p in parts:
            try:
                levels.append(round(float(p), 5))
            except ValueError:
                pass
        return levels

    return {
        'decision':     extract('DECISION'),
        'confidence':   extract('CONFIDENCE'),
        'entry':        extract('ENTRY'),
        'stop_loss':    extract('STOP_LOSS'),
        'target_1':     extract('TARGET_1'),
        'target_2':     extract('TARGET_2'),
        'risk_reward':  extract('RISK_REWARD'),
        'score':        extract('SCORE'),
        'analysis':          analysis,
        'invalidation':      invalidation,
        'support_levels':    parse_levels('SUPPORT_LEVELS'),
        'resistance_levels': parse_levels('RESISTANCE_LEVELS'),
        'raw':               text,
    }


# ── Write outputs ──────────────────────────────────────────────────────────────

def write_outputs(prices, parsed, generated_at):
    payload = {
        'generated':    generated_at,
        'model':        MODEL,
        'symbol':       prices['symbol'],
        'date':         prices['date'],
        'decision':     parsed['decision'],
        'confidence':   parsed['confidence'],
        'entry':        parsed['entry'],
        'stop_loss':    parsed['stop_loss'],
        'target_1':     parsed['target_1'],
        'target_2':     parsed['target_2'],
        'risk_reward':  parsed['risk_reward'],
        'score':        parsed['score'],
        'analysis':          parsed['analysis'],
        'invalidation':      parsed['invalidation'],
        'support_levels':    parsed['support_levels'],
        'resistance_levels': parsed['resistance_levels'],
    }

    js = f"window.ANALYSIS_DATA = {json.dumps(payload, indent=2)};\n"
    with open(OUTPUT_JS, 'w', encoding='utf-8') as f:
        f.write(js)
    print(f"  Written: {OUTPUT_JS}")

    # Markdown output
    md = f"""# Last AI Analysis — {prices['symbol']}

**Date:** {prices['date']}
**Generated:** {generated_at}
**Model:** {MODEL}

---

## Decision

| Field | Value |
|-------|-------|
| **Decision** | {parsed['decision']} |
| **Confidence** | {parsed['confidence']} |
| **Entry** | {parsed['entry']} |
| **Stop Loss** | {parsed['stop_loss']} |
| **Target 1** | {parsed['target_1']} |
| **Target 2** | {parsed['target_2']} |
| **Risk/Reward** | {parsed['risk_reward']} |
| **Score** | {parsed['score']} |

---

## Analysis

{parsed['analysis']}

---

## Invalidation

{parsed['invalidation']}

---

*Auto-generated by generate_analysis.py via OpenRouter ({MODEL})*
"""
    with open(OUTPUT_MD, 'w', encoding='utf-8') as f:
        f.write(md)
    print(f"  Written: {OUTPUT_MD}")


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    if not os.path.exists(PRICES_JSON):
        print(f"ERROR: {PRICES_JSON} not found. Run update_prices.py first.")
        sys.exit(1)

    with open(PRICES_JSON, 'r', encoding='utf-8') as f:
        prices = json.load(f)

    prompt    = build_prompt(prices)
    raw_text  = call_openrouter(prompt)
    parsed    = parse_response(raw_text)
    generated = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')

    write_outputs(prices, parsed, generated)

    print(f"\n  Decision:    {parsed['decision']}")
    print(f"  Confidence:  {parsed['confidence']}")
    print(f"  Entry:       {parsed['entry']}")
    print(f"  Stop Loss:   {parsed['stop_loss']}")
    print(f"  Target 1:    {parsed['target_1']}")
    print(f"  R/R:         {parsed['risk_reward']}")
    print("\nDone.")


if __name__ == '__main__':
    main()
