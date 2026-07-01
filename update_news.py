#!/usr/bin/env python3
"""
News Sentiment Fetcher — Alpha Vantage
Fetches the latest 8 news articles + sentiment scores for each tracked asset.
Writes news-data.js → window.NEWS_DATA = { generated, assets: { gbpusd: [...], xauusd: [...], spx: [...] } }

Each article: { title, url, time_published, source, summary, sentiment_label, sentiment_score }

Usage:
    python update_news.py

Requires:
    ALPHA_VANTAGE_API_KEY environment variable
    pip install requests python-dotenv
"""

import os
import sys
import json
import requests
from datetime import datetime, timezone

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

if sys.stdout.encoding and sys.stdout.encoding.lower() not in ('utf-8', 'utf-8-sig'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

API_KEY   = os.environ.get('ALPHA_VANTAGE_API_KEY', '')
BASE_URL  = 'https://www.alphavantage.co/query'
OUTPUT_JS = 'news-data.js'
LIMIT     = 8  # articles per asset

ASSETS = [
    {'slug': 'gbpusd', 'ticker': 'FOREX:GBPUSD',    'label': 'GBP/USD'},
    {'slug': 'xauusd', 'ticker': 'FOREX:XAUUSD',    'label': 'XAU/USD'},
    {'slug': 'spx',    'ticker': 'EQUITY:SPY',       'label': 'SPX'},
    {'slug': 'oil',    'ticker': 'COMMODITY:USOIL',  'label': 'WTI Crude Oil'},
]


def fetch_news(ticker, label):
    if not API_KEY:
        print(f"  ALPHA_VANTAGE_API_KEY not set — skipping {label}")
        return []

    params = {
        'function': 'NEWS_SENTIMENT',
        'tickers':  ticker,
        'sort':     'LATEST',
        'limit':    LIMIT,
        'apikey':   API_KEY,
    }

    print(f"  Fetching news for {label} ({ticker}) ...")
    try:
        resp = requests.get(BASE_URL, params=params, timeout=30)
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        print(f"    Failed: {e}")
        return []

    if 'Information' in data:
        print(f"    API limit hit: {data['Information'][:80]}")
        return []

    if 'Note' in data:
        print(f"    API note: {data['Note'][:80]}")
        return []

    feed = data.get('feed', [])
    if not feed:
        print(f"    No articles returned")
        return []

    articles = []
    for item in feed[:LIMIT]:
        # Find per-ticker sentiment if available
        ts_label = item.get('overall_sentiment_label', 'Neutral')
        ts_score = float(item.get('overall_sentiment_score', 0))

        for ts in item.get('ticker_sentiment', []):
            if ts.get('ticker', '').upper() == ticker.upper():
                ts_label = ts.get('ticker_sentiment_label', ts_label)
                try:
                    ts_score = float(ts.get('ticker_sentiment_score', ts_score))
                except (ValueError, TypeError):
                    pass
                break

        # Normalise time: "20240605T143000" → "2024-06-05 14:30"
        raw_time = str(item.get('time_published', ''))
        try:
            dt = datetime.strptime(raw_time, '%Y%m%dT%H%M%S')
            display_time = dt.strftime('%Y-%m-%d %H:%M')
        except ValueError:
            display_time = raw_time[:16]

        articles.append({
            'title':           item.get('title', ''),
            'url':             item.get('url', ''),
            'time_published':  display_time,
            'source':          item.get('source', ''),
            'summary':         item.get('summary', '')[:300],
            'sentiment_label': ts_label,
            'sentiment_score': round(ts_score, 4),
        })

    print(f"    {len(articles)} articles fetched")
    return articles


def main():
    if not API_KEY:
        print("ALPHA_VANTAGE_API_KEY not set — writing empty news data")

    assets = {}
    for asset in ASSETS:
        assets[asset['slug']] = fetch_news(asset['ticker'], asset['label'])

    payload = {
        'generated': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
        'assets':    assets,
    }

    js = f"window.NEWS_DATA = {json.dumps(payload, indent=2)};\n"
    with open(OUTPUT_JS, 'w', encoding='utf-8') as f:
        f.write(js)

    total = sum(len(v) for v in assets.values())
    print(f"\nWritten: {OUTPUT_JS}  ({total} articles total)")
    print("Done.")


if __name__ == '__main__':
    main()
