"""A decorator method to handle the exceptions that may occur durring the crud"""
import subprocess
from .constants import logger
from app.config.database import engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from functools import wraps #to maintain the function metadata when called

Session = sessionmaker(bind=engine)

def global_exception_handler(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            # Execute the function
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            logger.error(f"An error occurred running {func.__name__}: {e}")
            return None
    return wrapper

def transaction_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        """Create a db session"""
        session = Session()
        try:
            # Perform database transaction
            result = func(session, *args, **kwargs)
            
            # Commit the transaction if only there are changes to the database
            if session.dirty or session.new:
                session.commit()
                session.refresh(result)
            return result
        except SQLAlchemyError as e:
            session.rollback()
            logger.error(f"A database connection error occured: {e}")
            return None
        except Exception as e:
            session.rollback()
            logger.error(f"An unexpected error occurred during crud operation: {e}")
            return None
        finally:
            session.close()
            logger.info(f"Database session closed after {func.__name__}")
            
    return wrapper

def cli_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            # Execute the function
            result = func(*args, **kwargs)
            logger.info(f"successfully executed {func.__name__}")
            return result
        except subprocess.CalledProcessError as e:
            logger.error(f"A subprocess error occurred: {e.returncode}")
            logger.error(e)
            quit()
        except Exception as e:
            logger.error(f"An error occurred while running the CLI command: {e}")
            quit()
    return wrapper