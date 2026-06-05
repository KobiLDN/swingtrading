# GBP/USD Swing Trading Dashboard

**Live site → [KobiLDN.github.io/swingtrading](https://KobiLDN.github.io/swingtrading)**

A GBP/USD swing trading knowledge base and AI-powered analysis dashboard. Daily OHLC data is fetched automatically, all technical indicators are calculated, and DeepSeek AI generates a structured BUY / SELL / WAIT decision — updated every weekday morning.

---

## What it does

- Fetches 200 daily candles from Twelve Data every weekday at 06:00 UTC
- Calculates RSI(14), MACD(12,26,9), EMA(50/200), ATR(14)
- Detects 9 candlestick patterns on the last 5 candles
- Scores the setup 0–10 using confluence rules from the encyclopedia
- Calls OpenRouter (DeepSeek) at 06:10 UTC for a structured AI analysis
- Commits `prices-data.js` + `analysis-data.js` to the repo
- GitHub Pages serves the live dashboard automatically — candlestick chart with EMA lines and AI support/resistance levels, 9-pattern checklist, full AI decision panel

**No setup required to use the calculator** — paste any OHLC JSON directly on the dashboard and all indicators recalculate in-browser instantly.

---

## Project structure

```
swingtrading/
├── index.html               ← live dashboard (GitHub Pages)
├── prices-data.js           ← auto-generated daily by update_prices.py
├── analysis-data.js         ← auto-generated daily by generate_analysis.py
├── prices.json              ← raw data backup
├── last_analysis.md         ← latest AI analysis in markdown
├── update_prices.py         ← fetches OHLC + calculates indicators
├── generate_analysis.py     ← calls OpenRouter, writes analysis output
├── requirements.txt         ← pandas, numpy, requests, python-dotenv
├── .github/workflows/
│   ├── update-prices.yml    ← runs daily Mon–Fri 06:00 UTC
│   └── generate-analysis.yml← runs daily Mon–Fri 06:10 UTC
└── Trading/                 ← knowledge base (markdown reference)
    ├── AGENTS.md            ← full project guide (read first)
    ├── CHANGELOG.md         ← all changes, newest first
    ├── FEATURES.md          ← backlog + done
    ├── index.md             ← manual dashboard + AI prompt template
    ├── encyclopedia.md      ← pattern detection rules (AI's ground truth)
    ├── prompt_template.md   ← 3 prompt variants (quick / full / entry-exit)
    ├── trade_log.md         ← live trade tracking
    ├── ohlc_calculator.py   ← local calculator (no API key needed)
    ├── ohlc_data.json       ← sample OHLC data
    └── run_calculator.bat   ← double-click runner (Windows)
```

---

## Setup (self-hosting)

### 1. Fork the repo and enable GitHub Pages
> Settings → Pages → Source: `main` branch / `/ (root)`

### 2. Add repository secrets
> Settings → Secrets and variables → Actions

| Secret | Where to get it |
|--------|----------------|
| `TWELVE_DATA_API_KEY` | [twelvedata.com](https://twelvedata.com) — free tier (800 req/day) |
| `OPENROUTER_API_KEY` | [openrouter.ai](https://openrouter.ai) — pay-per-use, ~$0.001/run |

### 3. Trigger the first run
> Actions → **Update Prices** → Run workflow
> Actions → **Generate AI Analysis** → Run workflow

After both complete, your dashboard is live with real data.

---

## Local usage (no API key needed)

### Option 1 — Browser (easiest)
Go to the [live dashboard](https://KobiLDN.github.io/swingtrading), scroll to **Live Calculator**, paste your OHLC JSON, and hit **Calculate**. All indicators update instantly. Supports Twelve Data, Alpha Vantage, and plain `[{datetime, open, high, low, close}]` arrays.

### Option 2 — Python CLI
```bash
pip install pandas numpy
cd Trading
python ohlc_calculator.py          # reads ohlc_data.json
# or
python ohlc_calculator.py mydata.json
```
Replace `ohlc_data.json` with fresh data from [Twelve Data](https://twelvedata.com) or [Alpha Vantage](https://www.alphavantage.co/). Outputs a pre-filled AI prompt you can paste directly into Claude or ChatGPT.

---

## Knowledge base

The `Trading/` folder contains the full reference for consistent AI analysis:

- **[encyclopedia.md](Trading/encyclopedia.md)** — exact detection rules for 9 candlestick patterns, 13 chart patterns, RSI/MACD/EMA indicators, volume confirmation, and a 0–10 signal scoring system with Python pseudocode
- **[prompt_template.md](Trading/prompt_template.md)** — 3 ready-to-copy prompts: quick scan, full deep analysis, entry/exit only
- **[trade_log.md](Trading/trade_log.md)** — structured trade tracking with setup codes and monthly summary

---

## Tech stack

| Component | Tool |
|-----------|------|
| Data | [Twelve Data](https://twelvedata.com) free API |
| Indicators | Python (pandas, numpy) — no TA-Lib |
| AI analysis | [OpenRouter](https://openrouter.ai) → DeepSeek |
| Hosting | GitHub Pages (free) |
| Automation | GitHub Actions |

---

## Disclaimer

For research and educational purposes only. Not financial advice.
