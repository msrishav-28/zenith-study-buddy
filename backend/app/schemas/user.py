from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

from app.models.user import LearningStyle

class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: Optional[str] = None
    learning_style: Optional[LearningStyle] = LearningStyle.VISUAL
    preferred_language: Optional[str] = "en-US"

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    learning_style: Optional[LearningStyle] = None
    preferred_language: Optional[str] = None
    preferred_voice_id: Optional[str] = None

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(UserBase):
    id: int
    is_active: bool
    is_premium: bool
    is_verified: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    username: Optional[str] = None