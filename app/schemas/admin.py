from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from enum import Enum
from typing import Optional,Generic, TypeVar
from app.schemas.user import ProfileModel, ProfileResponse

class AdminRole(str, Enum):
    admin = "admin"

class AdminRegister(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    role: AdminRole
    password: str = Field(..., min_length=8)

class AdminAuthResponse(BaseModel):
    username: str
    email: EmailStr
    role: AdminRole
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"

    class Config:
        from_attributes = True

class AdminLogin(BaseModel):
    email: EmailStr
    password: str

class AdminProfileModel(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    full_name: Optional[str] = None
    avi: Optional[str] = None

class AdminProfileResponse(AdminProfileModel):
    uuid: str
    email: EmailStr
    role: AdminRole
    full_name: str
    username: str
    avi: Optional[str] = None
    is_active: bool

class AdminProfileResponseWrapper(BaseModel):
    message: str
    data: AdminProfileResponse

class AdminUserRole(str, Enum):
    admin = "admin"
    event_manager = "event_manager"
    participant = "participant"

class AdminGetUserProfileOut(BaseModel):
    id: str
    email: str
    username: str
    role: AdminUserRole

    class Config:
        from_attributes = True
