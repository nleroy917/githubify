from githubify.githubify import GithubifyBot
from dotenv import load_dotenv
import os
import random

load_dotenv()
DB_URL = os.environ.get("DB_URL")

from flask import Flask, render_template, request, jsonify
from db.models import Settings
from db.config import db
app = Flask(__name__, static_folder="client/build/static", template_folder="client/build")
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db.init_app(app)

def update_bio():
    bot = GithubifyBot(os.environ.get("GITHUB_ACCESS_TOKEN"))
    bot.update_bio("🟢 Listening to: Song -- Artist {}".format(random.randint(0,10)))
    del bot

# background worker
from apscheduler.schedulers.background import BackgroundScheduler
scheduler = BackgroundScheduler()
scheduler.add_job(func=update_bio, trigger="interval", seconds=6000)
scheduler.start()

@app.route("/")
def base():
    return render_template('index.html')

@app.route("/settings", methods=['GET', 'POST'])
def settings():
    if request.method == 'GET':
        results = Settings.query.all()
        settings = {}
        for row in results:
            settings[row.setting] = row.value
        return jsonify({
            "items": settings
        })
    
    if request.method == 'POST':
        # get the data from the UI
        data = request.get_json()['data']
        
        # update access token
        access_token = Settings.query.get(1) # the access token ID
        access_token.value = data['access_token']
        db.session.commit()
        db.session.refresh(access_token)
        
        # update refresh token
        refresh_token = Settings.query.get(2) # the refresh token ID
        refresh_token.value = data['refresh_token']
        db.session.commit()
        db.session.refresh(refresh_token)
        
        return jsonify({
            "message": "success"
        })
        
        

if __name__ == '__main__':
    app.run()