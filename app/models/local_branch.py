from sqlalchemy import Column, Integer, DateTime, ForeignKey, UniqueConstraint
from app.config.database import Base
from datetime import datetime

class LocalBranch(Base):
    """LocalBranch model"""
    
    __tablename__ = "local_branches"
    
    """table attributes"""
    id = Column(Integer, primary_key=True, index=True)
    repo_id = Column(Integer, ForeignKey("localRepos.id"), nullable=False, index=True)
    branch_id = Column(Integer, ForeignKey("branches.id"), nullable=False, index=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    __table_args__ = (UniqueConstraint('repo_id', 'branch_id', name='unique_repo_branch'),)
    
    """Method to be implemented"""
    def __repr__(self):
        """Return a string representation of the local_branch class"""
        return f"LocalBranch(id= {self.id}, repo_id= {self.repo_id}, branch_id= {self.branch_id}\n"

