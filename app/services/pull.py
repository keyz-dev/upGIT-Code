import os, sys
from app.services.cli import CLI
from app.controllers import (
    local_repo as local_repo_controller,
    branch as branch_controller
)
from app.models.local_repo import LocalRepo

def pull(remote_url, local_dir, branch_name):
    """Pulls the latest changes from the remote repository."""
    
    os.makedirs(local_dir, exist_ok=True)
    cli = CLI(local_dir=local_dir, branch_name=branch_name)
    return cli.pull(remote_url)