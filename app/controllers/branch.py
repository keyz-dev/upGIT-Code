from app.models.branch import Branch as branch_model
from app.crud import branch as branch_crud
from app.utils.constants import logger

def save(branch_object):
    branch = branch_model(**branch_object)
    try:
        saved_repo = branch_crud.create(branch=branch)
        logger.info("Successfully created branch")
        return saved_repo
    except Exception as e:
        logger.error("Failed to create branch: %s" % e)
        return False

def get_all(limit = None, skip:int = 0):
    try:
        branchs = branch_crud.get_all(limit=limit,skip=skip)
        logger.info(f"All branchs: {branchs}")
        return branchs
    except Exception as e:
        logger.error("Failed to get branchs: %s" % e)
        return False
        
def get(id: int):
    try:
        branch = branch_crud.get_branch(id=id)
        logger.info(f"Successfully retrieved {branch}")
        return branch
    except Exception as e:
        logger.error("Failed to get branchs: %s" % e)
        return False

def get_specific(column: str, value, limit = None, skip : int = 0):
    try:
        branchs = branch_crud.get_by_column(field=column, value=value, limit=limit, skip = skip)
        logger.info(f"Successfully retrieved branchs with {branchs}")
        return branchs
    except Exception as e:
        logger.error("Failed to get branchs: %s" % e)
        return False

def get_conditional(condition, limit=None, skip : int = 0):
    try:
        local_repos = branch_crud.get_by_condition(condition=condition, limit=limit, skip = skip)
        logger.info(f"Successfully retrieved local_repos with {local_repos}")
        return local_repos
    except Exception as e:
        logger.error("Failed to get local_repos: %s" % e)
        return False
def delete_branch(id: int):
    try:
        deleted = branch_crud.delete(branch_id=id)
        logger.info(f"Successfully deleted branch with id {id}")
        return deleted
    except Exception as e:
        logger.error("Failed to delete branch: %s" % e)
        return False