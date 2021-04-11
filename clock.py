from time import sleep
from githubify.githubify import GithubifyBot
from db.models import Tokens, Spotify
import os
from dotenv import load_dotenv

# Env variables
load_dotenv()
DB_URL = os.getenv('DB_URL').replace('postgres', 'postgresql')
from db.driver import Driver

dbdriver = Driver(DB_URL)

def cycle():
    sp_at = dbdriver.get_access_token(Tokens)
    sp_rt = dbdriver.get_refresh_token(Tokens)
    
    most_recent_song_uri = dbdriver.get_most_recent_song_URI(Spotify)
    
    bot = GithubifyBot(
        os.environ.get("GITHUB_ACCESS_TOKEN"), 
        sp_access_token=sp_at,
        sp_refresh_token=sp_rt
    )
    if bot._sp._refreshed:
        print('------> Refreshed tokens')
        dbdriver.update_tokens(
            Tokens,
            bot._sp._access_token,
            bot._sp._refresh_token
        )
    
    try:
        current_track = bot.get_current_song()
    except AttributeError:
        print('------> Make sure to visit your app and authorize Spotify!')
    
    if current_track is not None:
        print('------> Listening to: ', bot._sp.uri_to_track_and_artist(current_track['item']['uri']))
        
        if current_track['item']['uri'] == most_recent_song_uri:
            print('------> No song change')
        else:
            dbdriver.update_most_recent_song(Spotify, current_track['item']['uri'])
            print('------> Song change... updating bio.')
            
            # update bio here with githubify bot
            bot.update_bio(current_track)
    else:
        print('------> No song playing')
    
    print('\n')

# background worker
from apscheduler.schedulers.background import BlockingScheduler
scheduler = BlockingScheduler()
scheduler.add_job(func=cycle, trigger="interval", seconds=5)

if __name__ == '__main__':
    try:
        scheduler.start()
    except KeyboardInterrupt:
        print('------> Goodbye!')