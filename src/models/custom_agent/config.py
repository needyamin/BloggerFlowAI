import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
OUTPUT_FILE = os.getenv("NEWS_OUTPUT") or str(BASE_DIR / "data" / "news.json")

# High-Authority & High-Paid Categories
TOPICS = [
    "Education & Learning",
    "Scholarships & Study Abroad",
    "International (Overseas) News",
    "Latest Tech News",
    "Unique & Innovative Gadget Reviews"
]

# Keyword mapping for better matching in RSS feeds
TOPIC_KEYWORDS = {
    "Education & Learning": ["education", "learning", "university", "school", "student", "teacher", "curriculum", "online course"],
    "Scholarships & Study Abroad": ["scholarship", "study abroad", "fellowship", "grant", "international student", "funding", "bursary"],
    "International (Overseas) News": ["world news", "international", "global", "foreign", "un", "diplomacy", "overseas"],
    "Latest Tech News": ["technology", "tech", "ai", "artificial intelligence", "software", "innovation", "cyber", "hardware"],
    "Unique & Innovative Gadget Reviews": ["gadget", "review", "smartphone", "laptop", "wearable", "iot", "device", "unboxing"]
}

SOURCES = [
    # --- International & High Quality ---
    "https://www.theguardian.com/world/rss",
    "https://rss.nytimes.com/services/xml/rss/nyt/World.xml",
    "https://feeds.bbci.co.uk/news/world/rss.xml",
    "https://www.aljazeera.com/xml/rss/all.xml",
    "https://www.reutersagency.com/feed/?taxonomy=best-topics&post_type=best",
    
    # --- Education & Scholarships ---
    "https://www.theguardian.com/education/rss",
    "https://www.usnews.com/rss/education",
    "https://www.timeshighereducation.com/rss",
    "https://scholarship-positions.com/feed/",
    "https://www.scholars4dev.com/feed/",
    "https://www.ed.gov/feed",
    "https://www.scholarships.com/rss/news",
    
    # --- Tech & Gadgets ---
    "https://techcrunch.com/feed/",
    "https://www.theverge.com/rss/index.xml",
    "https://www.wired.com/feed/rss",
    "https://www.engadget.com/rss.xml",
    "https://www.cnet.com/rss/news/",
    "https://www.mashable.com/feeds/rss/all",
    "https://feeds.feedburner.com/arstechnica/index",
    
    # --- General High Quality ---
    "https://feeds.npr.org/1001/rss.xml",
    "https://www.bloomberg.com/feed/podcast/bloomberg-news.xml"
]

MAX_ITEMS = 15
INTERVAL_MINUTES = 60
