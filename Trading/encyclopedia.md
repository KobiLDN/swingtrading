# Pattern Recognition Guide

> Reference for GBP/USD swing trading. Use these exact detection rules when analyzing OHLC data.

---

## 1. Candlestick Patterns (Single Candle)

**Detection Logic:** All patterns use daily OHLC data. Body size = |Close - Open|. Total range = High - Low.

| Pattern | Signal | Detection Rule | Strength (1-5) |
|---------|--------|----------------|-----------------|
| **Hammer** | Bullish reversal | Body ≤ 30% of range, lower wick ≥ 2.2× body, small body at top, appears after downtrend | 3 |
| **Inverted Hammer** | Bullish reversal | Body ≤ 30% of range, upper wick ≥ 2.2× body, small body at bottom, appears after downtrend | 3 |
| **Shooting Star** | Bearish reversal | Body ≤ 30% of range, upper wick ≥ 2.2× body, small body at bottom, appears after uptrend | 3 |
| **Hanging Man** | Bearish reversal | Body ≤ 30% of range, lower wick ≥ 2.2× body, small body at top, appears after uptrend | 3 |
| **Bullish Engulfing** | Strong bullish | Current bullish candle (Close > Open) completely engulfs previous bearish candle body (Open > Close) | 4 |
| **Bearish Engulfing** | Strong bearish | Current bearish candle (Open > Close) completely engulfs previous bullish candle body (Close > Open) | 4 |
| **Morning Star** | Strong bullish reversal | Bearish candle → Doji → Bullish candle (second gap down, third closes ≥ midpoint of first) | 5 |
| **Evening Star** | Strong bearish reversal | Bullish candle → Doji → Bearish candle (second gap up, third closes ≤ midpoint of first) | 5 |
| **Doji** | Indecision/reversal | Body ≤ 5% of total range | 2 |

---

## 2. Chart Patterns (Multi-Candle)

### Reversal Patterns

| Pattern | Bias | Detection Rule | Target Calculation |
|---------|------|----------------|--------------------|
| **Head & Shoulders** | Bearish | Three peaks: center (head) highest, left/right shoulders similar (±2%), neckline connects troughs | Head height subtracted from neckline break |
| **Inverse H&S** | Bullish | Three troughs: center deepest, shoulders similar (±2%), neckline connects peaks | Head height added to neckline break |
| **Double Top** | Bearish | Two highs within 2% of each other, valley between ≥3% below highs | Height = highs - valley, subtracted from breakdown |
| **Double Bottom** | Bullish | Two lows within 2% of each other, peak between ≥3% above lows | Height = peak - lows, added to breakout |
| **Triple Top** | Bearish | Three touches at same resistance (±1%), fails each time | Resistance - support, subtracted from breakdown |
| **Triple Bottom** | Bullish | Three touches at same support (±1%), holds each time | Resistance - support, added to breakout |

### Continuation Patterns

| Pattern | Bias | Detection Rule | Breakout Direction |
|---------|------|----------------|--------------------|
| **Ascending Triangle** | Bullish | Flat top resistance, rising bottom trendline (higher lows) | Above flat top (≥1× ATR) |
| **Descending Triangle** | Bearish | Flat bottom support, falling top trendline (lower highs) | Below flat bottom (≥1× ATR) |
| **Symmetrical Triangle** | Directional | Converging trendlines (rising lows, falling highs) | Whichever direction first (≥1.5× ATR) |
| **Bull Flag** | Bullish | Sharp vertical rise → parallel or downward-sloping consolidation (10-40 candles) | Above flag top |
| **Bear Flag** | Bearish | Sharp vertical drop → parallel or upward-sloping consolidation (10-40 candles) | Below flag bottom |
| **Rising Wedge** | Bearish | Both trendlines rising, upper line steeper → converging | Below lower trendline |
| **Falling Wedge** | Bullish | Both trendlines falling, lower line steeper → converging | Above upper trendline |

