from sqlalchemy import select
from app.models.local_repo import LocalRepo
from app.utils.decorator import transaction_decorator

@transaction_decorator
def create(session, local_repo: LocalRepo):
    """Create a new local_repo in the database"""
    session.add(local_repo)
    return local_repo

@transaction_decorator
def get_all(session, limit = None, skip: int = 0):
    """Get all local_repos from the database"""
    result = session.query(LocalRepo).offset(skip).limit(limit).all()
    return result

@transaction_decorator
def get_local_repo(session, id: int):
    """Get the local_repos by the given id"""
    result = session.query(LocalRepo).filter_by(id = id).one_or_none()
    return result

@transaction_decorator
def get_by_column(session, field:str, value, skip:int=0, limit = None):
    filter_column = getattr(LocalRepo, field)
    condition = filter_column.ilike(value)
    if limit == 1:
        return session.query(LocalRepo).filter(condition).first()
    return session.query(LocalRepo).filter(condition).limit(limit).offset(skip).all()

@transaction_decorator
def get_by_condition(session, condition = [], limit = None, skip:int=0):
    if condition not in [None, []]:
        if limit == 1:
            return session.query(LocalRepo).filter(*condition).first()
        return session.query(LocalRepo).filter(*condition).limit(limit).offset(skip).all()
    else:
        raise Exception("Condition not provided")

@transaction_decorator
def update(session, id: int, local_repo):
    local_repo_to_update = session.query(LocalRepo).filter_by(id=id).one_or_none()
    if local_repo_to_update:
        for key, value in local_repo.items():
            if value is not None:
                setattr(local_repo_to_update, key, value)
        return local_repo_to_update
    else:
        raise Exception(f"Couldn't find local_repo with id {id}")

@transaction_decorator
def delete(session, local_repo_id: int):
    local_repo_to_delete = session.query(LocalRepo).filter_by(id=local_repo_id).one_or_none()
    if local_repo_to_delete:
        session.delete(local_repo_to_delete)
        return local_repo_to_delete
    else:
        raise Exception(f"Couldn't find local_repo with id {local_repo_id}")
                    