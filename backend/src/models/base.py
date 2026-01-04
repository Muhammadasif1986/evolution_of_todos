from sqlmodel import SQLModel
from typing import Any
import uuid
from datetime import datetime
from sqlalchemy import Column, DateTime, func
from sqlmodel import Field


class Base(SQLModel):
    """Base model that all other models will inherit from."""
    pass


class UUIDModel(Base):
    """Base model with UUID primary key."""
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)


class TimestampMixin:
    """Mixin with timestamp fields."""
    created_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now())
    )
    updated_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    )


class UUIDTimestampMixin(UUIDModel, TimestampMixin):
    """Mixin with UUID primary key and timestamp fields."""
    pass