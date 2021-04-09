from githubify.githubify import GithubifyBot
from db.models import Settings
import os
from dotenv import load_dotenv

# Env variables
load_dotenv()
DB_URL = os.getenv('DATABASE_URL')
from db.driver import Driver

dbdriver = Driver(DB_URL)

def update_bio():
    bot = GithubifyBot(os.environ.get("GITHUB_ACCESS_TOKEN"))
    bot.update_bio("🟢 Listening to: Song -- Artist")
    del bot

# background worker
from apscheduler.schedulers.background import BackgroundScheduler
scheduler = BackgroundScheduler()
scheduler.add_job(func=update_bio, trigger="interval", seconds=6000)
scheduler.start()