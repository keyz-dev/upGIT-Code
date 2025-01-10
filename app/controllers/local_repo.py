from app.models.local_repo import LocalRepo as local_repo_model
from app.crud import local_repo as local_repo_crud
from app.utils.constants import logger
from app.utils.decorator import global_exception_handler

@global_exception_handler
def save(local_repo_object):
    local_repo = local_repo_model(**local_repo_object)
    saved_repo = local_repo_crud.create(local_repo=local_repo)
    logger.info("Successfully created local_repo")
    return saved_repo


@global_exception_handler
def get_all(limit = None, skip:int = 0):
    local_repos = local_repo_crud.get_all(limit=limit,skip=skip)
    logger.info(f"All local_repos: {local_repos}")
    return local_repos

@global_exception_handler        
def get(id):
    local_repo = local_repo_crud.get_local_repo(id=id)
    logger.info(f"Successfully retrieved {local_repo}")
    return local_repo

@global_exception_handler
def get_specific(column: str, value, limit = None, skip : int = 0):
    local_repos = local_repo_crud.get_by_column(field=column, value=value, limit=limit, skip = skip)
    logger.info(f"Successfully retrieved local_repos with {local_repos}")
    return local_repos

@global_exception_handler
def get_conditional(condition, limit = None, skip : int = 0):
    local_repos = local_repo_crud.get_by_condition(condition=condition, limit=limit, skip = skip)
    logger.info(f"Successfully retrieved local_repos with {local_repos}")
    return local_repos

@global_exception_handler   
def update(id, data):
    update_obj = local_repo_model(**data)
    if update_obj is None:
        raise Exception("Invalid data")
    updated = local_repo_crud.update(id=id, local_repo=data)
    logger.info(f"Successfully updated local_repo with id {id}")
    return updated

@global_exception_handler    
def delete_local_repo(id):
    deleted = local_repo_crud.delete(local_repo_id=id)
    logger.info(f"Successfully deleted local_repo with id {id}")
    return deleted