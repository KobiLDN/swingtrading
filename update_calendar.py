#!/usr/bin/env python3
"""
Economic Calendar Fetcher
Fetches high-impact economic events from Twelve Data for the next 7 days.
Filters for USD, GBP, and EUR — the currencies that move GBP/USD, XAU/USD, and SPX.
Writes calendar-data.js → window.CALENDAR_DATA = { generated, events: [...] }

Usage:
    python update_calendar.py

Requires:
    TWELVE_DATA_API_KEY environment variable (or .env file)
    pip install requests python-dotenv
"""

import os
import sys
import json
import requests
from datetime import datetime, timezone, timedelta

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

if sys.stdout.encoding and sys.stdout.encoding.lower() not in ('utf-8', 'utf-8-sig'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

API_KEY   = os.environ.get('TWELVE_DATA_API_KEY', '')
OUTPUT_JS = 'calendar-data.js'

# Currencies we care about (affect GBP/USD, XAU/USD, SPX)
RELEVANT_CURRENCIES = {'USD', 'GBP', 'EUR'}


def fetch_calendar():
    if not API_KEY:
        print("TWELVE_DATA_API_KEY not set — writing empty calendar")
        return []

    today = datetime.now(timezone.utc).date()
    end   = today + timedelta(days=7)

    url = (
        f"https://api.twelvedata.com/economic_calendar"
        f"?start_date={today}&end_date={end}"
        f"&apikey={API_KEY}"
    )

    print(f"Fetching economic calendar {today} → {end} ...")
    try:
        resp = requests.get(url, timeout=30)
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        print(f"  Calendar fetch failed: {e}")
        return []

    if data.get('status') == 'error':
        print(f"  Calendar API error: {data.get('message', 'unknown')}")
        return []

    # Twelve Data returns events under 'result' key
    raw_events = data.get('result', data.get('data', data.get('events', [])))
    if not isinstance(raw_events, list):
        print(f"  Unexpected response format: {list(data.keys())}")
        return []

    out = []
    today_str = str(today)

    for e in raw_events:
        currency = str(e.get('currency', e.get('country', ''))).upper()
        if currency not in RELEVANT_CURRENCIES:
            continue

        importance = str(e.get('importance', e.get('impact', ''))).lower()
        # Only keep high-impact events
        if importance not in ('high', '3', 'major'):
            continue

        event_date = str(e.get('date', ''))
        event_time = str(e.get('time', e.get('datetime', '')))

        # Extract just the time part if datetime is included
        if 'T' in event_time:
            event_time = event_time.split('T')[1][:5]

        out.append({
            'date':     event_date,
            'time':     event_time,
            'currency': currency,
            'event':    str(e.get('event', e.get('name', e.get('description', '')))),
            'impact':   'high',
            'forecast': str(e.get('forecast', '')),
            'previous': str(e.get('previous', '')),
            'actual':   str(e.get('actual', '')),
            'today':    event_date == today_str,
        })

    # Sort by date then time
    out.sort(key=lambda x: (x['date'], x['time']))

    print(f"  {len(out)} high-impact events found (USD/GBP/EUR)")
    return out


def main():
    events = fetch_calendar()

    payload = {
        'generated': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
        'events':    events,
    }

    js = f"window.CALENDAR_DATA = {json.dumps(payload, indent=2)};\n"
    with open(OUTPUT_JS, 'w', encoding='utf-8') as f:
        f.write(js)
    print(f"  Written: {OUTPUT_JS}  ({len(events)} events)")

    # Print today's events as a quick summary
    today_events = [e for e in events if e.get('today')]
    if today_events:
        print(f"\n  ⚠  TODAY'S HIGH-IMPACT EVENTS:")
        for e in today_events:
            print(f"     {e['time']} UTC  {e['currency']}  {e['event']}")
    else:
        print("  No high-impact events today.")

    print("\nDone.")


if __name__ == '__main__':
    main()
