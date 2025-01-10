from app.models.file import File as file_model
from app.crud import file as file_crud
from app.utils.constants import logger

def save(file_object):
    file = file_model(**file_object)
    try:
        saved_repo = file_crud.create(file=file)
        logger.info("Successfully created file")
        return saved_repo
    except Exception as e:
        logger.error("Failed to create file: %s" % e)
        return False

def get_all(limit = None, skip:int = 0):
    try:
        files = file_crud.get_all(limit=limit,skip=skip)
        logger.info(f"All files: {files}")
        return files
    except Exception as e:
        logger.error("Failed to get files: %s" % e)
        return False
        
def get(id: int):
    try:
        file = file_crud.get_file(id=id)
        logger.info(f"Successfully retrieved {file}")
        return file
    except Exception as e:
        logger.error("Failed to get files: %s" % e)
        return False

def get_specific(column: str, value, limit = None, skip : int = 0):
    try:
        files = file_crud.get_by_column(field=column, value=value, limit=limit, skip = skip)
        logger.info(f"Successfully retrieved files with {files}")
        return files
    except Exception as e:
        logger.error("Failed to get files: %s" % e)
        return False
 
def get_conditional(condition, limit=None, skip : int = 0):
    try:
        local_repos = file_crud.get_by_condition(condition=condition, limit=limit, skip=skip)
        logger.info(f"Successfully retrieved local_repos with {local_repos}")
        return local_repos
    except Exception as e:
        logger.error("Failed to get local_repos: %s" % e)
        return False 
def delete_file(id: int):
    try:
        deleted = file_crud.delete(file_id=id)
        logger.info(f"Successfully deleted file with id {id}")
        return deleted
    except Exception as e:
        logger.error("Failed to delete file: %s" % e)
        return False