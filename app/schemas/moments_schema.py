from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
import uuid
from enum import Enum


class MomentType(str, Enum):
    text = "text"
    image = "image"
    video = "video"

class MomentBase(BaseModel):
    event_id: str = Field(..., description="ID of the associated event")
    content: str = Field(..., description="Content of the moment")
    media_url: Optional[str] = Field(None, description="URL of the media associated with the moment")
    type: MomentType = Field(..., description="Type of the moment")

class MomentCreate(MomentBase):
    pass

class MomentUpdate(BaseModel):
    content: Optional[str] = Field(None, description="Updated content of the moment")
    media_url: Optional[str] = Field(None, description="Updated URL of the media associated with the moment")
    type: Optional[MomentType] = Field(None, description="Updated type of the moment")

class MomentResponse(MomentBase):
    pass