from sqlalchemy import String, Column, Enum, Boolean, DateTime
import enum
from db import Base
from datetime import datetime
import uuid
from sqlalchemy.orm import relationship
from app.models.moments_models import event_user_association as event_user
from sqlalchemy.dialects.postgresql import UUID

class UserRole(str, enum.Enum):
    admin = "admin"
    event_manager = "event_manager"
    participant = "participant"

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=True)
    avi = Column(String, nullable=True)
    role = Column(Enum(UserRole), default=UserRole.participant, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # one-to-many: user organizes events
    organized_events = relationship("Events", back_populates="organizer")

    # many-to-many: user participates in events
    events = relationship("Events", secondary=event_user, back_populates="participants")

    # one-to-many with moments
    moments = relationship("Moment", back_populates="user")


class BlacklistedToken(Base):
    __tablename__ = "blacklisted_tokens"

    token = Column(String, primary_key=True, index=True)
    blacklisted_on = Column(DateTime, default=datetime.utcnow)