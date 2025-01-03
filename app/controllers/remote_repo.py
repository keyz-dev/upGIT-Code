from ..models.remote_repo import RemoteRepo as remote_repo_model
from ..crud import remote_repo as remote_repo_crud
from ..utils.constants import logger
        
def save(remote_repo_object):
    remote_repo = remote_repo_model(**remote_repo_object)
    try:
        saved_repo = remote_repo_crud.create(remote_repo=remote_repo)
        logger.info("Successfully created remote_repo")
        return saved_repo
    except Exception as e:
        logger.error("Failed to create remote_repo: %s" % e)
        return False

def get_all(limit = None, skip:int = 0):
    try:
        remote_repos = remote_repo_crud.get_all(limit=limit,skip=skip)
        logger.info(f"All remote_repos: {remote_repos}")
        return remote_repos
    except Exception as e:
        logger.error("Failed to get remote_repos: %s" % e)
        return False
        
def get(id: int):
    try:
        remote_repo = remote_repo_crud.get_remote_repo(id=id)
        logger.info(f"Successfully retrieved {remote_repo}")
        return remote_repo
    except Exception as e:
        logger.error("Failed to get remote_repos: %s" % e)
        return False

def get_specific(column: str, value, limit = None, skip : int = 0):
    try:
        remote_repos = remote_repo_crud.get_by_column(field=column, value=value, limit=limit, skip = skip)
        logger.info(f"Successfully retrieved remote_repos {remote_repos}")
        return remote_repos
    except Exception as e:
        logger.error("Failed to get remote_repos: %s" % e)
        return False

def get_conditional(condition, limit = None, skip : int = 0):
    try:
        local_repos = remote_repo_crud.get_by_condition(condition=condition, limit=limit, skip = skip)
        logger.info(f"Successfully retrieved local_repos with {local_repos}")
        return local_repos
    except Exception as e:
        logger.error("Failed to get local_repos: %s" % e)
        return False 
def delete_remote_repo(id):
    try:
        deleted = remote_repo_crud.delete(remote_repo_id=id)
        logger.info(f"Successfully deleted remote_repo with id {id}")
        return deleted
    except Exception as e:
        logger.error("Failed to delete remote_repo: %s" % e)
        return False