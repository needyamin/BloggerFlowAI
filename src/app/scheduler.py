import schedule
import time
from .post import auto_post
from models.custom_agent.bot import run_once

def _job():
    news_items = run_once()
    auto_post(news_items=news_items)

schedule.every().day.at("09:00").do(_job)

def run():
    print("Scheduler started. News + posts daily at 9:00 AM")
    while True:
        schedule.run_pending()
        time.sleep(60)
