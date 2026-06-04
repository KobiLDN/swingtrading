# Changelog

Columns: `Date (BST)`, `AI Name`, `Where` (Desktop / Mobile / Web), `Changed` (short description with primary file(s) in backticks).

All notable changes to this project are documented here — **newest first**.

| Date (BST) | AI Name | Where | Changed |
|---|---|---|---|
| 2026-06-04 | Claude Sonnet 4.6 (Claude Code) | Desktop | Infra: **Python OHLC calculator** — `ohlc_calculator.py` calculates RSI(14) Wilder smoothing, MACD(12,26,9), EMA(50/200), ATR(14); detects 9 candlestick patterns on last 5 candles; RSI divergence check over 20-candle lookback; 0-10 signal scoring per encyclopedia rules; outputs formatted analysis + pre-filled AI prompt block to console and `analysis_output.txt`; supports Twelve Data + Alpha Vantage JSON; `ohlc_data.json` sample data; `run_calculator.bat` double-click runner; `requirements.txt` (`ohlc_calculator.py`, `ohlc_data.json`, `run_calculator.bat`, `requirements.txt`). |
| 2026-06-04 | Claude Sonnet 4.6 (Claude Code) | Desktop | Docs: **prompt_template.md + trade_log.md created** — 3 prompt variants (quick scan, full deep analysis, entry/exit only) with tips table; trade log with active/closed tables, setup key, outcome key, monthly summary, and logging rules (`prompt_template.md`, `trade_log.md`). |
| 2026-06-04 | Claude Sonnet 4.6 (Claude Code) | Desktop | Docs: **AGENTS.md + CHANGELOG.md + FEATURES.md created** — full project documentation added; AGENTS.md covers project purpose, file structure, workflow, scoring system, data sources, and expansion guide; FEATURES.md seeds backlog with Python auto-calculator, EUR/USD pair, HTML dashboard, and Claude API automation (`AGENTS.md`, `CHANGELOG.md`, `FEATURES.md`). |
| 2026-06-04 | Claude Sonnet 4.6 (Claude Code) | Desktop | **Initial knowledge base created** — `index.md` (dashboard: OHLC data input template, AI analysis prompt, quick reference card, last analysis placeholder, resource links) + `encyclopedia.md` (full pattern recognition guide: 9 candlestick patterns, 13 chart patterns, S/R rules, RSI/MACD/EMA indicators, volume confirmation, GBP/USD characteristics, 0-10 scoring system, Python pseudocode); content sourced from DeepSeek (`index.md`, `encyclopedia.md`). |
