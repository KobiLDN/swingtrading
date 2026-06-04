# Features

## Backlog

- ~~**Python OHLC auto-calculator**~~ — done ✓

- **EUR/USD pair expansion** — duplicate `index.md` and `encyclopedia.md` for EUR/USD; adjust GBP/USD-specific characteristics section (session volatility, typical daily range, economic drivers: ECB vs Fed); separate "Last Analysis" log per pair

- **USD/JPY pair expansion** — same as EUR/USD; note JPY safe-haven behaviour and BOJ intervention risk as additional factors in the characteristics section

- **HTML dashboard version** — convert `index.md` into an interactive `index.html`; live OHLC fetch from Twelve Data free API; auto-render the quick reference card as a filterable table; one-click copy of the analysis prompt with the latest data pre-pasted

- **Automated AI analysis via Claude API** — Python script that fetches fresh OHLC, builds the analysis prompt, calls Claude API (claude-sonnet-4-6), and writes the result back to a `last_analysis.md` file; run on a schedule or from a bat file

- ~~**Prompt template variants**~~ — done ✓
- ~~**Trade log**~~ — done ✓

- **Backtesting results** — `backtesting.md` documenting how many times each pattern (Hammer, Engulfing, etc.) at key S/R produced a profitable swing on GBP/USD daily over the past 2 years

---

## Done

- **Initial knowledge base** — `index.md` (GBP/USD swing trading dashboard: OHLC data input template, AI analysis prompt, quick reference card, last analysis placeholder, resource links) + `encyclopedia.md` (full pattern recognition guide: 9 candlestick patterns, 13 chart patterns, S/R detection, RSI/MACD/EMA rules, volume confirmation, GBP/USD characteristics, 0-10 signal scoring system, Python pseudocode for Hammer/support/RSI); content sourced from DeepSeek

- **Python OHLC calculator** — `ohlc_calculator.py`: RSI(14) Wilder smoothing, MACD(12,26,9), EMA(50/200), ATR(14); 9 candlestick pattern detectors (Hammer, Shooting Star, Engulfing ×2, Morning/Evening Star, Doji, Inverted Hammer, Hanging Man); RSI divergence over 20-candle lookback; 0-10 signal score per encyclopedia rules; pre-filled AI prompt block output; supports Twelve Data + Alpha Vantage JSON formats; `ohlc_data.json` sample, `run_calculator.bat` double-click runner

- **Project documentation** — `AGENTS.md` (project purpose, file structure, workflow, data sources, scoring quick reference, expansion guide) + `CHANGELOG.md` + `FEATURES.md`

- **Prompt templates** — `prompt_template.md` with 3 variants: Quick Scan (1-4 outputs, one-liner verdict), Full Deep Analysis (10 questions + entry/SL/TP/invalidation), Entry/Exit Only (clean numbers only); tips table for best practices

- **Trade log** — `trade_log.md` with Active and Closed trade tables, setup code key (HMR/SS/BE/BrE/MS/ES/DT/DB/HS/IHS/BF/BrF/AT/DT/ST/FW/RW), outcome key, monthly summary, and logging rules (only log score ≥5 setups)
