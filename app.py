from dotenv import load_dotenv
import os
from apscheduler.schedulers.background import BackgroundScheduler
from clock import *

load_dotenv()
DB_URL = "sqlite:///data.db"

from flask import Flask, render_template, request, jsonify
from db.models import Tokens, Spotify
from db.config import db
app = Flask(__name__, static_folder="client/build/static", template_folder="client/build")
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db.init_app(app)

# create all tables if
# not exist
with app.app_context():
    db.create_all()
    
# init schedular
scheduler = BackgroundScheduler()
scheduler.add_job(func=cycle, trigger="interval", seconds=5)
scheduler.start()

@app.route("/")
def base():
    return render_template('index.html')

@app.route("/tokens", methods=['GET', 'POST'])
def tokens():
    
    #
    # Check authentication
    #
    if request.headers.get('Auth') != os.environ.get('INTERNAL_TOKEN'):
        return jsonify({
            "message": "Invalid auth token."
        }), 401
    
    
    if request.method == 'GET':
        results = Tokens.query.all()
        tokens = {}
        
        for row in results:
            tokens[row.token] = row.value

        return jsonify({
            "tokens": tokens
        })
    
    if request.method == 'POST':
        # get the data from the UI
        data = request.get_json()['data']
        
        # update access token if exists
        # else create it
        access_token = Tokens.query.get(1) # the access token ID
        if access_token is not None:
            access_token.value = data['access_token']
        else:
            access_token = Tokens(
                token='SPOTIFY_ACCESS_TOKEN',
                value=data['access_token']
            )
            db.session.add(access_token)
            
        db.session.commit()
        db.session.refresh(access_token)
        
        # update refresh token if exists,
        # else create it
        refresh_token = Tokens.query.get(2) # the refresh token ID
        if refresh_token is not None:
            refresh_token.value = data['refresh_token']
        else:
            refresh_token = Tokens(
                token='SPOTIFY_REFRESH_TOKEN',
                value=data['refresh_token']
            )
            db.session.add(refresh_token)
        db.session.commit()
        db.session.refresh(refresh_token)
        
        return jsonify({
            "message": "success"
        })
        
@app.route('/spotify', methods=['GET'])
def spotify():
    if request.method == 'GET':
        results = Spotify.query.all()
        settings = {}
        
        for row in results:
            settings[row.setting] = row.value
        
        return jsonify({
            "settings": settings
        })

if __name__ == '__main__':
    app.run()