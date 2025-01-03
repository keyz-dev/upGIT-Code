from sqlalchemy import Column, Integer, String, Text, ARRAY, DateTime, Enum, ForeignKey
from ..config.database import Base
from sqlalchemy.orm import relationship
from datetime import datetime
from .branch import Branch

class RemoteRepo(Base):
    """RemoteRepo model"""
    
    __tablename__ = "remoteRepos"
    
    """table attributes"""
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    url = Column(String, nullable=False, index=True)
    clone_url = Column(String, nullable=False, index=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    """Parent-child relationship with the branches"""
    branches = relationship("Branch", backref="parent_repo")
    
    """Method to be implemented"""
    def __repr__(self):
        """Return a string representation of the remoteRepo class"""
        return f"RemoteRepo(remoteRepo_name = {self.name}, remoteRepo_url = {self.url}\n"

