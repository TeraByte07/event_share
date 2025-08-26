from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from enum import Enum
from typing import Optional,Generic, TypeVar
from datetime import datetime

class UserRole(str, Enum): 
    event_manager = "event_manager"
    participant = "participant"

class UserRegister(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    role: UserRole
    password: str = Field(..., min_length=8)

class ProfileModel(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    full_name: Optional[str] = None
    avi: Optional[str] = None
    
class ProfileResponse(ProfileModel):
    id: str
    email: EmailStr
    role: UserRole
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ProfileResponseWrapper(BaseModel):
    message: str
    data: ProfileResponse

class AuthResponse(BaseModel):
    username: str
    email: EmailStr
    role: UserRole
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
class RefreshTokenRequest(BaseModel):
    refresh_token: str

T = TypeVar('T')
class GenericResponseModel(BaseModel, Generic[T]):
    status_code: int
    message: str
    data: Optional[T] = None

class RefreshTokenRequest(BaseModel):
    refresh_token: str