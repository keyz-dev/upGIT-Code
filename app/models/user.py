from sqlalchemy import Column, Integer, String, Text, ARRAY, DateTime, Enum, ForeignKey
from ..config.database import Base
from sqlalchemy.orm import relationship
from datetime import datetime
import bcrypt
from .remote_repo import RemoteRepo
from .local_repo import LocalRepo

class User(Base):
    """User model"""
    
    __tablename__ = "users"
    
    """table attributes"""
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    password = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    """one-to-one relationship with remote repository"""
    remote_repos = relationship("RemoteRepo", backref="owner", uselist=False)
    
    """parent-child relationship with local repository/uploaded folder"""
    local_repos = relationship("LocalRepo", backref="uploader")
    
    """Method to be implemented"""
    def set_password(self) -> str:
        salt = bcrypt.gensalt()
        self.password = self.password.encode('utf-8')
        self.password = bcrypt.hashpw(self.password, salt=salt)
        self.password = self.password.decode('utf-8')
        
    def check_password(self, plain_password: str) -> bool:
        return bcrypt.checkpw(plain_password.encode('utf-8'), self.password.encode('utf-8'))
    
    def __repr__(self):
        """Return a string representation of the user class"""
        return f"User(user_name = {self.name}, user_email = {self.email}, user_password = {self.password})\n"

