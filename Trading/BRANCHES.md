# Branches

All pushes must go to **all three branches** every time. Never leave one behind.

## Push sequence (after every commit)

```bash
git pull --rebase origin main
git push origin main
git push origin --delete dev && git push origin main:dev
git push origin main:claude/friendly-dijkstra-lBUrd
```

---

## Branch table

| Branch | Type | Session | Purpose |
|---|---|---|---|
| `main` | Local + Remote | trading/local (this session) | Live GitHub Pages — source of truth |
| `dev` | Remote only (no local checkout) | trading/local (this session) | Dev mirror — delete+recreate from main each sync; no separate local folder |
| `claude/friendly-dijkstra-lBUrd` | Remote only | trading/cloud (claude.ai) | Cloud session branch — must receive every main push |

---

## Notes

- `dev` cannot be force-pushed — use delete+recreate pattern (`git push origin --delete dev && git push origin main:dev`)
- `claude/friendly-dijkstra-lBUrd` accepts a normal push: `git push origin main:claude/friendly-dijkstra-lBUrd`
- GitHub Pages serves from `main` — pushing main = site is live
- `dev` and `claude/friendly-dijkstra-lBUrd` should always match `main` HEAD after a sync
