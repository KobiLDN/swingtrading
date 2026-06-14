# Kanban

Sessions: **trading/local** (this session) · **trading/cloud** (`claude/friendly-dijkstra-lBUrd`)

---

## Backlog

| Item | Notes | Owner |
|---|---|---|
| EUR/USD pair expansion | Architecture ready (Step 1/2); add after Gold + SPX proven stable | local |
| USD/JPY pair expansion | Same as EUR/USD; add JPY safe-haven + BOJ intervention characteristics | local |
| Encyclopedia sections 12–15 | Written locally; review + publish when stable | local |
| yfinance news fallback | Supplement Alpha Vantage with yfinance + VADER (no API key); use `GC=F`, `GBPUSD=X`, `SPY` tickers in `update_news.py` | cloud |
| Mobile responsive pass | Dashboard at 1440px — needs a proper mobile breakpoint review | local |
| Trade log UI | Surface `trade_log.md` data on dashboard or add a dedicated page | local |

---

## Todo

| Item | Notes | Owner |
|---|---|---|
| News card yfinance fallback | When Alpha Vantage returns no data, fall back to yfinance headlines + VADER sentiment | cloud |
| Encyclopedia publish sections 12–15 | Review locally-written sections, merge into `encyclopedia.html` | local |

---

## In Progress

| Item | Notes | Owner |
|---|---|---|
| — | — | — |

---

## Done (recent)

| Item | Date | Session |
|---|---|---|
| BRANCHES.md + push-all-branches rule | 2026-06-14 | local |
| Traders sidebar scroll fix (`scroll-margin-top`) | 2026-06-14 | local |
| Price Overview 3-col grid (price · asset context · AI verdict mini) | 2026-06-14 | local |
| Candlestick Patterns horizontal flex-wrap + Pattern Guide card | 2026-06-14 | local |
| Inline explainer panels + 1440px + enriched AI prompt (5 sections) | 2026-06-09 | local |
| Dual-source economic calendar (Forex Factory + Twelve Data) | 2026-06-09 | local |
| News sentiment feed — Alpha Vantage Step 4 | 2026-06-09 | cloud |
| Sims multi-agent integration (`sims/topic-{slug}.txt`) | 2026-06-07 | local |
| Shared CSS + traders sidebar + encyclopedia search | 2026-06-06 | local |
| Multi-asset pipeline + calendar + backtesting (Steps 1–5) | 2026-06-06 | local |
