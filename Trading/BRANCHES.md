# Branches

## ⛔ STRICT RULES — read before any push

1. **All work MUST go to the dev branch (`claude/friendly-dijkstra-lBUrd`) first.** No exceptions. Test it on the Cloudflare dev preview before it goes anywhere near live.
2. **NEVER push to `main` (live) without asking Kobi for permission first.** Every push to main = instant live deploy on Cloudflare + GitHub Pages. Ask, wait for a yes, then push.

The only exception: the GitHub Actions bots (price/analysis/news updates) push generated data files to `main` automatically — that is expected and allowed.

## Workflow

```bash
# 1. Develop + commit on the dev branch
git push -u origin claude/friendly-dijkstra-lBUrd

# 2. Check it on the dev preview URL:
#    https://claude-friendly-dijkstra-lbu.swingtrading.pages.dev

# 3. ASK KOBI: "ready to push to live?"

# 4. Only after a yes:
git push origin claude/friendly-dijkstra-lBUrd:main
```

---

## Branch table

| Branch | Session | Deploys to | Push policy |
|---|---|---|---|
| `main` | trading/local | **LIVE** — [swingtrading.pages.dev](https://swingtrading.pages.dev) + GitHub Pages | ⛔ permission required |
| `claude/friendly-dijkstra-lBUrd` | trading/cloud | Dev preview — [claude-friendly-dijkstra-lbu.swingtrading.pages.dev](https://claude-friendly-dijkstra-lbu.swingtrading.pages.dev) | ✅ push freely |

---

## Notes

- Only one local folder: `G:\My Drive\coding\ai\Trading\SwingTrading` — always on `main`
- Cloudflare Pages deploys every branch automatically: `main` → production, any other branch → its own preview URL
- After a live push is approved, keep both branches in sync so dev never falls behind main
