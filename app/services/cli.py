import os, sys
import subprocess
from app.utils.decorator import cli_decorator, global_exception_handler
from app.services.manage_files import organize_push_files, organize_pull_files
import shutil
from app.utils.constants import logger
import socket
import uuid    

class CLI():
    def __init__(self, local_dir, branch_name, user):
        self.local_dir = local_dir
        self.user_email = user.email
        self.user_name = user.name
        self.branch_name = branch_name
        pass

    def backup(self, local_dir_id, remote_url):
        self.remote_url = remote_url
        self.chunk_dirs = organize_push_files(dir_path=self.local_dir, folder_id=local_dir_id)
        self.init_git()
        self.add_remote()
        self.create_branch()
        self.add()
        self.commit()
        if self.chunk_dirs not in [None, [], '', False]:
            self.delete_chunk()
        self.push()
        self.add()
        self.commit()
    
    @cli_decorator
    def init_git(self):
        # initialize git
        subprocess.run(
            ['git', 'init'], 
            cwd=self.local_dir, 
            check=True, 
            capture_output=True, 
            text=True
        )

        # configure the user
        subprocess.run(
            ['git', 'config', '--global', 'user.email', self.user_email], 
            cwd=self.local_dir, 
            check=True, 
            capture_output=True, 
            text=True
        )
        
        subprocess.run(
            ['git', 'config', '--global', 'user.name', self.user_name], 
            cwd=self.local_dir, 
            check=True, 
            capture_output=True, 
            text=True
        )
    
    @cli_decorator
    def add_remote(self):
        USERNAME = os.getenv('GITHUB_USER')
        PAT = os.getenv('GITHUB_TOKEN')
        EMAIL = os.getenv('GITHUB_EMAIL')
        replacement = f"://{USERNAME}:{PAT}@"
        url = self.remote_url.replace("://", replacement)
        result = subprocess.run(
            ['git', 'remote', '-v'], 
            cwd=self.local_dir, 
            capture_output=True,
            check=True, 
            text=True
        )
        if url not in result.stdout.strip():
            return subprocess.run(
                ['git', 'remote', 'add', 'origin', url], 
                cwd=self.local_dir, 
                capture_output=True, 
                check=True, 
                text=True
            ).stdout.strip()  
    
    @cli_decorator
    def create_branch(self):
        # check if branch exists
        result = subprocess.run(
            ['git', 'branch', '--list', self.branch_name], 
            cwd=self.local_dir, 
            capture_output=True, 
            check=True, 
            text=True
        )
        if self.branch_name not in result.stdout:    
            return subprocess.run(
                ['git', 'checkout', '-b', self.branch_name], 
                cwd=self.local_dir, 
                capture_output=True, 
                check=True
            ).stdout.strip()
    
    @cli_decorator
    def add(self):
        return subprocess.run(
            ['git', 'add', '.'], 
            cwd=self.local_dir, 
            capture_output=True, 
            check=True, 
            text=True
        ).stdout.strip()
    
    @cli_decorator
    def commit(self):
        message=f"successful backup-{uuid.uuid4()}"
        return subprocess.run(
            ['git', 'commit', '-m', message], 
            cwd=self.local_dir, 
            capture_output=True, 
            check=True, 
            text=True
        ).stdout.strip()
    
    def delete_chunk(self):
        for dir in self.chunk_dirs:
            if os.path.exists(dir):
                shutil.rmtree(dir)
                logger.info(f"successfully Deleted {dir}")

    def is_connected(self):
        try:
            # Perform a DNS lookup to check for internet connectivity
            socket.gethostbyname("www.google.com")
            return True
        except socket.error:
            return False
    @global_exception_handler
    def is_git_installed():
            # Execute the 'git --version' command
            result = subprocess.run(['git', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            # Check if the command was successful
            if result.returncode == 0:
                logger.info(f"Git is installed: {result.stdout.strip()}")
                return True
            else:
                raise FileNotFoundError("Git is not installed or not added to the system PATH.")
    
    @cli_decorator
    def push(self):
        """Push to git if there is internet connectivity"""
        if self.is_connected():
            return subprocess.run(
                ['git', 'push', 'origin', self.branch_name], 
                cwd=self.local_dir, 
                capture_output=True, 
                check=True, 
                text=True
            ).stdout.strip()
        else:
            raise Exception("no internet connection found, push failed")

    @cli_decorator
    def pull(self, remote_url = None):
        self.init_git()
        if remote_url not in [None, '', False, []]:
            self.remote_url = remote_url
            self.add_remote()
            self.create_branch()    
    
        if self.is_connected():
            result = subprocess.run(
                ['git', 'pull', 'origin', self.branch_name], 
                cwd=self.local_dir, 
                capture_output=True, 
                check=True, 
                text=True
            )
            
            self.chunk_dirs = organize_pull_files(self.local_dir)
            if self.chunk_dirs not in [None, [], '', False]:
                self.delete_chunk()
            logger.info("Pull operation successful")
            return True
        else:
            raise Exception("no internet connection found, pull failed")
        
    # push to remote branch if there is internet connection available