from ..schema.user import UserUpdate
from ..crud import user as user_crud
from ..utils.constants import logger
        
def get_all(limit = None, skip:int = 0):
    try:
        users = user_crud.get_all(limit=limit,skip=skip)
        logger.info(f"All users: {users}")
        return users
    except Exception as e:
        logger.error("Failed to get users: %s" % e)
        return False
        
def get(id):
    try:
        user = user_crud.get_user(id=id)
        logger.info(f"Successfully retrieved {user}")
        return user
    except Exception as e:
        logger.error("Failed to get users: %s" % e)
        return False

def get_specific(column: str, value, limit = None, skip : int = 0):
    try:
        users = user_crud.get_by_column(field=column, value=value)
        logger.info(f"Successfully retrieved users with {users}")
        return users
    except Exception as e:
        logger.error("Failed to get users: %s" % e)
        return False

def get_conditional(condition, limit = None, skip : int = 0):
    try:
        local_repos = user_crud.get_by_condition(condition=condition, limit=limit, skip=skip)
        logger.info(f"Successfully retrieved local_repos with {local_repos}")
        return local_repos
    except Exception as e:
        logger.error("Failed to get local_repos: %s" % e)
        return False
    
def update_user(id: int, user_object):
    try:
        """trim the object of empty fields"""
        user_object = {key : value for key, value in user_object.items() if value not in [None, '', []] }
        user = UserUpdate(**user_object)
        updated_user = user_crud.update(user_id=id, user=user)
        logger.info(f"Successfully updated user with id {id}")
        return updated_user
    except Exception as e:
        logger.error("Failed to update user: %s" % e)
        return False
        
def delete_user(id):
    try:
        deleted = user_crud.delete(user_id=id)
        logger.info(f"Successfully deleted user with id {id}")
        return deleted
    except Exception as e:
        logger.error("Failed to delete user: %s" % e)
        return False