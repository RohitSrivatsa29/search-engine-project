from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional


class User(BaseModel):
    """User model"""
    id: Optional[str] = Field(None, alias="_id")
    email: EmailStr
    username: str
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "username": "johndoe",
                "created_at": "2024-01-01T00:00:00"
            }
        }


class UserCreate(BaseModel):
    """User registration schema"""
    email: EmailStr
    username: str
    password: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "username": "johndoe",
                "password": "securepassword123"
            }
        }


class UserLogin(BaseModel):
    """User login schema"""
    email: EmailStr
    password: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "securepassword123"
            }
        }


class UserResponse(BaseModel):
    """User response schema (without password)"""
    id: str = Field(..., alias="_id")
    email: EmailStr
    username: str
    created_at: datetime
    
    class Config:
        populate_by_name = True


class Token(BaseModel):
    """JWT token response"""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Token payload data"""
    email: Optional[str] = None
