from sqlalchemy import Column, Integer, String, Text, ARRAY, DateTime, Enum, ForeignKey
from ..config.database import Base
from sqlalchemy.orm import relationship
from datetime import datetime
import bcrypt
import enum as PyEnum


class Repository_type(PyEnum):
    LOCAL = "local"
    REMOTE = "remote"
    
class Backup_status(PyEnum):
    BACKUP = "Backup"
    NOTBACKUP = "not cackup"
    IN_PROGRESS="in progress"

class Repo(Base):
    """Repo model"""
    
    __tablename__ = "repos"
    
    """table attributes"""
    repository_id = Column(Integer, primary_key=True, index=True)
    repository_name = Column(String, nullable=False, index=True)
    url = Column(String, nullable=False, index=True)
    repository_type = Column(Enum(Repository_type), nullable=False, index=True)
    backup_frequency = Column(String, nullable=False, index=True)
    remote_repo_id = Column(Integer,ForeignKey=True,nullable=False,index=True)
    backup_status = Column(Enum(Backup_status), nullable=False, index=True)
    user_id = Column(Integer,ForeignKey=True, nullable=False, index=True)
    
    
    