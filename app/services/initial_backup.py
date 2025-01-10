from app.models.local_repo import LocalRepo
from app.schema.user import User
from app.controllers import (
    remote_repo as remote_repo_controller, 
    branch as branch_controller, 
    local_repo as local_repo_controller, 
    local_branch as local_branch_controller
)
from app.utils.decorator import global_exception_handler
import os, re
from datetime import datetime, timedelta
from app.services.cli import CLI
from app.utils.constants import logger

is_new_branch = False
is_new_folder = False

def check_branch(branch_name, repo_id):
    """Check if the branch exists"""
    global is_new_branch
    branch_name = branch_name.strip().replace(' ', '_')
    branch_exists = branch_controller.get_specific(column='name', value=branch_name, limit=1) 
    if branch_exists in [None, False, '', []]:
        """create the branch"""
        branch_object = {
            'name': branch_name.lower(),
            'remote_repo': repo_id
        } 
        created_branch = branch_controller.save(branch_object)  
        is_new_branch = True
        return created_branch    
    else:              
        return branch_exists
   
@global_exception_handler
def check_folder(backup_object, user_id):
    global is_new_folder
    if not os.path.isdir(backup_object['path']):
        raise Exception("Not a directory")
    
    frequency_reg = re.compile(r'^[1-9][0-9]*\s?[hHMmDd]$')
    freq = backup_object['backup_frequency'].strip()
    if frequency_reg.match(freq) is None:
        raise Exception('Invalid backup frequency. backup set to 24h')
    
    # Convert the backup frequency to h format
    if freq.lower().endswith('m'):
        time = re.findall(r'\d+', freq)
        time = int(time[0])/60
        freq = f'{round(time, 2)}h'
    elif freq.lower().endswith('d'):
        time = re.findall(r'\d+', freq)
        time = int(time[0])*24
        freq = f'{time}h'
    folder_object = {
        'name': backup_object['path'],
        'user_id': user_id,
        'backup_frequency': freq
    }
    condition = [LocalRepo.user_id == user_id, LocalRepo.name == backup_object['path']]
    created_folder = local_repo_controller.get_conditional(condition=condition, limit=1)
    if created_folder in [None, False, '', []]:
        created_folder = local_repo_controller.save(folder_object)
        is_new_folder = True
    
    return created_folder

@global_exception_handler
def handle_local_branch(repo_id, branch_id):
    global is_new_branch
    global is_new_folder
    
    local_branch_object = {
    'repo_id': repo_id,
    'branch_id': branch_id
    }
    if is_new_folder or is_new_branch:
        local_branch_controller.save(local_branch_object)
        
@global_exception_handler           
def new_backup(user : User, backup_object, repo):
    global is_new_branch
    global is_new_folder
    # get branch id
    branch_info = check_branch(backup_object['branch_name'], repo.id)
    created_folder = check_folder(backup_object, user.id)
    handle_local_branch(created_folder.id, branch_info.id)
    
    return backup(folder=created_folder, branch=branch_info, repo=repo)
    
@global_exception_handler
def backup(folder, branch, repo):
    cli = CLI(local_dir=folder.name, branch_name=branch.name)
    cli.backup(local_dir_id=folder.id, remote_url=repo.clone_url)
    
    """update the local_repo's backup status"""
    backup_hours = re.findall(r'\d+', folder.backup_frequency)
    backup_hours = int(backup_hours[0])
    next_backup_time = datetime.now() + timedelta(hours = backup_hours)
    local_repo_controller.update(folder.id, {'backup_status': 'COMPLETED', 'backup_time': next_backup_time})
    
    logger.info(f"Successfully backed up {folder.name} to {repo.name} at {datetime.now()}")
    
    return True