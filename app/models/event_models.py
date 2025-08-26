from sqlalchemy import String, Integer, Column, Enum, Boolean, DateTime
from db import Base
from datetime import datetime
import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class Events(Base):
    __tablename__ = "events"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    scheduled_at = Column(DateTime, nullable=False)
    location = Column(String, nullable=True)
    organizer_id = Column(String, ForeignKey("users.id"), nullable=False)
    organizer = relationship("User", back_populates="events")
    banner_url = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)