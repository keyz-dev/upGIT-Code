from github import Auth, Github
import os
from dotenv import load_dotenv

load_dotenv()
class GithubUtililty():
    def __init__(self):
        PAT = os.getenv('GITHUB_TOKEN')
        auth = Auth.Token(PAT)
        gh = Github(auth=auth)
        self.user = gh.get_user()
    
    def create_repo(self, repo_name, repo_description="This is an initial user repository created via upGIT", private=True):
        repo = self.user.create_repo(
            name = repo_name, 
            description = repo_description, 
            private=private
        )
        return repo
    
    def get_repo(self, repo_name = None):
        for repo in self.user.get_repos():
            print(repo)
    
    def delete_repo(self, repo_name):
        pass