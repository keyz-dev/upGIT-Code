from pydantic import BaseModel, Field, EmailStr, validator
from datetime import datetime
from typing import Optional

class BaseUser(BaseModel):
    """
    '...' means that the field is obligatory
    """
    name: str = Field(..., max_length=50, example='test')
    email: EmailStr = Field(..., example='test@example.com')
    password: str = Field(..., min_length=5, min_digits=1)

class UserCreate(BaseUser):
    """Handle user creation"""
    confirm_password: str = Field(..., min_length=5, min_digits=1)
    
    @validator('confirm_password')
    def check_passwords(cls, confirm_password, values):
        if 'password' in values and values['password'] != confirm_password:
            raise ValueError('Passwords do not match')
        return confirm_password

class UserUpdate(BaseModel):
    """Handle updates to the user table."""
    name: Optional[str] = Field(max_length=50, example='test')
    email: Optional[EmailStr] = Field(None, example='test@example.com')
    password: Optional[str] = Field(None, min_length=5,  min_digits=1)

class UserInDb(BaseUser):
    id: int
    created_at: datetime
    updated_at: datetime

class User(UserInDb):
    """Format for user display in case of a """
    pass