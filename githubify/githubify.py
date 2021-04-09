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
        return content[0:content.find("🟢")]
    
    def _current_song_change(self):
        pass
        
    
    def update_bio(self, message): 
        user = self._g.get_user()
        cleaned_bio = self._remove_listening_to(user.bio)
        
        print(cleaned_bio)
        
        new_bio = cleaned_bio + message
        
        user.edit(
            bio=new_bio
        )
        print("success")

        