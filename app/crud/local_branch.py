from sqlalchemy import select
from app.models.local_branch import LocalBranch
from app.utils.decorator import transaction_decorator

@transaction_decorator
def create(session, local_branch: LocalBranch):
    """Create a new local_branch in the database"""
    session.add(local_branch)
    return local_branch

@transaction_decorator
def get_all(session, limit = None, skip: int = 0):
    """Get all local_branchs from the database"""
    result = session.query(LocalBranch).limit(limit).offset(skip).all()
    return result

@transaction_decorator
def get_local_branch(session, id: int):
    """Get the local_branchs by the given id"""
    result = session.query(LocalBranch).filter_by(id = id).one_or_none()
    return result

@transaction_decorator
def get_by_column(session, field:str, value, skip:int=0, limit = None):
    filter_column = getattr(LocalBranch, field)
    condition = filter_column.ilike(value)
    if limit == 1:
        return session.query(LocalBranch).filter(condition).first()
    return session.query(LocalBranch).filter(condition).limit(limit).offset(skip).all()

@transaction_decorator
def get_by_condition(session, condition = [], limit = None, skip:int=0):
    if condition not in [None, []]:
        if limit == 1:
            return session.query(LocalBranch).filter(*condition).first()
        return session.query(LocalBranch).filter(*condition).limit(limit).offset(skip).all()
    else:
        raise Exception("Condition not provided")

@transaction_decorator
def delete(session, local_branch_id: int):
    local_branch_to_delete = session.query(LocalBranch).filter_by(id=local_branch_id).one_or_none()
    if local_branch_to_delete:
        session.delete(local_branch_to_delete)
        return local_branch_to_delete
    else:
        raise Exception(f"Couldn't find local_branch with id {local_branch_id}")
                    