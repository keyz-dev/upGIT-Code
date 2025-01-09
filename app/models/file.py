from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.config.database import Base

class File(Base):
    """File model"""
    __tablename__ = 'files'
    
    """table attributes"""
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, index=True)
    repo_id = Column(Integer, ForeignKey('localRepos.id'), nullable=False, index=True)
    filepath = Column(String, nullable=False, index=True)
    size = Column(Float)
    parent_id = Column(Integer, ForeignKey('files.id'), nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        """Return a string representation of the file class"""
        return f"File(file_name = {self.name}, file_parent = {self.repo_id}, file_size = {self.size}\n"