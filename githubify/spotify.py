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
        self._refreshed = False
        # case where an access_token is passed directly in (first
        # authentication, specific use cases maybe)
        if access_token:
            print("Authenticating Spotify with access token")
            self._spotify = spotipy.Spotify(auth=access_token)
            try:
                # try to ge the user's data with
                # the current access token -> 
                # if the request fails,
                # fall back on the refresh token since
                # the access token might be expired
                result = self._spotify.current_user()
            except Exception as e:
                self._refreshed = True
                print('Access token failed. Reason: {}'.format(e))
                print("Authenticating Spotify with refresh token")
                auth = SpotifyOAuth(
                    client_id=os.environ.get("SPOTIFY_CLIENT_ID"),
                    client_secret=os.environ.get("SPOTIFY_CLIENT_SECRET"),
                    redirect_uri=os.environ.get("SPOTIFY_REDIRECT_URI")
                )
                tokens = auth.refresh_access_token(refresh_token)
                self._spotify = spotipy.Spotify(auth=tokens['access_token'])
                self._access_token = tokens['access_token']
                self._refresh_token = tokens['refresh_token']
                
        elif refresh_token:
            print("Authenticating Spotify with refresh token")
            auth = SpotifyOAuth(
                client_id=os.environ.get("SPOTIFY_CLIENT_ID"),
                client_secret=os.environ.get("SPOTIFY_CLIENT_SECRET"),
                redirect_uri=os.environ.get("SPOTIFY_REDIRECT_URI")
            )
            tokens = auth.refresh_access_token(refresh_token)
            self._spotify = spotipy.Spotify(auth=tokens['access_token'])
            self._access_token = tokens['access_token']
            self._refresh_token = tokens['refresh_token']
        
    def current_song(self):
        return self._spotify.current_playback()
    
    def uri_to_track_and_artist(self, uri):
        track = self._spotify.track(uri)
        return (
            track['name'] + ' -- ' + track['artists'][0]['name']
        )
