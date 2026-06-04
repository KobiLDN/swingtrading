# GBP/USD Swing Trading Dashboard

> Live analysis page powered by AI (Claude/GPT). Paste fresh OHLC data below for instant technical analysis.

---

## 📥 Data Input

Fetch fresh GBP/USD daily data from [Twelve Data](https://twelvedata.com/) or [Alpha Vantage](https://www.alphavantage.co/):

```json
// Paste your OHLC JSON here. Example format:
{
  "symbol": "GBP/USD",
  "values": [
    {"datetime": "2026-06-03", "open": "1.2750", "high": "1.2785", "low": "1.2732", "close": "1.2768"},
    {"datetime": "2026-06-02", "open": "1.2720", "high": "1.2765", "low": "1.2710", "close": "1.2750"}
  ]
}
```

---

## 🤖 AI Analysis Prompt

Copy this prompt and paste it to Claude or ChatGPT along with your JSON data:

> *"Here is GBP/USD daily OHLC data. Using the pattern rules from the attached knowledge base, please identify:*
>
> 1. *Current trend (bullish/bearish/neutral) with confidence %*
> 2. *Any candlestick patterns in the last 5 candles*
> 3. *Any chart patterns visible (triangles, double tops/bottoms, flags)*
> 4. *Current RSI(14) value and divergence status*
> 5. *Key support and resistance levels*
> 6. *The single most reliable trade setup visible right now*
>
> *Then output a simple decision: BUY / SELL / WAIT with a risk score (1-10)."*

---

## 📊 Quick Reference Card

| Condition | Action |
|-----------|--------|
| RSI <30 + Hammer + at support | **BUY** |
| RSI >70 + Shooting Star + at resistance | **SELL** |
| Golden Cross (50 EMA > 200 EMA) | Bullish bias |
| Death Cross (50 EMA < 200 EMA) | Bearish bias |
| Bullish Engulfing at support | **BUY** (high confidence) |
| Bearish Engulfing at resistance | **SELL** (high confidence) |

---

## 📈 Last Analysis (Example)

*Run the prompt above with your current data. Results will appear here.*

**Current Bias:** —  
**Best Setup:** —  
**Recommended Action:** WAIT  
**Risk Score:** —/10

---

## 🔗 Resources

- [Pattern Recognition Guide](encyclopedia.md) — Full reference for candlestick and chart patterns
- [Twelve Data API](https://twelvedata.com/) — Free JSON endpoint
- [TradingView GBP/USD](https://www.tradingview.com/symbols/GBPUSD/) — Chart verification
