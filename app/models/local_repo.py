from sqlalchemy import Column, Integer, String, Text, ARRAY, DateTime, Enum, ForeignKey, UniqueConstraint
from app.config.database import Base
from sqlalchemy.orm import relationship
from datetime import datetime
from enum import Enum as PyEnum
from app.models.file import File

class BackupStatus(PyEnum):
    """Enum types for backup status"""
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    READY = "ready"

class LocalRepo(Base):
    """LocalRepo model"""
    __tablename__ = "localRepos"
    
    """table attributes"""
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    branch_id = Column(Integer, ForeignKey("branches.id"), nullable=False, index=True)
    backup_frequency = Column(String, nullable=False, index=True, default="24h")
    backup_status = Column(Enum(BackupStatus), nullable=False, index=True, default=BackupStatus.READY)
    backup_time = Column(DateTime, nullable=False, index=True, default=datetime.utcnow)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    
    """parent-child relationship with the File"""
    files = relationship("File", backref="folder")
    
    __table_args__ = (UniqueConstraint("name", "user_id", name="unq_user_repo"),)
    
    """Method to be implemented"""
    def __repr__(self):
        """Return a string representation of the localRepo class"""
        return f"LocalRepo(localRepo_name = {self.name}, localRepo_frequency = {self.backup_frequency}\n"

