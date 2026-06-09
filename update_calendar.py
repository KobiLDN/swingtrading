#!/usr/bin/env python3
"""
Economic Calendar Fetcher — dual source
Sources:
  1. Forex Factory JSON (no key, always populated) — primary
  2. Twelve Data /economic_calendar (requires TWELVE_DATA_API_KEY) — supplementary

Events are merged and deduplicated. Filters for USD, GBP, EUR high-impact only.
Writes calendar-data.js → window.CALENDAR_DATA = { generated, events: [...] }

Usage:
    python update_calendar.py

Requires:
    TWELVE_DATA_API_KEY environment variable (optional — FF works without it)
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

RELEVANT_CURRENCIES = {'USD', 'GBP', 'EUR'}

FF_URLS = [
    'https://nfs.faireconomy.media/ff_calendar_thisweek.json',
    'https://nfs.faireconomy.media/ff_calendar_nextweek.json',
]


# ── Forex Factory source ────────────────────────────────────────────────────────

def fetch_ff():
    """Fetch this week + next week from the Forex Factory JSON feed."""
    events = []
    for url in FF_URLS:
        try:
            resp = requests.get(url, timeout=15)
            resp.raise_for_status()
            raw = resp.json()
        except Exception as e:
            print(f"  FF fetch failed ({url}): {e}")
            continue

        for e in raw:
            currency = str(e.get('country', '')).upper()
            if currency not in RELEVANT_CURRENCIES:
                continue

            impact = str(e.get('impact', '')).lower()
            if impact != 'high':
                continue

            # FF date is ISO 8601 e.g. "2026-06-10T12:30:00-04:00"
            raw_date = str(e.get('date', ''))
            try:
                dt = datetime.fromisoformat(raw_date)
                event_date = dt.strftime('%Y-%m-%d')
                event_time = dt.strftime('%H:%M')
            except Exception:
                event_date = raw_date[:10] if len(raw_date) >= 10 else raw_date
                event_time = ''

            events.append({
                'date':     event_date,
                'time':     event_time,
                'currency': currency,
                'event':    str(e.get('title', '')),
                'impact':   'high',
                'forecast': str(e.get('forecast', '')),
                'previous': str(e.get('previous', '')),
                'actual':   str(e.get('actual', '')),
                'source':   'ff',
            })

    print(f"  Forex Factory: {len(events)} high-impact USD/GBP/EUR events")
    return events


# ── Twelve Data source ──────────────────────────────────────────────────────────

def fetch_twelve_data():
    """Fetch next 7 days from Twelve Data (supplementary — requires API key)."""
    if not API_KEY:
        print("  Twelve Data: no API key — skipping")
        return []

    today = datetime.now(timezone.utc).date()
    end   = today + timedelta(days=7)
    url = (
        f"https://api.twelvedata.com/economic_calendar"
        f"?start_date={today}&end_date={end}"
        f"&apikey={API_KEY}"
    )

    print(f"  Twelve Data: fetching {today} → {end} ...")
    try:
        resp = requests.get(url, timeout=30)
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        print(f"  Twelve Data fetch failed: {e}")
        return []

    if data.get('status') == 'error':
        print(f"  Twelve Data error: {data.get('message', 'unknown')}")
        return []

    raw_events = data.get('result', data.get('data', data.get('events', [])))
    if not isinstance(raw_events, list):
        print(f"  Twelve Data unexpected format: {list(data.keys())}")
        return []

    events = []
    for e in raw_events:
        currency = str(e.get('currency', e.get('country', ''))).upper()
        if currency not in RELEVANT_CURRENCIES:
            continue

        importance = str(e.get('importance', e.get('impact', ''))).lower()
        if importance not in ('high', '3', 'major'):
            continue

        event_date = str(e.get('date', ''))
        event_time = str(e.get('time', e.get('datetime', '')))
        if 'T' in event_time:
            event_time = event_time.split('T')[1][:5]

        events.append({
            'date':     event_date,
            'time':     event_time,
            'currency': currency,
            'event':    str(e.get('event', e.get('name', e.get('description', '')))),
            'impact':   'high',
            'forecast': str(e.get('forecast', '')),
            'previous': str(e.get('previous', '')),
            'actual':   str(e.get('actual', '')),
            'source':   'td',
        })

    print(f"  Twelve Data: {len(events)} high-impact USD/GBP/EUR events")
    return events


# ── Merge + deduplicate ─────────────────────────────────────────────────────────

def _dedup_key(e):
    """Normalise event name for deduplication: lowercase, strip punctuation."""
    name = e['event'].lower()
    for ch in '()[].,\'-/':
        name = name.replace(ch, ' ')
    name = ' '.join(name.split())  # collapse whitespace
    return (e['date'], e['currency'], name[:40])


def merge_events(ff_events, td_events):
    """
    Primary: Forex Factory.
    Supplementary: Twelve Data adds events not already in FF.
    Dedup by (date, currency, normalised title prefix).
    """
    seen = {_dedup_key(e) for e in ff_events}
    extra = []
    for e in td_events:
        k = _dedup_key(e)
        if k not in seen:
            seen.add(k)
            extra.append(e)

    merged = ff_events + extra
    merged.sort(key=lambda x: (x['date'], x['time']))

    if extra:
        print(f"  Twelve Data added {len(extra)} unique event(s) not in FF")
    else:
        print(f"  Twelve Data: no new events beyond FF")

    # Strip internal 'source' key before writing
    for e in merged:
        e.pop('source', None)

    return merged


# ── Filter to next 7 days ───────────────────────────────────────────────────────

def filter_window(events):
    today = datetime.now(timezone.utc).date()
    end   = today + timedelta(days=7)
    today_str = str(today)
    end_str   = str(end)

    filtered = [e for e in events if today_str <= e['date'] <= end_str]

    # Tag today's events for amber highlight on dashboard
    for e in filtered:
        e['today'] = (e['date'] == today_str)

    return filtered


# ── Main ────────────────────────────────────────────────────────────────────────

def main():
    print("Fetching economic calendar (dual source) ...")

    ff_events = fetch_ff()
    td_events = fetch_twelve_data()
    merged    = merge_events(ff_events, td_events)
    events    = filter_window(merged)

    payload = {
        'generated': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
        'events':    events,
    }

    js = f"window.CALENDAR_DATA = {json.dumps(payload, indent=2)};\n"
    with open(OUTPUT_JS, 'w', encoding='utf-8') as f:
        f.write(js)
    print(f"\n  Written: {OUTPUT_JS}  ({len(events)} events in next 7 days)")

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