---

## 3. Support & Resistance

| Concept | Detection Rule | Confirmation |
|---------|----------------|--------------|
| **Support** | Price bounces from same level ≥2 times within 3% range | Volume increases on bounce |
| **Resistance** | Price rejects from same level ≥2 times within 3% range | Volume increases on rejection |
| **Breakout** | Close ≥1× ATR above resistance or below support | Volume ≥1.5× 20-day average |
| **Role Reversal** | Broken support becomes new resistance (or vice versa) | Price retests and reverses |

---

## 4. Momentum Indicators

### RSI (Relative Strength Index) — 14-period default

| Value | Interpretation | Action |
|-------|----------------|--------|
| >70 | Overbought | Look for bearish reversal patterns |
| <30 | Oversold | Look for bullish reversal patterns |
| 30-70 | Neutral | Follow trend direction |

**Divergence Detection:**
- **Bearish divergence:** Price makes higher high, RSI makes lower high → SELL signal
- **Bullish divergence:** Price makes lower low, RSI makes higher low → BUY signal

### MACD (12, 26, 9)

| Condition | Signal |
|-----------|--------|
| MACD line crosses above Signal line | Bullish momentum |
| MACD line crosses below Signal line | Bearish momentum |
| Histogram turns from negative to positive | Momentum acceleration up |
| Histogram turns from positive to negative | Momentum acceleration down |

### Moving Averages (50 EMA & 200 EMA)

| Condition | Bias | Strength |
|-----------|------|----------|
| 50 EMA > 200 EMA | Bullish | Trend |
| 50 EMA < 200 EMA | Bearish | Trend |
| 50 EMA crosses above 200 EMA | Golden Cross | Major bullish (confirm with volume) |
| 50 EMA crosses below 200 EMA | Death Cross | Major bearish (confirm with volume) |
| Price > 50 EMA > 200 EMA | Strong uptrend | Buy on pullbacks to 50 EMA |
| Price < 50 EMA < 200 EMA | Strong downtrend | Sell on rallies to 50 EMA |

---

## 5. Volume Confirmation Rules

| Scenario | Valid Signal | Weak/False Signal |
|----------|--------------|--------------------|
| Breakout above resistance | Volume ≥ 1.5× 20-day avg | Volume below average |
| Breakout below support | Volume ≥ 1.5× 20-day avg | Volume below average |
| Bullish engulfing | Volume ≥ 1.2× previous candle | Volume shrinking |
| Bearish engulfing | Volume ≥ 1.2× previous candle | Volume shrinking |

---

## 6. GBP/USD Specific Characteristics

| Factor | Typical Behavior |
|--------|------------------|
| London-NY overlap (12-16 GMT) | Highest volatility, best entries |
| Asian session (00-09 GMT) | Range-bound, false breakouts common |
| Average daily range | 70-120 pips (varies by volatility regime) |
| Key economic drivers | BOE rate decisions, US NFP, CPI from both |
| Typical swing duration | 3-10 days (daily chart) or 1-3 days (4H chart) |

---

## 7. Combined Signal Scoring System

Score each setup (0-10):

| Factor | Points |
|--------|--------|
| Pattern reliability (chart pattern = +4, candlestick = +2) | 0-4 |
| RSI confirms (oversold/overbought = +2, divergence = +3) | 0-3 |
| Volume confirms (≥1.5× avg = +2) | 0-2 |
| S/R alignment (at key level = +1) | 0-1 |

**Decision matrix:**
- **8-10:** Strong BUY/SELL — take trade
- **5-7:** WATCH — wait for confirmation
- **0-4:** NO TRADE — insufficient signals

---

## 8. Quick Detection Pseudocode

