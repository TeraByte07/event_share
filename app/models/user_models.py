from sqlalchemy import String, Integer, Column, Enum, Boolean, DateTime
import enum
from db import Base
from datetime import datetime
import uuid
from sqlalchemy.orm import relationship

class UserRole(str, enum.Enum):
    admin = "admin"
    event_manager = "event_manager"
    participant = "participant"

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=True)
    avi = Column(String, nullable=True)
    role = Column(Enum(UserRole), default=UserRole.participant, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    events = relationship("Events", back_populates="organizer")

class BlacklistedToken(Base):
    __tablename__ = "blacklisted_tokens"

    token = Column(String, primary_key=True, index=True)
    blacklisted_on = Column(DateTime, default=datetime.utcnow)