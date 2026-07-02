# GBP/USD Swing Trading Dashboard

**Live site → [swingtrading.pages.dev](https://swingtrading.pages.dev)** (Cloudflare Pages, deploys from `main`)

| Environment | URL | Deploys from |
|---|---|---|
| **Live** (Cloudflare) | [swingtrading.pages.dev](https://swingtrading.pages.dev) | `main` |
| **Dev preview** (Cloudflare) | [claude-friendly-dijkstra-lbu.swingtrading.pages.dev](https://claude-friendly-dijkstra-lbu.swingtrading.pages.dev) | `claude/friendly-dijkstra-lBUrd` |
| **Mirror** (GitHub Pages) | [KobiLDN.github.io/swingtrading](https://KobiLDN.github.io/swingtrading) | `main` |

A multi-asset swing trading knowledge base and AI-powered analysis dashboard covering GBP/USD, XAU/USD, SPX (via SPY), and WTI Crude (via USO). Daily OHLC data is fetched automatically, all technical indicators are calculated, and DeepSeek AI generates a structured BUY / SELL / WAIT decision — updated every weekday morning.

---

## What it does

- Fetches 200 daily candles for GBP/USD, XAU/USD, and SPX (SPY) from Twelve Data every weekday at 06:00 UTC
- Fetches the economic calendar from **Forex Factory** (primary) + Twelve Data (supplementary), merged and deduplicated
- Calculates RSI(14), MACD(12,26,9), EMA(50/200), ATR(14) per asset
- Detects 9 candlestick patterns on the last 5 candles
- Scores the setup 0–10 using confluence rules from the encyclopedia
- Calls OpenRouter (DeepSeek) at 06:10 UTC for a structured AI analysis per asset
- Commits `prices-data-{slug}.js` + `analysis-data-{slug}.js` + `sims/topic-{slug}.txt` to the repo
- GitHub Pages serves the live dashboard automatically
- `sims/topic-{slug}.txt` provides a ready-made debate prompt for the Sims multi-agent model

---

## Project structure

```
swingtrading/
├── index.html                    ← live dashboard (GitHub Pages)
├── styles/
│   └── site.css                  ← shared header/nav CSS (all pages link here)
├── prices-data-gbpusd.js         ← auto-generated daily
├── prices-data-xauusd.js         ← auto-generated daily
├── prices-data-spx.js            ← auto-generated daily (SPY as SPX proxy)
├── analysis-data-gbpusd.js       ← auto-generated daily
├── analysis-data-xauusd.js       ← auto-generated daily
├── analysis-data-spx.js          ← auto-generated daily
├── last_analysis.md              ← latest AI analysis in markdown
├── sims/
│   ├── topic-gbpusd.txt          ← auto-generated debate prompt (GBP/USD)
│   ├── topic-xauusd.txt          ← auto-generated debate prompt (XAU/USD)
│   └── topic-spx.txt             ← auto-generated debate prompt (SPX)
├── update_prices.py              ← fetches OHLC + calculates indicators
├── generate_analysis.py          ← calls OpenRouter, writes analysis + sims topic
├── requirements.txt              ← pandas, numpy, requests, python-dotenv
├── .github/workflows/
│   ├── update-prices.yml         ← runs daily Mon–Fri 06:00 UTC
│   └── generate-analysis.yml     ← runs daily Mon–Fri 06:10 UTC
└── Trading/                      ← knowledge base + HTML pages
    ├── encyclopedia.html         ← pattern recognition guide (live HTML)
    ├── traders.html              ← 10 legendary trader profiles (live HTML)
    ├── AGENTS.md                 ← full project guide (read first)
    ├── CHANGELOG.md              ← all changes, newest first
    ├── FEATURES.md               ← backlog + done
    ├── index.md                  ← manual dashboard + AI prompt template
    ├── encyclopedia.md           ← pattern detection rules (source of truth)
    ├── prompt_template.md        ← 3 prompt variants (quick / full / entry-exit)
    ├── trade_log.md              ← live trade tracking
    ├── ohlc_calculator.py        ← local calculator (no API key needed)
    ├── ohlc_data.json            ← sample OHLC data
    └── run_calculator.bat        ← double-click runner (Windows)
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

```bash
pip install pandas numpy
cd Trading
python ohlc_calculator.py          # reads ohlc_data.json
# or
python ohlc_calculator.py mydata.json
```

Replace `ohlc_data.json` with fresh data from [Twelve Data](https://twelvedata.com) or [Alpha Vantage](https://www.alphavantage.co/). The calculator outputs a pre-filled AI prompt you can paste directly into Claude or ChatGPT.

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
