# Features

## Backlog

### Step 1 — Multi-asset data pipeline
- Add Gold (XAU/USD) and SPX to `update_prices.py` and `generate_analysis.py`
- Create folder structure: `data/forex/gbpusd/`, `data/comod/gold/`, `data/equity/spx/`
- Each folder gets its own `prices-data.js` and `analysis-data.js`
- Update GitHub Actions to run all 3 symbols (separate workflow steps or matrix)

### Step 2 — Dashboard asset selector
- Add dropdown at top of `index.html` (GBP/USD default)
- Dashboard dynamically loads the correct `prices-data.js` and `analysis-data.js` based on selection
- Asset-specific characteristics block swaps in when symbol changes (GBP/USD session times vs Gold drivers vs SPX earnings)

### Step 3 — Dashboard widgets
- **Regime tag** — Trending / Consolidating badge derived from EMA alignment, shown on signal score card
- **Position size calculator** — account size + risk % + stop distance → position size in units/lots

### Step 4 — Economic calendar + news
- Twelve Data `/economic_calendar` endpoint (no new API key) → upcoming high-impact events panel on dashboard
- Alpha Vantage news sentiment for FOREX:GBPUSD (needs `ALPHA_VANTAGE_API_KEY` secret) → headlines feed
- Visual warning flag when high-impact event within 2 days (does not affect score)

### Step 5 — Backtesting script
- Python script replaying 2 years of GBP/USD daily data through all 9 pattern detectors
- Results split by regime (trending vs consolidation) and volatility (ATR > 100 vs < 70 pips)
- Output: `Trading/backtesting.md` with win-rate per pattern per regime

### Parked
- **EUR/USD pair expansion** — covered by Step 1/2 architecture; add after Gold + SPX proven
- **USD/JPY pair expansion** — same; JPY safe-haven and BOJ intervention risk as additional characteristics

---

## Done

- **Initial knowledge base** — `index.md` (GBP/USD swing trading dashboard: OHLC data input template, AI analysis prompt, quick reference card, last analysis placeholder, resource links) + `encyclopedia.md` (full pattern recognition guide: 9 candlestick patterns, 13 chart patterns, S/R detection, RSI/MACD/EMA rules, volume confirmation, GBP/USD characteristics, 0-10 signal scoring system, Python pseudocode for Hammer/support/RSI); content sourced from DeepSeek

- **Python OHLC calculator** — `ohlc_calculator.py`: RSI(14) Wilder smoothing, MACD(12,26,9), EMA(50/200), ATR(14); 9 candlestick pattern detectors; RSI divergence over 20-candle lookback; 0-10 signal score per encyclopedia rules; pre-filled AI prompt block output; supports Twelve Data + Alpha Vantage JSON formats; `ohlc_data.json` sample, `run_calculator.bat` double-click runner

- **Project documentation** — `AGENTS.md` (project purpose, full file structure, workflow, data sources, scoring quick reference, expansion guide) + `CHANGELOG.md` + `FEATURES.md`

- **Prompt templates** — `prompt_template.md` with 3 variants: Quick Scan (1-4 outputs, one-liner verdict), Full Deep Analysis (10 questions + entry/SL/TP/invalidation), Entry/Exit Only (clean numbers only); tips table for best practices

- **Trade log** — `trade_log.md` with Active and Closed trade tables, setup code key, outcome key, monthly summary, and logging rules (only log score ≥5 setups)

- **Automated pipeline** — `update_prices.py` fetches 200 daily OHLC candles from Twelve Data, calculates EMA/RSI/MACD/ATR/patterns/score, writes `prices-data.js` + `prices.json`; `generate_analysis.py` calls OpenRouter (DeepSeek v4 Flash), parses structured BUY/SELL/WAIT decision with S/R levels, writes `analysis-data.js` + `last_analysis.md`; GitHub Actions runs both scripts Mon–Fri at 06:00 and 06:10 UTC

- **Live HTML dashboard** — `index.html` on GitHub Pages: Lightweight Charts candlestick chart with EMA 50/200 lines and AI S/R price lines; RSI bar; MACD panel; 0-10 signal score with breakdown table; 9-pattern checklist with ✓/✗ and signal direction; AI analysis panel (decision, confidence, entry, SL, targets, risk/reward, invalidation); in-browser OHLC paste calculator (full JS port of `update_prices.py` — no API key needed); copy-prompt builder with step-by-step instructions; collapsible "How to use" guide; trend badge with EMA criteria; ATR explained as stop loss sizing guide

- **In-browser OHLC calculator** — full JS port of `update_prices.py` indicator logic embedded in `index.html`; supports Twelve Data, Alpha Vantage, and plain array formats; recalculates all indicators and updates the chart instantly on paste

- **Beginner context layer** — plain-English explanations throughout: RSI/MACD/EMA/ATR definitions in `encyclopedia.md`; score breakdown showing contributing factors; pattern signal direction; confidence sub-labels; R/R explanation; 4-step how-to guide on dashboard

- **Encyclopedia HTML** — full styled HTML version of encyclopedia at `Trading/encyclopedia.html`; fixed left sidebar nav (11 sections, active link scroll spy, smooth scroll); sections 10 (Market Regime) and 11 (Risk Management) added; LAGGING badges on RSI/MACD/EMA; AVWAP sub-section; weekend gap risk in GBP/USD characteristics; recommended reading (12 traders, Market Wizards series, trader archetypes)

- **Encyclopedia expanded (Ariyan's advice)** — VWAP/Anchored VWAP concept; lagging indicator warnings on all momentum indicators; Section 10 Market Regime (trending vs consolidation, regime filter rule, variable isolation for backtesting); Section 11 Risk Management (1–2% rule, position size formula with worked example, R/R minimums, full risk rules table)
