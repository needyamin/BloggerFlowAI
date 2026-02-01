# News Bot

Collects news from trusted RSS feeds, fetches full article content, filters by topic, saves to JSON.

## Install

```bash
pip install -r requirements.txt
```

## Run

```bash
python bot.py
```

Runs every 60 min. Output: `news.json`

## Files

| File | Purpose |
|------|---------|
| `bot.py` | Main script: fetch feeds → filter by topic → scrape full content → save |
| `config.py` | `TOPICS`, `SOURCES`, `MAX_ITEMS` (0 = no limit), `INTERVAL_MINUTES` |
| `news.json` | Output: `{fetched, items[{title, content, link, source, published}]}` |

## Flow

1. Parse RSS feeds from BBC, NPR, Al Jazeera, Reuters
2. Keep only items whose title/content matches `TOPICS`
3. Fetch each article URL, extract full text via trafilatura
4. Save to `news.json`
