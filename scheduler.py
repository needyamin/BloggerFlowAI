import schedule
import time
from blogger_post import auto_post

schedule.every().day.at("09:00").do(auto_post)

print("Scheduler started. Posts will be published daily at 9:00 AM")
while True:
    schedule.run_pending()
    time.sleep(60)

