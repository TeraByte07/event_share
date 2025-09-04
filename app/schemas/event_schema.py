from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import uuid

class EventBase(BaseModel):
    name: str
    description: Optional[str] = None
    scheduled_at: datetime
    location: Optional[str] = None

class EventUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    scheduled_at: Optional[datetime] = None
    location: Optional[str] = None

class EventUpdateResponse(EventUpdate):
    id: uuid.UUID
    organizer_id: uuid.UUID
    banner_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class EventResponse(EventBase):
    id: uuid.UUID
    organizer_id: uuid.UUID
    banner_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
