import sys
from pathlib import Path
import os

# Add src to path
src_path = str(Path(__file__).resolve().parent.parent / "src")
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from models.custom_agent.bot import run_once
from app.post import auto_post

def test_full_workflow():
    print("--- Starting News Collection ---")
    news = run_once()
    
    if news:
        print(f"--- news Collection Complete ({len(news)} items) ---")
        print("--- Starting Blog Post Generation with News Context ---")
        auto_post(news_items=news)
    else:
        print("--- No news found on current topics. Posting regular article. ---")
        auto_post()

if __name__ == "__main__":
    test_full_workflow()
