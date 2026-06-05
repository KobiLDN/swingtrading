# Agent Guide (Read First)

This file is for any AI or human contributor working in this repo. It describes the entire project so it can be understood or recreated from scratch.

---

## What This Project Is

A **GBP/USD Swing Trading knowledge base and AI-analysis dashboard** — a fully automated pipeline that fetches live price data, calculates technical indicators, calls an AI model for a structured trading decision, and serves the result as a live dashboard on GitHub Pages.

The automated workflow runs every weekday morning:
1. **06:00 UTC** — `update_prices.py` fetches 200 daily OHLC candles from Twelve Data, calculates all indicators, writes `prices-data.js` and `prices.json`
2. **06:10 UTC** — `generate_analysis.py` reads `prices.json`, builds a structured prompt, calls OpenRouter (DeepSeek), parses the AI response, writes `analysis-data.js` and `last_analysis.md`
3. **GitHub Pages** serves `index.html` which loads both JS files and renders the full dashboard

Users can also use the **in-browser OHLC calculator** on the dashboard — paste any OHLC JSON and all indicators recalculate instantly without any API key.

---

## Read Order Before Editing

1. `AGENTS.md` (this file)
2. `CHANGELOG.md` (newest entry is first row under the header)
3. `FEATURES.md` (backlog of planned work)
4. `encyclopedia.md` (the full pattern detection knowledge base)
5. `index.md` (legacy manual dashboard — superseded by `index.html`)

---

## Full Project Structure

```
swingtrading/
├── index.html               ← live dashboard (GitHub Pages)
│                               Lightweight Charts candlestick chart, EMA 50/200,
│                               S/R price lines from AI, RSI bar, MACD, signal score,
│                               9-pattern checklist, AI analysis panel,
│                               in-browser OHLC paste calculator, copy-prompt builder
├── prices-data.js           ← auto-generated daily: window.PRICES_DATA
├── analysis-data.js         ← auto-generated daily: window.ANALYSIS_DATA
├── prices.json              ← raw data backup (input for generate_analysis.py)
├── last_analysis.md         ← latest AI analysis in markdown
├── update_prices.py         ← fetches OHLC + calculates all indicators
├── generate_analysis.py     ← calls OpenRouter, writes analysis output
├── requirements.txt         ← pandas, numpy, requests, python-dotenv
├── .github/workflows/
│   ├── update-prices.yml    ← Mon–Fri 06:00 UTC
│   └── generate-analysis.yml← Mon–Fri 06:10 UTC
└── Trading/                 ← knowledge base (markdown reference)
    ├── AGENTS.md            ← you are here; read first
    ├── CHANGELOG.md         ← all changes, newest first
    ├── FEATURES.md          ← backlog + done
    ├── index.md             ← legacy manual dashboard + prompt template
    ├── encyclopedia.md      ← pattern detection rules (AI's ground truth)
    ├── prompt_template.md   ← 3 prompt variants (quick / full / entry-exit)
    ├── trade_log.md         ← live trade tracking
    ├── ohlc_calculator.py   ← local CLI calculator (no API key needed)
    ├── ohlc_data.json       ← sample OHLC data
    └── run_calculator.bat   ← double-click runner (Windows)
```

---

## File Purposes

### `index.html` — Live Dashboard
The primary interface, served via GitHub Pages. Loads `prices-data.js` and `analysis-data.js` as globals, then renders:
- **Price overview**: current price, ATR(14) in pips, EMA 50/200 tags, trend badge
- **Candlestick chart**: Lightweight Charts v4, last 100 candles, EMA 50 (green) and EMA 200 (red) lines, dashed S/R price lines sourced from the AI analysis
- **RSI(14)**: value, animated progress bar, overbought/oversold/divergence status
- **MACD(12,26,9)**: direction, line values, histogram with colour coding
- **Signal score**: 0–10 circle with BUY/SELL/WATCH/NO TRADE verdict
- **Pattern checklist**: all 9 candlestick patterns listed with ✓/✗ and detection date
- **AI analysis panel**: decision, confidence, entry, SL, targets, R/R, score, analysis text, invalidation level
- **In-browser OHLC calculator**: paste Twelve Data, Alpha Vantage, or plain-array JSON → all indicators recalculate in JS (identical logic to `update_prices.py`) and the chart updates
- **Copy-prompt builder**: pre-filled AI prompt with all current indicators ready to paste into Claude or ChatGPT

### `update_prices.py` — Price + Indicator Updater
Fetches 200 daily candles from Twelve Data, calculates:
- EMA(50), EMA(200) — `ewm(span, adjust=False)`
- RSI(14) — Wilder smoothing `ewm(alpha=1/14, adjust=False)`
- MACD(12,26,9) — standard EWM
- ATR(14) — EWM on true range
- 9 candlestick patterns on the last 5 candles
- RSI divergence over a 20-candle lookback
- 0–10 signal score + verdict (BUY/SELL / WATCH / NO TRADE)
- Trend label (STRONG UPTREND / STRONG DOWNTREND / BULLISH BIAS / BEARISH BIAS / NEUTRAL)

Writes `prices-data.js` (JavaScript global `window.PRICES_DATA`) and `prices.json`.

