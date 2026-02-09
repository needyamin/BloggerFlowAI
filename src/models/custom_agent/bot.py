import feedparser
import json
import re
import time
import requests
import trafilatura
from datetime import datetime
from .config import SOURCES, MAX_ITEMS, INTERVAL_MINUTES, TOPICS, TOPIC_KEYWORDS, OUTPUT_FILE

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}


def strip_html(s):
    return re.sub(r"<[^>]+>", " ", s or "").strip()


def fetch_full_content(url):
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        r.raise_for_status()
        return trafilatura.extract(r.text) or ""
    except Exception:
        return ""


def get_content(entry, link):
    full = fetch_full_content(link)
    if full:
        return full.strip()
    c = (entry.get("content") or [{}])[0].get("value", "")
    return strip_html(c or getattr(entry, "summary", "") or getattr(entry, "description", ""))


def matches_topic(text):
    t = (text or "").lower()
    # Check if any keyword from any topic mapping is in the text
    for major_topic, keywords in TOPIC_KEYWORDS.items():
        if any(kw.lower() in t for kw in keywords):
            return True
    return False


def fetch_feed(url):
    try:
        return feedparser.parse(url, request_headers={"User-Agent": "NewsBot/1.0"})
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None


def collect():
    seen = set()
    items = []
    print(f"[+] Scanning {len(SOURCES)} high-authority sources...")
    for url in SOURCES:
        feed = fetch_feed(url)
        if not feed or not feed.entries:
            continue
        source = feed.feed.get("title", url)
        for e in feed.entries:
            link = getattr(e, "link", "")
            if not link or link in seen:
                continue
            
            title = getattr(e, "title", "Untitled")
            published = getattr(e, "published", "")
            
            # Year filter: Priority to 2026. If no year mentioned, we might accept it 
            # if we are sure it's recent, but user requested strictness.
            if published:
                if not any(year in published for year in ["2026", "2027", "2028"]):
                    continue
            else:
                # If no date, we take a risk OR we skip. Let's skip for high authenticity.
                continue
                
            content = get_content(e, link)
            if not matches_topic(title) and not matches_topic(content):
                continue
                
            seen.add(link)
            items.append({
                "title": title,
                "content": content,
                "link": link,
                "source": source,
                "published": published,
            })
            if MAX_ITEMS and len(items) >= MAX_ITEMS:
                break
        if MAX_ITEMS and len(items) >= MAX_ITEMS:
            break
    return items


def run_once():
    """Collect news once and save to OUTPUT_FILE."""
    ts = datetime.now().isoformat()
    items = collect()
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump({"fetched": ts, "items": items}, f, indent=2, ensure_ascii=False)
    print(f"[+] News collected: {len(items)} items saved to {OUTPUT_FILE}")
    return items

def run():
    while True:
        ts = datetime.now().isoformat()
        print(f"\n--- {ts} ---")
        items = collect()
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump({"fetched": ts, "items": items}, f, indent=2, ensure_ascii=False)
        for item in items:
            print(f"\n[{item['source']}] {item['title']}")
            print(f"  {item['content'][:200]}")
            print(f"  {item['link']}")
        print(f"\nSaved to {OUTPUT_FILE}. Next run in {INTERVAL_MINUTES} min")
        time.sleep(INTERVAL_MINUTES * 60)


if __name__ == "__main__":
    run()
