import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

class Spotify():
    """
    Class to interface the spotify api
    """
    # loads the environment from a .env file
    from dotenv import load_dotenv
    load_dotenv()
    
    def __init__(self, access_token=None, refresh_token=None):
        # case where an access_token is passed directly in (first
        # authentication, specific use cases maybe)
        if access_token:
            print("Authenticating Spotify with access token")
            self._spotify = spotipy.Spotify(auth=access_token)
            self._access_token = access_token
            self._refresh_token = None

        # typical use - refresh_token taken from a database and used to create
        # a new access_token
        elif refresh_token:
            print("Authenticating Spotify with refresh token")
            auth = SpotifyOAuth(
                client_id=os.environ.get("SPOTIFY_CLIENT_ID"),
                client_secret=os.environ.get("SPOTIFY_CLIENT_SECRET"),
            )
            tokens = auth.refresh_access_token(refresh_token)
            self._spotify = spotipy.Spotify(auth=tokens['access_token'])
            self._access_token = tokens['access_token']
            self._refresh_token = tokens['refresh_token']
        
    def current_song(self):
        return self._spotify.current_playback()
