from github import Github
from .spotify import Spotify

class GithubifyBot:
    def __init__(self, gh_access_token, sp_access_token=None, sp_refresh_token=None):
        self._gh_access_token = gh_access_token
        self._sp_access_token = sp_access_token
        self._sp_refresh_token = sp_refresh_token
        self._g = Github(gh_access_token)
        self._sp = Spotify(
            access_token=sp_access_token, 
            refresh_token=sp_refresh_token
        )
        self._current_song = None
    
    def _remove_listening_to(self, content):
        return content[:content.find("🟢")]
    
    def get_current_song(self):
        return self._sp.current_song()
    
    def update_bio(self, current_track): 
        user = self._g.get_user()
        cleaned_bio = self._remove_listening_to(user.bio).rstrip() # remove whitespace that appears
        
        new_bio = cleaned_bio + " 🟢 Listening to: " + self._sp.uri_to_track_and_artist(current_track['item']['uri'])
        
        user.edit(
            bio=new_bio
        )

        