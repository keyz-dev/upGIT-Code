from app.services.cli import CLI
from app.controllers import (
    local_repo as local_repo_controller,
    branch as branch_controller
)
from app.models.local_repo import LocalRepo

def pull(user_id, local_repo_id, branch_id):
    """Pulls the latest changes from the remote repository."""
    condition = [LocalRepo.user_id == user_id, LocalRepo.id == local_repo_id]
    local_repo = local_repo_controller.get_conditional(condition=condition, limit=1)
    if local_repo in [None, False, '', []]:
        return
    """Get branch information"""
    branch = branch_controller.get(branch_id)
    if branch in [None, False, '', []]:
        return
    """Pull the latest changes"""
    
    cli = CLI(local_dir=local_repo.name, branch_name=branch.name)
    cli.pull()