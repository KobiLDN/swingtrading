# Prompt Templates

> Copy the relevant variant below, paste into Claude or ChatGPT, then append your OHLC JSON data.
> Attach or paste `encyclopedia.md` for consistent detection rules across sessions.

---

## Variant 1 — Quick Scan (30-second read)

```
Here is GBP/USD daily OHLC data for the last 20 candles.

Give me:
1. Current trend: BULLISH / BEARISH / NEUTRAL
2. Any patterns in the last 3 candles (candlestick or chart)
3. RSI(14) status: overbought / oversold / neutral + any divergence
4. One-line verdict: BUY / SELL / WAIT — and why in one sentence

[PASTE OHLC JSON HERE]
```

---

## Variant 2 — Full Deep Analysis

```
Here is GBP/USD daily OHLC data. Using the pattern rules from the encyclopedia, identify:

1. Current trend (bullish/bearish/neutral) with confidence %
2. Any candlestick patterns in the last 5 candles
3. Any chart patterns visible (triangles, double tops/bottoms, flags, wedges, H&S)
4. Current RSI(14) value and divergence status
5. MACD(12,26,9) signal — crossover or histogram direction
6. EMA alignment: 50 EMA vs 200 EMA (Golden Cross / Death Cross / neutral)
7. Key support and resistance levels (nearest above and below current price)
8. Volume confirmation: is the last candle supported by above-average volume?
9. The single most reliable trade setup visible right now
10. Score the setup using the 0-10 scoring system

Output:
- Decision: BUY / SELL / WAIT
- Risk score: X/10
- Entry zone: X.XXXX – X.XXXX
- Stop loss: X.XXXX (reason)
- Target: X.XXXX (reason)
- Invalidation: what price action would cancel this setup

[PASTE OHLC JSON HERE]
```

---

## Variant 3 — Entry / Exit Only

```
Here is GBP/USD daily OHLC data. Skip the explanation.

Output only:
- Action: BUY / SELL / WAIT
- Entry: X.XXXX
- Stop loss: X.XXXX
- Target 1: X.XXXX
- Target 2: X.XXXX (optional)
- Risk/reward: X:X
- Confidence: LOW / MEDIUM / HIGH

[PASTE OHLC JSON HERE]
```

---

## Tips

| Tip | Detail |
|-----|--------|
| Attach encyclopedia | Paste `encyclopedia.md` before the OHLC data for consistent results |
| Candle count | 20-50 daily candles is the sweet spot — enough for trend context, not too much noise |
| Recency bias | Always include the last 5 candles unbroken — don't skip recent data |
| 4H confirmation | Run Variant 1 on 4H data after a daily signal to confirm entry timing |
| Log the result | Paste the AI output into `trade_log.md` under the relevant date |
