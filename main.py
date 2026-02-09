import sys
import os
from pathlib import Path

# Add src to python path so we can import modules normally
src_path = str(Path(__file__).resolve().parent / "src")
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from config import RUN_MODE

if __name__ == '__main__':
    if RUN_MODE == "direct":
        from models.custom_agent.bot import run_once
        from app.post import auto_post
        print("[+] Collecting authentic news context...")
        news_items = run_once()
        auto_post(news_items=news_items)
    else:
        from app.scheduler import run
        run()

