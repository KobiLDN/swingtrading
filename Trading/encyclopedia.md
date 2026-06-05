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

**What it is:** RSI measures the speed and size of recent price moves on a 0–100 scale. It answers the question: *has price moved too far too fast in one direction?* It compares the average size of up-moves to down-moves over the last 14 candles. A reading above 70 means buyers have been dominant and the move may be exhausted; below 30 means sellers have been dominant. RSI is most useful as a *confirmation* tool — a pattern at a key S/R level with RSI confirming is a stronger signal than either alone.

| Value | Interpretation | Action |
|-------|----------------|--------|
| >70 | Overbought | Look for bearish reversal patterns |
| <30 | Oversold | Look for bullish reversal patterns |
| 30-70 | Neutral | Follow trend direction |

**Divergence Detection:**
Divergence means price and RSI disagree — price makes a new extreme but RSI does not confirm it, signalling weakening momentum before price reverses.
- **Bearish divergence:** Price makes higher high, RSI makes lower high → momentum fading, SELL signal
- **Bullish divergence:** Price makes lower low, RSI makes higher low → momentum fading, BUY signal

### MACD (Moving Average Convergence Divergence) — 12, 26, 9

**What it is:** MACD measures the relationship between two EMAs of closing price (fast 12-period and slow 26-period). When the fast EMA pulls away from the slow EMA, momentum is building. The three components are:
- **MACD line** — the gap between EMA(12) and EMA(26). Positive = fast above slow = bullish momentum.
- **Signal line** — 9-period EMA of the MACD line. Acts as a trigger.
- **Histogram** — MACD line minus Signal line. Shows whether momentum is accelerating or decelerating. Bars growing = momentum building; bars shrinking = momentum fading.

| Condition | Signal |
|-----------|--------|
| MACD line crosses above Signal line | Bullish momentum |
| MACD line crosses below Signal line | Bearish momentum |
| Histogram turns from negative to positive | Momentum acceleration up |
| Histogram turns from positive to negative | Momentum acceleration down |
| Histogram shrinking (towards zero) | Momentum fading — potential reversal |

### Moving Averages (50 EMA & 200 EMA)

**What they are:** An EMA (Exponential Moving Average) is the average closing price over N candles, with recent candles weighted more heavily than older ones. The 50 EMA tracks the medium-term trend; the 200 EMA tracks the long-term trend. When price is above both EMAs, conditions favour longs. When both EMAs slope upward and price pulls back to the 50 EMA, that is a classic trend continuation entry.

| Condition | Bias | Strength |
|-----------|------|----------|
| 50 EMA > 200 EMA | Bullish | Trend |
| 50 EMA < 200 EMA | Bearish | Trend |
| 50 EMA crosses above 200 EMA | Golden Cross | Major bullish (confirm with volume) |
| 50 EMA crosses below 200 EMA | Death Cross | Major bearish (confirm with volume) |
| Price > 50 EMA > 200 EMA | Strong uptrend | Buy on pullbacks to 50 EMA |
| Price < 50 EMA < 200 EMA | Strong downtrend | Sell on rallies to 50 EMA |

### ATR (Average True Range) — 14-period

**What it is:** ATR measures volatility — specifically, the average size of a daily candle (including gaps) over the last 14 days, expressed in price units. It tells you *how much the market typically moves in a day*, which is used to size stop losses and targets proportionally. On GBP/USD daily, ATR is typically 70–120 pips. A stop loss of 1× ATR means the trade has room to breathe through normal daily fluctuation without being stopped out by noise.

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

- Bulkowski's pattern reliability ratings
- Nison's candlestick criteria
- Wilder's RSI and momentum principles
- Pattern Zoo volume confirmation rules

---

## 9. Recommended Reading

### Top Swing Traders & Their Books

| # | Trader / Author | Known For | Book(s) |
|---|-----------------|-----------|---------|
| 1 | **George Soros** | "Broke the Bank of England" in 1992, $1B+ profit shorting GBP | *The Alchemy of Finance* |
| 2 | **Paul Tudor Jones** | Anticipated 1987 Black Monday crash, made ~$100M | No single book — study via *Market Wizards* interviews and *Trader* documentary |
| 3 | **Stanley Druckenmiller** | Macro hedge fund legend; worked with Soros on the GBP trade | No single book — appears in *The New Market Wizards* and interviews |
| 4 | **Jesse Livermore** | Early 1900s trader; shorted the 1929 crash | *Reminiscences of a Stock Operator* (Edwin Lefèvre) |
| 5 | **Nicolas Darvas** | Turned $25,000 into $2M+ in 18 months with the Darvas Box system | *How I Made $2,000,000 in the Stock Market* |
| 6 | **William J. O'Neil** | Founded Investor's Business Daily; developed the CAN SLIM system | *How to Make Money in Stocks* |
| 7 | **Alan S. Farley** | Swing trading author; CNBC contributor; TheStreet.com columnist | *The Master Swing Trader* |
| 8 | **John F. Carter** | Systematic trader; founder of TradetheMarkets.com | *Mastering the Trade* (3rd ed.) |
| 9 | **Mark Minervini** | Renowned for consistent outsized returns; trend following advocate | *Trade Like a Stock Market Wizard* · *Think & Trade Like a Champion* |
| 10 | **Brian Pezim & Andrew Aziz** | Beginner-focused; Pezim trading since 1967; Aziz Forbes Council member | *How to Swing Trade* |
| 11 | **Omar Bassal, CFA** | CIO with 30 years experience; MBA from Wharton | *Swing Trading For Dummies* |
| 12 | **Brett N. Steenbarger** | Trading psychology specialist; active trader | *The Psychology of Trading* |

---

### Market Wizards Series (Jack D. Schwager)

Interview-based books covering many of the traders above. Essential reading for understanding how professionals think.

| Book | Key Traders Featured |
|------|---------------------|
| *Market Wizards* | Paul Tudor Jones, Ed Seykota, Bruce Kovner |
| *The New Market Wizards* | Stanley Druckenmiller, William O'Neil |
| *Stock Market Wizards* | Various short-term traders |

---

### Trader Archetypes

| Archetype | Traders | Best for learning |
|-----------|---------|-------------------|
| **Macro swing** | Soros, Tudor Jones, Druckenmiller | Big-picture entries/exits, catalyst trading, GBP/USD drivers |
| **Technical / mechanical** | Darvas, Farley, Carter | Box theory, pattern rules, systematic execution |
| **Momentum / breakout** | Minervini, O'Neil | CAN SLIM, VCP setups, pivot points |
| **Psychology / discipline** | Livermore, Steenbarger | Mindset, cutting losses, learning from mistakes |
| **Beginner foundation** | Aziz, Bassal | Basic mechanics, position sizing, risk management |
