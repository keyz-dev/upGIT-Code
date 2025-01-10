import os
from app.controllers import (
    local_repo as local_repo_controller,
    remote_repo as remote_repo_controller,
    branch as branch_controller,
    local_branch as local_branch_controller
)
from app.models.local_repo import LocalRepo
from datetime import datetime
from app.services.initial_backup import backup

def get_repos_in_batches(user_id, limit: int):
    """Get the repos in batches"""
    skip_value = 0
    while True:
        # get the repos in batches
        condition = [LocalRepo.user_id == user_id, LocalRepo.backup_time < datetime.now()]
        batches = local_repo_controller.get_conditional(condition=condition, skip=skip_value, limit=limit)
        if batches in [None, False, [], '']:
            break
        skip_value += limit
        yield batches
 
def bg_backup():
    """Backup the repos"""
    with open(os.path.join(os.getcwd(),'app', 'auth', 'user_id.txt'), 'r') as f:
        user_id = f.read()
    
    user_id = int(user_id)
    for batches in get_repos_in_batches(user_id=user_id, limit=2):
        if batches in [None, False, [], '']:
            break
        for batch in batches:
            # get remote repo
            repo = remote_repo_controller.get_specific(column='user_id', value=user_id, limit=1)
            if repo in [None, False, '', []]:
                raise Exception("No remote repository found for this user with id,  %d" % user_id)
            
            # get branch
            branch = local_branch_controller.get_specific(column='repo_id', value=batch.id, limit=1)
            if branch in [None, False, '', []]:
                raise Exception("No local branch found for this repo with id,  %d" % batch.id)
            
            branch = branch_controller.get(branch.id)   
            if branch not in [None, False, '', []]:
                backup(folder = batch, repo = repo, branch = branch)

    