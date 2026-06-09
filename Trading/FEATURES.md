# Features

## Backlog

### Parked
- **EUR/USD pair expansion** — covered by Step 1/2 architecture; add after Gold + SPX proven
- **USD/JPY pair expansion** — same; JPY safe-haven and BOJ intervention risk as additional characteristics
- **Sections 12–15 encyclopedia** — local added additional encyclopedia sections; review and publish when stable

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

- **Multi-asset pipeline (Step 1)** — `update_prices.py` rewritten with `ASSET` env var support; writes `prices-data-{slug}.js` + `window.PRICES_DATA_{SLUG}` per asset (GBP/USD, XAU/USD, SPY); asset config adds `pip_mult`, `pip_label`, `pip_value`, `decimals`, `slug` fields; backward-compat legacy files still written for GBP/USD; `generate_analysis.py` reads `prices-{slug}.json`, writes `analysis-data-{slug}.js` per asset; both GitHub Actions workflows loop over all 3 assets; placeholder JS files committed so page doesn't 404 before first Action run

- **SPX data fix** — `SPX500USD` invalid on Twelve Data free tier; switched to `SPY` (SPDR S&P 500 ETF, 99.9%+ correlation) as proxy in `update_prices.py`, `generate_analysis.py`, and both GitHub Actions workflow files

- **Dashboard asset selector (Step 2)** — asset selector pills in `index.html` header (GBP/USD · XAU/USD · SPX); `switchAsset()` swaps globals and re-renders all panels; asset-specific characteristics block (session times vs Gold drivers vs SPX earnings); ATR label and chart title dynamic; position calculator uses `pip_value` from data; `buildPrompt` uses `d.symbol` and `d.pip_label`

- **Dashboard widgets (Step 3)** — regime tag (Trending ↑/↓ / Consolidating / Ranging badge from EMA alignment) shown on signal score card; position size calculator widget (account size + risk % + stop distance → position size in units/lots)

- **Economic calendar widget** — `update_calendar.py` new script — Twelve Data `/economic_calendar` endpoint, filters USD/GBP/EUR high-impact events, writes `calendar-data.js`; calendar warning banner for today's events + 7-day events table card on dashboard; both GitHub Actions workflows include calendar step

- **Backtesting script (Step 5)** — `Trading/backtest.py` fetches 730 daily GBP/USD candles, runs all 9 pattern detectors across full history, measures outcomes at 5/10/20 candle horizons, classifies each signal by regime (Trending ↑/↓ / Consolidating / Ranging); outputs `Trading/backtesting.md` with 6-section report (by pattern, by hold period, by regime, pattern×regime matrix, year-by-year, key findings)

- **Shared CSS standardisation** — `styles/site.css` created as single source of truth for header/nav styles; all 3 pages link to it; fixed encyclopedia header bounce (wrong `max-width` + `justify-content:space-between`); standardised `theme-btn` across all pages

- **Encyclopedia search + EMA expansion + collapsible sidebar** — full-width sticky search bar with `/` shortcut, ESC clear, amber highlights, match count; EMA 50/200 section fully expanded for beginners (formula, SMA vs EMA comparison, weight cards, time-context cards, self-fulfilling prophecy); collapsible Books and Momentum sidebar sections with chevron animation; sub-nav items for RSI(14), MACD(12,26,9), EMA 50/200, ATR(14), AVWAP

- **Traders sidebar + Wikipedia links** — `Trading/traders.html` sticky sidebar replaces jump-chip grid with 10 traders grouped by archetype (Quant / Macro / Technical / Value / Trend), colour dots matching card border colours, scroll spy highlights active trader; Wikipedia link on every trader card; Back to top button in sidebar

- **Dual-source economic calendar** — `update_calendar.py` fetches from Forex Factory JSON (primary, no API key, always populated) and Twelve Data (supplementary); events merged and deduplicated by date/currency/title; `nextweek.json` 404 handled gracefully; calendar card now reliably shows events every week

- **Sims multi-agent integration** — `generate_analysis.py` writes `sims/topic-{slug}.txt` after each daily analysis run; one-paragraph debate prompt covering signal score, AI verdict, entry/stop/targets, R/R, indicators, patterns, and invalidation with a challenge question; workflow commits all three files (`sims/topic-gbpusd.txt`, `sims/topic-xauusd.txt`, `sims/topic-spx.txt`) so raw GitHub URLs are always live for the Sims Load button

- **News sentiment feed (Step 4 complete)** — `update_news.py` fetches Alpha Vantage `NEWS_SENTIMENT` for `FOREX:GBPUSD`, `FOREX:XAUUSD`, and `EQUITY:SPY`; 8 latest articles per asset with per-ticker sentiment score, source, timestamp, and summary; writes `news-data.js`; `generate-analysis.yml` runs it daily at 06:10 UTC using `ALPHA_VANTAGE_API_KEY` secret; dashboard shows news card below economic calendar — switches per asset pill, Bullish/Bearish/Neutral badge, clickable headline links; hidden when no data
