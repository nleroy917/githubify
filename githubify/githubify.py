from github import Github

class GithubifyBot:
    def __init__(self, access_token):
        self._access_token = access_token
        self._g = Github(access_token)
    
    def _remove_listening_to(self, content):
        return content[0:content.find("🟢")]
        
    
    def update_bio(self, message):
        user = self._g.get_user()
        cleaned_bio = self._remove_listening_to(user.bio)
        
        print(cleaned_bio)
        
        new_bio = cleaned_bio + message
        
        user.edit(
            bio=new_bio
        )
        print("success")

        