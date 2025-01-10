from sqlalchemy import select
from app.models.branch import Branch
from app.utils.decorator import transaction_decorator

@transaction_decorator
def create(session, branch: Branch):
    """Create a new branch in the database"""
    session.add(branch)
    return branch

@transaction_decorator
def get_all(session, limit = None, skip: int = 0):
    """Get all branchs from the database"""
    result = session.query(Branch).offset(skip).limit(limit).all()
    return result

@transaction_decorator
def get_branch(session, id: int):
    """Get the branchs by the given id"""
    result = session.query(Branch).filter_by(id = id).one_or_none()
    return result

@transaction_decorator
def get_by_column(session, field:str, value, skip:int=0, limit = None):
    filter_column = getattr(Branch, field)
    condition = filter_column.ilike(value)
    if limit == 1:
        return session.query(Branch).filter(condition).first()
    return session.query(Branch).filter(condition).offset(skip).limit(limit).all()

@transaction_decorator
def get_by_condition(session, condition = [], limit = None, skip:int=0):
    if condition not in [None, []]:
        if limit == 1:
            return session.query(Branch).filter(*condition).first()
        return session.query(Branch).filter(*condition).offset(skip).limit(limit).all()
    else:
        raise Exception("Condition not provided")

@transaction_decorator
def delete(session, branch_id: int):
    branch_to_delete = session.query(Branch).filter_by(id=branch_id).one_or_none()
    if branch_to_delete:
        session.delete(branch_to_delete)
        return branch_to_delete
    else:
        raise Exception(f"Couldn't find branch with id {branch_id}")
                    