# Agent Guide (Read First)

This file is for any AI or human contributor working in this repo. It describes the entire project so it can be understood or recreated from scratch.

---

## What This Project Is

A **live GBP/USD swing trading dashboard** hosted on GitHub Pages, with a fully automated daily data pipeline powered by GitHub Actions, Python, and an OpenRouter AI model.

Every weekday at 06:00 UTC:
1. GitHub Actions fetches 200 daily OHLC candles from Twelve Data API
2. Python calculates all indicators (RSI, MACD, EMA 50/200, ATR) and detects 9 candlestick patterns
3. A structured prompt is sent to DeepSeek via OpenRouter, which returns a BUY/SELL/WAIT decision with entry, SL, targets, R:R, score, and full analysis
4. Results are written as JS data files and committed back to the repo
5. GitHub Pages serves the live dashboard at **https://kobildn.github.io/swingtrading/**

There is also an **in-browser OHLC calculator** on the dashboard for manual analysis without any API key.

---

## Read Order Before Editing

1. `Trading/AGENTS.md` (this file)
2. `Trading/CHANGELOG.md` (newest entry first)
3. `Trading/FEATURES.md` (backlog of planned work, structured in 5 steps)
4. `README.md` (repo root — live site URL, secrets table, setup guide)
5. `index.html` (the live dashboard — main entry point)
6. `update_prices.py` + `generate_analysis.py` (the automation pipeline)
7. `Trading/encyclopedia.md` + `Trading/encyclopedia.html` (pattern knowledge base)

---

## Project Structure

```
SwingTrading/                           ← repo root (GitHub Pages serves from here)
├── index.html                          ← live dashboard (main page)
├── prices-data.js                      ← auto-generated: window.PRICES_DATA = {...}
├── analysis-data.js                    ← auto-generated: window.ANALYSIS_DATA = {...}
├── prices.json                         ← intermediate data file (read by generate_analysis.py)
├── last_analysis.md                    ← human-readable version of latest AI analysis
├── update_prices.py                    ← Step 1: fetches OHLC + calculates indicators
├── generate_analysis.py                ← Step 2: calls OpenRouter AI, writes analysis
├── requirements.txt                    ← Python deps: pandas numpy requests python-dotenv
├── README.md                           ← setup guide, secrets table, live URL
├── .gitignore                          ← ignores .env
├── .github/
│   └── workflows/
│       ├── update-prices.yml           ← GitHub Action: runs update_prices.py Mon-Fri 06:00 UTC
│       └── generate-analysis.yml      ← GitHub Action: runs generate_analysis.py Mon-Fri 06:10 UTC
└── Trading/                            ← knowledge base + local tools
    ├── AGENTS.md                       ← you are here; read first
    ├── CHANGELOG.md                    ← all changes, newest first
    ├── FEATURES.md                     ← backlog + done, in 5 numbered steps
    ├── encyclopedia.md                 ← pattern detection rules (source of truth)
    ├── encyclopedia.html               ← styled HTML version of encyclopedia.md (live at /Trading/encyclopedia.html)
    ├── index.md                        ← original markdown dashboard (pre-HTML era)
    ├── ohlc_calculator.py              ← local calculator: reads ohlc_data.json, no API key needed
    ├── ohlc_data.json                  ← paste raw OHLC data here for local calculator
    ├── analysis_output.txt             ← output from ohlc_calculator.py
    ├── prompt_template.md              ← copy-paste prompt for manual AI analysis
    ├── trade_log.md                    ← manual trade journal
    ├── requirements.txt                ← local pip deps for ohlc_calculator.py
    └── run_calculator.bat              ← Windows batch file to run ohlc_calculator.py
```

---

## File Purposes

### `index.html` — Live Dashboard
Served directly by GitHub Pages. Single-page app with:
- **Candlestick chart** (Lightweight Charts v4.2) with EMA 50/200 lines + AI S/R price lines
- **RSI panel** (bar chart, overbought/oversold bands)
- **MACD panel** (line + signal + histogram)
- **Pattern checklist** — 9 patterns with ✓/✗ detected status
- **Signal score** (0-10) with breakdown by factor
- **AI analysis panel** — decision badge, confidence, entry, SL, T1/T2, R:R, score, full narrative, invalidation level
- **In-browser OHLC calculator** — full JS port of Python logic; paste raw OHLC, runs instantly without any API key
- **Copy-prompt builder** — builds a structured analysis prompt from current data
- **Collapsible how-to guide**
- **Dark/light theme toggle**

Loads `prices-data.js` and `analysis-data.js` as `<script>` tags. All indicator math (RSI, MACD, EMA) is also replicated client-side.

### `prices-data.js` — Price Data (auto-generated)
Written by `update_prices.py`. Format: `window.PRICES_DATA = { candles: [...], indicators: {...}, patterns: [...], score: N, meta: {...} }`. Committed by GitHub Actions.

### `analysis-data.js` — AI Analysis (auto-generated)
Written by `generate_analysis.py`. Format: `window.ANALYSIS_DATA = { decision, confidence, entry, stop_loss, target_1, target_2, risk_reward, score, analysis, invalidation, ... }`. Committed by GitHub Actions.

### `update_prices.py` — Price Fetcher + Indicator Calculator
- Fetches 200 daily candles from Twelve Data (`/time_series` endpoint)
- Calculates: RSI(14) Wilder smoothing, MACD(12,26,9), EMA(50), EMA(200), ATR(14)
- Detects 9 candlestick patterns: Hammer, Inverted Hammer, Shooting Star, Hanging Man, Bullish Engulfing, Bearish Engulfing, Morning Star, Evening Star, Doji
- Detects RSI divergence (20-candle lookback)
- Computes 0–10 signal score
- Writes `prices-data.js` and `prices.json`
- Env var required: `TWELVE_DATA_API_KEY`

### `generate_analysis.py` — AI Analysis Generator
- Reads `prices.json`
- Builds a structured prompt with last 5 candles, all indicators, detected patterns, score
- Calls OpenRouter API → model: `deepseek/deepseek-v4-flash`
- Parses response for: DECISION / CONFIDENCE / ENTRY / STOP_LOSS / TARGET_1 / TARGET_2 / RISK_REWARD / SCORE / ANALYSIS / INVALIDATION
- Writes `analysis-data.js` and `last_analysis.md`
- Env var required: `OPENROUTER_API_KEY`

### GitHub Actions Workflows
Both workflows live in `.github/workflows/` and require `permissions: contents: write` (so the bot can push generated files back).

| Workflow | Schedule | Steps |
|----------|----------|-------|
| `update-prices.yml` | Mon–Fri 06:00 UTC | checkout → setup Python → pip install → run update_prices.py → commit prices-data.js + prices.json |
| `generate-analysis.yml` | Mon–Fri 06:10 UTC | checkout → setup Python → pip install → run generate_analysis.py → commit analysis-data.js + last_analysis.md |

The 10-minute gap ensures `prices.json` exists before `generate_analysis.py` reads it.

### `Trading/ohlc_calculator.py` — Local Calculator
- No API key required
- Reads `Trading/ohlc_data.json` (paste raw OHLC data there)
- Calculates same indicators as `update_prices.py`
- Outputs full analysis + a pre-filled AI prompt to console and `Trading/analysis_output.txt`
- Run via `Trading/run_calculator.bat` on Windows

### `Trading/encyclopedia.html` — Knowledge Base (HTML)
Styled version of `encyclopedia.md`. Fixed left sidebar nav with 11 sections, IntersectionObserver scroll spy, dark/light theme matching dashboard. Sections: Candlestick Patterns, Chart Patterns, S&R, Momentum (RSI/MACD/EMA), Volume, GBP/USD Characteristics, Scoring System, Pseudocode, Books/Reading, Market Regime, Risk Management. Live at: https://kobildn.github.io/swingtrading/Trading/encyclopedia.html

---

## API Keys & Secrets

| Secret name (GitHub) | Used by | Where to get |
|----------------------|---------|--------------|
| `TWELVE_DATA_API_KEY` | `update_prices.py` | https://twelvedata.com/ (free tier) |
| `OPENROUTER_API_KEY` | `generate_analysis.py` | https://openrouter.ai/ |

Both must be set in **GitHub repo → Settings → Secrets and variables → Actions**.
For local development, create a `.env` file in the repo root (already in `.gitignore`):
```
TWELVE_DATA_API_KEY=your_key_here
OPENROUTER_API_KEY=your_key_here
```

---

## Signal Scoring Quick Reference

| Score | Decision |
|-------|----------|
| 8–10 | Strong BUY or SELL — take trade |
| 5–7 | WATCH — wait for confirmation |
| 0–4 | NO TRADE — insufficient confluence |

Score breakdown (max 10):
- Strong chart pattern detected: +4 / candlestick pattern: +2
- RSI overbought/oversold: +2 / RSI divergence: +3
- MACD histogram momentum: +1
- At key S/R level: +1

---

## How to Recreate This Project from Scratch

1. Create a GitHub repo, enable Pages from main branch root
2. Add both API keys as repo secrets (see table above)
3. Copy all files from this repo — the directory structure is exactly as shown above
4. The two GitHub Actions workflows will auto-run each weekday morning
5. On first run, manually trigger both workflows in order (update-prices first, then generate-analysis) to populate the data files
6. Visit `https://<username>.github.io/<repo>/` — the dashboard will show live data

---

## Pair & Timeframe Scope

| Item | Value |
|------|-------|
| Instrument | GBP/USD (Cable) |
| Primary timeframe | Daily |
| Secondary timeframe | 4H |
| Data source | Twelve Data (200 daily candles) |
| AI model | deepseek/deepseek-v4-flash via OpenRouter |
| Typical swing duration | 3–10 days (daily) / 1–3 days (4H) |
| Average daily range | 70–120 pips |

---

## Pending Work

See `Trading/FEATURES.md` for the full backlog. Planned next steps:
- **Step 3**: Regime tag (Trending/Consolidating badge) + position size calculator widget
- **Step 1+2**: Multi-asset pipeline (XAU/USD, SPX) with asset selector dropdown
- **Step 4**: Economic calendar integration (Twelve Data `/economic_calendar` endpoint)
- **Step 5**: Backtesting script — replay 2yr daily data through all 9 pattern detectors

---

## Style Rules

- All pattern detection rules use precise numeric thresholds (`body ≤ 30% of range`) — no vague language
- `prices-data.js` and `analysis-data.js` follow `window.VARIABLE = {...}` pattern (same as STOCKSMain project)
- Update `CHANGELOG.md` whenever any file is meaningfully changed
- Dark/light theme toggle is global — all pages (index.html, encyclopedia.html) must honour it
