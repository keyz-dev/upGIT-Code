from sqlalchemy import Column, Integer, String, Text, ARRAY, DateTime, Enum, ForeignKey
from app.config.database import Base
from datetime import datetime
from sqlalchemy.orm import relationship
from app.models.local_branch import LocalBranch

class Branch(Base):
    """Branch model"""
    
    __tablename__ = "branches"
    
    """table attributes"""
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True, unique=True)
    remote_repo = Column(Integer, ForeignKey('remoteRepos.id'), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    """parent-child relationship with the local_branch"""
    repos = relationship("LocalBranch", backref="branch")
    
    def __repr__(self):
        """Return a string representation of the branch class"""
        return f"Branch(branch_name = {self.name}, branch_parent_repo = {self.remote_repo}\n"