```python
# Hammer detection
def is_hammer(candle):
    body = abs(candle['close'] - candle['open'])
    range_total = candle['high'] - candle['low']
    lower_wick = min(candle['open'], candle['close']) - candle['low']

    return (body / range_total <= 0.3 and
            lower_wick >= 2.2 * body and
            candle['close'] > candle['open'])  # bullish

# Support detection (requires historical data)
def is_at_support(price, swing_lows, tolerance=0.02):
    return any(abs(price - low) / low <= tolerance for low in swing_lows)

# RSI calculation (14-period)
def calculate_rsi(prices, period=14):
    gains = [max(prices[i] - prices[i-1], 0) for i in range(1, len(prices))]
    losses = [max(prices[i-1] - prices[i], 0) for i in range(1, len(prices))]
    # ... standard Wilder's smoothing
```

---

## References

### Core Detection Sources
- Bulkowski's pattern reliability ratings (*Encyclopedia of Chart Patterns*, 3rd Edition) — win rates, failure rates, average hold times for all Section 2 patterns
- Nison's candlestick criteria (*Japanese Candlestick Charting Techniques*) — source material for all 9 patterns in Section 1
- Wilder's RSI and momentum principles
- Pattern Zoo volume confirmation rules

### Complete Trading Library (39 Books)

**Part 1 — Swing Trading & Legends (14)**
1. George Soros — *The Alchemy of Finance*
2. Paul Tudor Jones — *Trader* documentary + *Market Wizards* content
3. Stanley Druckenmiller — *Market Wizards* series interviews
4. Jesse Livermore (Edwin Lefèvre) — *Reminiscences of a Stock Operator*
5. Nicolas Darvas — *How I Made $2,000,000 in the Stock Market*
6. William J. O'Neil — *How to Make Money in Stocks*
7. Alan S. Farley — *The Master Swing Trader*
8. John F. Carter — *Mastering the Trade* (3rd Edition)
9. Mark Minervini — *Trade Like a Stock Market Wizard*
10. Mark Minervini — *Think & Trade Like a Champion*
11. Brian Pezim & Andrew Aziz — *How to Swing Trade*
12. Omar Bassal, CFA — *Swing Trading For Dummies*
13. Brett N. Steenbarger — *The Psychology of Trading*
14. Jack D. Schwager — *Market Wizards* series (3 volumes)

**Part 2 — Warren Buffett Collection (11)**
15. Lawrence Cunningham — *The Essays of Warren Buffett* ★ Primary source
16. Mary Buffett & David Clark — *The New Tao of Warren Buffett* (2024)
17. Mary Buffett & David Clark — *The Tao of Warren Buffett*
18. Mary Buffett & David Clark — *Buffettology*
19. Mary Buffett & David Clark — *Warren Buffett and the Interpretation of Financial Statements*
20. Mary Buffett & Sean Seah — *7 Secrets to Investing Like Warren Buffett*
21. Roger Lowenstein — *Buffett: The Biography* ★ Definitive biography
22. Daniel Pecaut — *University of Berkshire Hathaway*
23. Danielle Town — *Invested*
24. Charles R. Morris — *The Sages*
25. Anthony McCarten — *Warren and Bill* (2024)

**Part 3 — Books Buffett Recommends (14)**
26. Benjamin Graham — *The Intelligent Investor* ★ "By far the best book about investing ever written"
27. Benjamin Graham & David Dodd — *Security Analysis*
28. Philip Fisher — *Common Stocks and Uncommon Profits*
29. Charles T. Munger — *Poor Charlie's Almanack*
30. John Brooks — *Business Adventures* (Buffett's favourite business book)
31. John C. Bogle — *The Little Book of Common Sense Investing*
32. John C. Bogle — *The Clash of Cultures*
33. William N. Thorndike — *The Outsiders*
34. Howard Marks — *The Most Important Thing*
35. Fred Schwed Jr. — *Where Are the Customers' Yachts?*
36. Phil Knight — *Shoe Dog*
37. Walter Isaacson — *The Innovators*
38. John Kenneth Galbraith — *The Great Crash of 1929*
39. John Maynard Keynes — *Essays in Persuasion*
