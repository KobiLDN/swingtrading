#!/usr/bin/env python3
"""
News Fetcher — Yahoo Finance RSS (no API key required)
Fetches the latest 8 news headlines for each tracked asset.
Writes news-data.js → window.NEWS_DATA = { generated, assets: { slug: [...] } }

Each article: { title, url, time_published, source, summary }

Usage:
    python update_news.py
"""

import sys
import json
import requests
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime

if sys.stdout.encoding and sys.stdout.encoding.lower() not in ('utf-8', 'utf-8-sig'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

OUTPUT_JS = 'news-data.js'
LIMIT     = 8

ASSETS = [
    {'slug': 'gbpusd', 'ticker': 'GBPUSD=X', 'label': 'GBP/USD'},
    {'slug': 'eurusd', 'ticker': 'EURUSD=X', 'label': 'EUR/USD'},
    {'slug': 'xauusd', 'ticker': 'XAUUSD=X', 'label': 'XAU/USD'},
    {'slug': 'xagusd', 'ticker': 'SLV',       'label': 'Silver'},
    {'slug': 'spx',    'ticker': 'SPY',        'label': 'SPX'},
    {'slug': 'oil',    'ticker': 'USO',        'label': 'WTI Crude Oil'},
]

RSS_URL = 'https://feeds.finance.yahoo.com/rss/2.0/headline?s={ticker}&region=US&lang=en-US'

HEADERS = {'User-Agent': 'Mozilla/5.0 (compatible; swingtrading-bot/1.0)'}


def fetch_news(ticker, label):
    url = RSS_URL.format(ticker=ticker)
    print(f'  Fetching news for {label} ({ticker}) ...')
    try:
        resp = requests.get(url, headers=HEADERS, timeout=20)
        resp.raise_for_status()
    except Exception as e:
        print(f'    Failed: {e}')
        return []

    try:
        root = ET.fromstring(resp.content)
    except ET.ParseError as e:
        print(f'    XML parse error: {e}')
        return []

    items = root.findall('./channel/item')
    articles = []
    for item in items[:LIMIT]:
        title   = (item.findtext('title')       or '').strip()
        link    = (item.findtext('link')        or '').strip()
        pub     = (item.findtext('pubDate')     or '').strip()
        summary = (item.findtext('description') or '').strip()

        # Strip HTML tags from summary
        import re
        summary = re.sub(r'<[^>]+>', '', summary)[:300].strip()

        # Normalise pubDate (RFC 2822) → "YYYY-MM-DD HH:MM"
        try:
            dt = parsedate_to_datetime(pub).astimezone(timezone.utc)
            display_time = dt.strftime('%Y-%m-%d %H:%M')
        except Exception:
            display_time = pub[:16]

        # Source: second-to-last segment of the link domain, or "Yahoo Finance"
        source = 'Yahoo Finance'
        try:
            from urllib.parse import urlparse
            host = urlparse(link).hostname or ''
            parts = [p for p in host.split('.') if p not in ('www', '')]
            if parts:
                source = parts[0].capitalize()
        except Exception:
            pass

        articles.append({
            'title':          title,
            'url':            link,
            'time_published': display_time,
            'source':         source,
            'summary':        summary,
        })

    print(f'    {len(articles)} articles fetched')
    return articles


def main():
    assets = {}
    for asset in ASSETS:
        assets[asset['slug']] = fetch_news(asset['ticker'], asset['label'])

    payload = {
        'generated': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
        'assets':    assets,
    }

    js = f'window.NEWS_DATA = {json.dumps(payload, indent=2)};\n'
    with open(OUTPUT_JS, 'w', encoding='utf-8') as f:
        f.write(js)

    total = sum(len(v) for v in assets.values())
    print(f'\nWritten: {OUTPUT_JS}  ({total} articles total)')
    print('Done.')


if __name__ == '__main__':
    main()
