# Branches

All pushes must go to **both branches** every time. Never leave one behind.

## Push sequence (after every commit)

```bash
git pull --rebase origin main
git push origin main
git push origin main:claude/friendly-dijkstra-lBUrd
```

---

## Branch table

| Branch | Type | Session | Purpose |
|---|---|---|---|
| `main` | Local + Remote | trading/local (this session) | Live GitHub Pages — source of truth |
| `claude/friendly-dijkstra-lBUrd` | Remote only | trading/cloud (claude.ai) | Cloud session branch — must always match main |

---

## Notes

- Only one local folder: `G:\My Drive\coding\ai\Trading\SwingTrading` — always on `main`
- GitHub Pages serves from `main` — pushing main = site is live
- `claude/friendly-dijkstra-lBUrd` accepts a normal push: `git push origin main:claude/friendly-dijkstra-lBUrd`
