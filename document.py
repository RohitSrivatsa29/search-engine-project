from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class Document(BaseModel):
    """Document model"""
    id: Optional[str] = Field(None, alias="_id")
    title: str
    content: str
    author_id: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "title": "Introduction to Python",
                "content": "Python is a high-level programming language...",
                "author_id": "user123"
            }
        }


class DocumentCreate(BaseModel):
    """Document creation schema"""
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1)
    
    class Config:
        json_schema_extra = {
            "example": {
                "title": "Introduction to Python",
                "content": "Python is a high-level programming language that emphasizes code readability..."
            }
        }


class DocumentUpdate(BaseModel):
    """Document update schema"""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    content: Optional[str] = Field(None, min_length=1)


class DocumentResponse(BaseModel):
    """Document response schema"""
    id: str = Field(..., alias="_id")
    title: str
    content: str
    author_id: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        populate_by_name = True
