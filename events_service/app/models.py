"""SQLAlchemy models for the Events service.

See docs/data-model.md for the full schema rationale.
"""
import enum
import uuid
from datetime import datetime

from sqlalchemy import (
    Column, String, Boolean, DateTime, ForeignKey, Enum, Numeric, Text
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class UserRole(str, enum.Enum):
    visitor = "visitor"
    registered = "registered"
    admin = "admin"


class EventCategory(str, enum.Enum):
    festival = "festival"
    community = "community"
    social_cultural = "social_cultural"
    food_market = "food_market"
    embassy_official = "embassy_official"
    commercial_promo = "commercial_promo"
    other = "other"


class OrganizerType(str, enum.Enum):
    temple = "temple"
    association = "association"
    embassy = "embassy"
    business = "business"
    individual = "individual"


class EventStatus(str, enum.Enum):
    draft = "draft"
    submitted = "submitted"
    under_review = "under_review"
    approved = "approved"
    rejected = "rejected"


class City(Base):
    __tablename__ = "cities"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    country = Column(String, nullable=False)
    region = Column(String)
    timezone = Column(String, nullable=False)
    latitude = Column(Numeric(9, 6), nullable=False)
    longitude = Column(Numeric(9, 6), nullable=False)


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.registered, nullable=False)
    language = Column(String, default="en")
    created_at = Column(DateTime, default=datetime.utcnow)


class Event(Base):
    __tablename__ = "events"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    city_id = Column(UUID(as_uuid=True), ForeignKey("cities.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text)
    venue_name = Column(String)
    venue_address = Column(String)
    start_datetime = Column(DateTime, nullable=False)
    end_datetime = Column(DateTime)
    organizer_name = Column(String)
    organizer_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))

    event_category = Column(Enum(EventCategory), default=EventCategory.other)
    community_state_tag = Column(String)
    organizer_type = Column(Enum(OrganizerType))

    is_free = Column(Boolean, default=True)
    has_entry_fee = Column(Boolean, default=False)
    price_from = Column(Numeric(10, 2))
    price_to = Column(Numeric(10, 2))
    currency = Column(String, default="EUR")
    booking_url = Column(String)

    language = Column(String, default="en")
    is_family_friendly = Column(Boolean, default=True)

    status = Column(Enum(EventStatus), default=EventStatus.draft, nullable=False)
    created_by_user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    reviewed_by_admin_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    review_notes = Column(Text)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    city = relationship("City")
