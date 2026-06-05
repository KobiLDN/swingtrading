# Features

## Backlog

- **EUR/USD pair expansion** — duplicate `encyclopedia.md` for EUR/USD; adjust GBP/USD-specific characteristics section (session volatility, typical daily range, economic drivers: ECB vs Fed); add pair selector to `index.html`; separate data fetch and AI analysis per pair

- **USD/JPY pair expansion** — same as EUR/USD; note JPY safe-haven behaviour and BOJ intervention risk as additional factors in the characteristics section

- **Backtesting results** — `backtesting.md` documenting how many times each pattern (Hammer, Engulfing, etc.) at key S/R produced a profitable swing on GBP/USD daily over the past 2 years

---

## Done

- **Initial knowledge base** — `index.md` (GBP/USD swing trading dashboard: OHLC data input template, AI analysis prompt, quick reference card, last analysis placeholder, resource links) + `encyclopedia.md` (full pattern recognition guide: 9 candlestick patterns, 13 chart patterns, S/R detection, RSI/MACD/EMA rules, volume confirmation, GBP/USD characteristics, 0-10 signal scoring system, Python pseudocode for Hammer/support/RSI); content sourced from DeepSeek

- **Python OHLC calculator** — `ohlc_calculator.py`: RSI(14) Wilder smoothing, MACD(12,26,9), EMA(50/200), ATR(14); 9 candlestick pattern detectors; RSI divergence over 20-candle lookback; 0-10 signal score per encyclopedia rules; pre-filled AI prompt block output; supports Twelve Data + Alpha Vantage JSON formats; `ohlc_data.json` sample, `run_calculator.bat` double-click runner

- **Project documentation** — `AGENTS.md` (project purpose, full file structure, workflow, data sources, scoring quick reference, expansion guide) + `CHANGELOG.md` + `FEATURES.md`

- **Prompt templates** — `prompt_template.md` with 3 variants: Quick Scan (1-4 outputs, one-liner verdict), Full Deep Analysis (10 questions + entry/SL/TP/invalidation), Entry/Exit Only (clean numbers only); tips table for best practices

- **Trade log** — `trade_log.md` with Active and Closed trade tables, setup code key, outcome key, monthly summary, and logging rules (only log score ≥5 setups)

- **Automated pipeline** — `update_prices.py` fetches 200 daily OHLC candles from Twelve Data, calculates EMA/RSI/MACD/ATR/patterns/score, writes `prices-data.js` + `prices.json`; `generate_analysis.py` calls OpenRouter (DeepSeek v4 Flash), parses structured BUY/SELL/WAIT decision with S/R levels, writes `analysis-data.js` + `last_analysis.md`; GitHub Actions runs both scripts Mon–Fri at 06:00 and 06:10 UTC

- **Live HTML dashboard** — `index.html` on GitHub Pages: Lightweight Charts candlestick chart with EMA 50/200 lines and AI S/R price lines; RSI bar; MACD panel; 0-10 signal score; 9-pattern checklist with ✓/✗; AI analysis panel (decision, confidence, entry, SL, targets, R/R, invalidation); in-browser OHLC paste calculator (full JS port of `update_prices.py` — no API key needed); copy-prompt builder

- **In-browser OHLC calculator** — full JS port of `update_prices.py` indicator logic embedded in `index.html`; supports Twelve Data, Alpha Vantage, and plain array formats; recalculates all indicators and updates the chart instantly on paste
