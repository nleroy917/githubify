from dotenv import load_dotenv
import os

load_dotenv()
DB_URL = os.environ.get("DB_URL")

# clean the DB_URL since SQLAlchemy doesnt like the
# format given by Heroku
DB_URL = DB_URL.replace('postgres', 'postgresql')
print('------> DB_URL cleaned', flush=True)
print('------> New DB_URL: {}'.format(DB_URL))

from flask import Flask, render_template, request, jsonify
from db.models import Tokens, Spotify
from db.config import db
app = Flask(__name__, static_folder="client/build/static", template_folder="client/build")
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db.init_app(app)

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
        
        # update access token
        access_token = Tokens.query.get(1) # the access token ID
        access_token.value = data['access_token']
        db.session.commit()
        db.session.refresh(access_token)
        
        # update refresh token
        refresh_token = Tokens.query.get(2) # the refresh token ID
        refresh_token.value = data['refresh_token']
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