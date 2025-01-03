from sqlalchemy import select
from sqlalchemy.orm import Session
from ..models.remote_repo import RemoteRepo
from ..utils.decorator import transaction_decorator

@transaction_decorator
def create(session, remote_repo: RemoteRepo):
    """Create a new remote_repo in the database"""
    session.add(remote_repo)
    return remote_repo

@transaction_decorator
def get_all(session, limit = None, skip: int = 0):
    """Get all remote_repos from the database"""
    result = session.query(RemoteRepo).offset(skip).limit(limit).all()
    return result

@transaction_decorator
def get_remote_repo(session, id: int):
    """Get the remote_repos by the given id"""
    result = session.query(RemoteRepo).filter_by(id = id).one_or_none()
    return result

@transaction_decorator
def get_by_column(session, field:str, value, skip:int=0, limit = None):
    filter_column = getattr(RemoteRepo, field)
    condition = filter_column.ilike(value)
    if limit == 1:
        return session.query(RemoteRepo).filter(condition).first()
    result = session.query(RemoteRepo).filter(condition).limit(limit).offset(skip).all()
    return result

@transaction_decorator
def get_by_condition(session, condition = [], limit = None, skip:int=0):
    if condition not in [None, []]:
        if limit == 1:
            return session.query(RemoteRepo).filter(*condition).first()
        return session.query(RemoteRepo).filter(*condition).limit(limit).offset(skip).all()
    else:
        raise Exception("Condition not provided")

@transaction_decorator
def delete(session, remote_repo_id: int):
    remote_repo_to_delete = session.query(RemoteRepo).filter_by(id=remote_repo_id).one_or_none()
    if remote_repo_to_delete:
        session.delete(remote_repo_to_delete)   
        return remote_repo_to_delete
    else:
        raise Exception(f"Couldn't find remote_repo with id {remote_repo_id}")
                    