### `generate_analysis.py` — AI Analysis Generator
Reads `prices.json`, builds a structured prompt with all pre-calculated indicators, calls OpenRouter (DeepSeek v4 Flash, temperature 0.3, max 1500 tokens), parses the response into:
- `DECISION`, `CONFIDENCE`, `ENTRY`, `STOP_LOSS`, `TARGET_1`, `TARGET_2`, `RISK_REWARD`, `SCORE`
- `SUPPORT_LEVELS`, `RESISTANCE_LEVELS` — arrays of prices rendered as dashed lines on the chart
- `ANALYSIS` — 2–4 paragraph reasoning block
- `INVALIDATION` — single sentence cancel condition

Writes `analysis-data.js` (global `window.ANALYSIS_DATA`) and `last_analysis.md`.

### `encyclopedia.md` — Pattern Knowledge Base
The AI's ground truth for consistent analysis. Contains exact detection rules for:
- **9 candlestick patterns** with body/wick ratio thresholds (Hammer, Shooting Star, Engulfing ×2, Morning/Evening Star, Doji, Inverted Hammer, Hanging Man)
- **13 chart patterns** split into reversal (H&S, Double/Triple Top/Bottom) and continuation (triangles, flags, wedges)
- **Support & resistance** detection and breakout confirmation rules
- **RSI** (14-period): overbought/oversold thresholds + divergence detection
- **MACD** (12,26,9): crossover and histogram rules
- **EMA** (50/200): Golden Cross, Death Cross, trend alignment
- **Volume confirmation** rules for breakouts and engulfing candles
- **GBP/USD characteristics**: session volatility, daily range, economic drivers, swing duration
- **Combined signal scoring system** (0-10) with BUY/WATCH/NO TRADE decision matrix
- **Python pseudocode** for Hammer, support detection, and RSI calculation

### `ohlc_calculator.py` — Local CLI Calculator
Standalone script in `Trading/`. Reads `ohlc_data.json` (or a path argument), calculates all indicators, and prints a formatted analysis + pre-filled AI prompt to the console. No API key needed. Identical indicator logic to `update_prices.py`.

---

## Pair & Timeframe Scope

| Item | Value |
|------|-------|
| Instrument | GBP/USD (Cable) |
| Primary timeframe | Daily |
| Secondary timeframe | 4H |
| Typical swing duration | 3-10 days (daily) / 1-3 days (4H) |
| Average daily range | 70-120 pips |
| Key sessions | London-NY overlap 12-16 GMT (best entries) |

---

## Data Sources

| Source | URL | Notes |
|--------|-----|-------|
| Twelve Data | https://twelvedata.com/ | Free tier (800 req/day); primary OHLC source |
| Alpha Vantage | https://www.alphavantage.co/ | Free tier; alternative for OHLC paste |
| OpenRouter | https://openrouter.ai/ | Routes to DeepSeek v4 Flash; ~$0.001/run |
| TradingView | https://www.tradingview.com/symbols/GBPUSD/ | Chart verification only |

---

## Signal Scoring Quick Reference

| Score | Decision |
|-------|----------|
| 8-10 | Strong BUY or SELL — take trade |
| 5-7 | WATCH — wait for confirmation candle |
| 0-4 | NO TRADE — insufficient confluence |

Score breakdown (max 10):
- Chart pattern (+4) or candlestick pattern (+2)
- RSI confirms: overbought/oversold (+2) or divergence (+3)
- MACD histogram turning (+1)
- At key S/R level (+1, via volume in encyclopedia)

---

## Secrets Required (GitHub Actions)

| Secret | Where to get it |
|--------|----------------|
| `TWELVE_DATA_API_KEY` | twelvedata.com — free tier |
| `OPENROUTER_API_KEY` | openrouter.ai — pay-per-use |

---

## Adding Content

### Adding a new candlestick or chart pattern to `encyclopedia.md`
1. Add a row to the relevant table in Section 1 (candlesticks) or Section 2 (chart patterns)
2. Include: Pattern name, Signal bias, Detection rule (precise body/wick/range thresholds), Strength (1-5) or Breakout direction
3. If adding pseudocode, add a function to Section 8
4. Mirror the detection logic in `update_prices.py` → `detect_patterns()` and in `index.html` → `detectPatternsJS()`
5. Add the pattern name to `ALL_PATTERNS` in `index.html` so it appears in the checklist

### Adding a new indicator
1. Implement in `update_prices.py` → `add_indicators()`
2. Add to the `payload` dict in `main()`
3. Mirror the JS equivalent in `index.html`
4. Add to the prompt in `generate_analysis.py` → `build_prompt()`

---

## Future Expansion

See `FEATURES.md` for the full backlog. Planned additions include:
- Additional currency pairs (EUR/USD, USD/JPY)
- Backtesting results doc

---

## Style and Scope

- All detection rules must use precise numeric thresholds (e.g. `body ≤ 30% of range`) — avoid vague language like "small body"
- No hardcoded dates anywhere — everything works with any fresh data
- Update `CHANGELOG.md` whenever a file is meaningfully edited
- Keep Python and JS indicator logic in sync — they must produce identical results
