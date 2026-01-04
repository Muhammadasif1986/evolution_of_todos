from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING
from datetime import datetime
from src.models.base import UUIDModel
from sqlalchemy import Column, DateTime, func
import uuid


if TYPE_CHECKING:
    from src.models.user import User


class SessionBase(SQLModel):
    token: str = Field(unique=True, nullable=False, max_length=500)
    user_id: uuid.UUID = Field(foreign_key="users.id", nullable=False)
    expires_at: datetime = Field(nullable=False)
    is_active: bool = Field(default=True)


class Session(SessionBase, UUIDModel, table=True):
    __tablename__ = "sessions"

    # Timestamp fields
    created_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now())
    )
    updated_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    )

    # Foreign key fields
    user_id: uuid.UUID = Field(foreign_key="users.id", nullable=False)

    # Relationships
    user: Optional["User"] = Relationship()


class SessionCreate(SessionBase):
    pass


class SessionRead(SessionBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime