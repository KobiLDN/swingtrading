# Agent Guide (Read First)

This file is for any AI or human contributor working in this repo. It describes the entire project so it can be understood or recreated from scratch.

---

## What This Project Is

A **GBP/USD Swing Trading knowledge base and AI-analysis dashboard** — a set of Markdown files that together form a self-contained reference site for swing trading GBP/USD on the daily and 4H timeframes.

The workflow is:
1. Fetch fresh OHLC data from a free API (Twelve Data or Alpha Vantage)
2. Paste the data + the AI analysis prompt (from `index.md`) into Claude or ChatGPT
3. The AI uses the detection rules in `encyclopedia.md` to identify patterns and output a BUY / SELL / WAIT decision with a risk score

There is no backend, no Python scripts, and no automation pipeline yet. Everything is manual and AI-assisted. The files are designed to be hosted as a static Markdown site (e.g. GitHub Pages, MkDocs, Obsidian Publish) or used directly from a local folder.

---

## Read order before editing

1. `AGENTS.md` (this file)
2. `CHANGELOG.md` (newest entry is first row under the header)
3. `FEATURES.md` (backlog of planned work)
4. `index.md` (the trading dashboard and prompt template)
5. `encyclopedia.md` (the full pattern detection knowledge base)

---

## Project Structure

```
SwingTrading/
└── Trading/
    ├── AGENTS.md          ← you are here; read first
    ├── CHANGELOG.md       ← all changes, newest first
    ├── FEATURES.md        ← backlog + done
    ├── index.md           ← main dashboard: data input, AI prompt, quick reference
    └── encyclopedia.md    ← full pattern knowledge base: candlesticks, chart patterns,
                               S/R, RSI, MACD, EMAs, volume, scoring system, pseudocode
```

---

## File Purposes

### `index.md` — Main Dashboard
- **Data input section**: JSON format example for OHLC paste (symbol, datetime, OHLC fields)
- **AI analysis prompt**: ready-to-copy prompt asking for trend, candlestick patterns, chart patterns, RSI divergence, S/R levels, best setup, and a BUY/SELL/WAIT decision with risk score (1-10)
- **Quick reference card**: key signal combinations in a table (RSI + pattern + level)
- **Last analysis placeholder**: manual section to paste in the AI's latest output
- **Resource links**: links to encyclopedia.md, Twelve Data API, TradingView

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
| Twelve Data | https://twelvedata.com/ | Free tier; JSON endpoint; use for OHLC |
| Alpha Vantage | https://www.alphavantage.co/ | Free tier; alternative |
| TradingView | https://www.tradingview.com/symbols/GBPUSD/ | Chart verification only |

---

## AI Analysis Workflow

1. Open `index.md`
2. Fetch fresh daily OHLC JSON (last 20-50 candles is sufficient)
3. Copy the analysis prompt from `index.md`
4. Paste prompt + JSON data into Claude or ChatGPT
5. Optionally attach `encyclopedia.md` or paste the relevant sections as context
6. Record the AI's decision in the "Last Analysis" section of `index.md`

### Recommended AI prompt attachment

When using Claude: paste the full `encyclopedia.md` content before the OHLC data so the detection rules are in context. This ensures consistent results across sessions.

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
- Volume confirms ≥1.5× 20-day avg (+2)
- At key S/R level (+1)

---

## Adding Content

### Adding a new candlestick or chart pattern to `encyclopedia.md`
1. Add a row to the relevant table in Section 1 (candlesticks) or Section 2 (chart patterns)
2. Include: Pattern name, Signal bias, Detection rule (precise body/wick/range thresholds), Strength (1-5) or Breakout direction
3. If adding pseudocode, add a function to Section 8

### Updating the quick reference card in `index.md`
Edit the table in the "Quick Reference Card" section. Keep entries to signal combinations only (pattern + indicator + level → action).

### Logging a trade analysis
Paste the AI output into the "Last Analysis" section of `index.md` and update the four fields: Current Bias, Best Setup, Recommended Action, Risk Score.

---

## Future Expansion

See `FEATURES.md` for the full backlog. Planned additions include:
- Additional currency pairs (EUR/USD, USD/JPY)
- Python script to auto-calculate RSI/MACD/EMA from OHLC JSON
- HTML dashboard version with live data fetch
- Automated AI analysis via Claude API on a schedule

---

## Style and Scope

- All detection rules must use precise numeric thresholds (e.g. `body ≤ 30% of range`) — avoid vague language like "small body"
- Keep the prompt template in `index.md` concise: 6 questions + decision format
- No hardcoded dates in `index.md` — it should work with any fresh data paste
- Update `CHANGELOG.md` whenever a file is meaningfully edited
