from sqlalchemy import select
from app.models.file import File
from app.utils.decorator import transaction_decorator

@transaction_decorator
def create(session, file: File):
    """Create a new file in the database"""
    session.add(file)
    return file

@transaction_decorator
def get_all(session, limit = None, skip: int = 0):
    """Get all files from the database"""
    result = session.query(File).limit(limit).offset(skip).all()
    return result

@transaction_decorator
def get_file(session, id: int):
    """Get the files by the given id"""
    result = session.query(File).filter_by(id = id).one_or_none()
    return result

@transaction_decorator
def get_by_column(session, field:str, value, skip:int=0, limit = None):
    filter_column = getattr(File, field)
    condition = filter_column.ilike(value)
    if limit == 1:
        return session.query(File).filter(condition).first()
    return session.query(File).filter(condition).limit(limit).offset(skip).all()

@transaction_decorator
def get_by_condition(session, condition = [], limit = None, skip:int=0):
    if condition not in [None, []]:
        if limit == 1:
            return session.query(File).filter(*condition).first()
        return session.query(File).filter(*condition).limit(limit).offset(skip).all()
    else:
        raise Exception("Condition not provided")

@transaction_decorator
def delete(session, file_id: int):
    file_to_delete = session.query(File).filter_by(id=file_id).one_or_none()
    if file_to_delete:
        session.delete(file_to_delete)
        return file_to_delete
    else:
        raise Exception(f"Couldn't find file with id {file_id}")
                    