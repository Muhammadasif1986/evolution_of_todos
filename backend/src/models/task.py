from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING, List
from datetime import datetime, date, time
import uuid
from src.models.base import Base
from sqlalchemy import Column, DateTime, func, Date, Time
from sqlalchemy.dialects.postgresql import JSON
from pydantic import BaseModel
import json

if TYPE_CHECKING:
    from src.models.user import User


class RecurrencePatternBase(BaseModel):
    """Pydantic model for recurrence pattern to be embedded in Task"""
    type: Optional[str] = "daily"  # daily, weekly, monthly, yearly, custom
    interval: Optional[int] = 1  # How many intervals between recurrences
    days_of_week: Optional[List[str]] = []  # For weekly recurrence: monday, tuesday, etc.
    day_of_month: Optional[int] = None  # For monthly recurrence
    end_date: Optional[datetime] = None  # When to stop recurrence
    occurrence_count: Optional[int] = None  # Max number of occurrences


class ReminderSettingsBase(BaseModel):
    """Pydantic model for reminder settings to be embedded in Task"""
    enabled: bool = True
    time_before: Optional[int] = 15  # Minutes before due time
    notification_channels: List[str] = ["email"]  # email, push, sms


class TaskBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)
    status: str = Field(default="pending")  # pending, completed, archived
    priority: str = Field(default="medium")  # low, medium, high, urgent
    tags: List[str] = Field(default=[])  # Array field for tags
    due_date: Optional[date] = Field(default=None, sa_column=Column(Date, nullable=True))
    due_time: Optional[time] = Field(default=None, sa_column=Column(Time, nullable=True))
    # Store recurrence pattern as JSON string
    recurrence_pattern: Optional[str] = Field(default=None, sa_column=Column("recurrence_pattern", JSON, nullable=True))
    # Store reminder settings as JSON string
    reminder_settings: Optional[str] = Field(default=None, sa_column=Column("reminder_settings", JSON, nullable=True))
    user_id: uuid.UUID = Field(nullable=False)  # Foreign key to users table


class Task(TaskBase, Base, table=True):
    __tablename__ = "tasks"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)  # UUID primary key

    # Relationship to User
    user: "User" = Relationship(back_populates="tasks")

    # Timestamp fields
    created_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now())
    )
    updated_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    )
    completed_at: Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True), nullable=True)
    )


class TaskCreate(TaskBase):
    pass  # Inherits all fields from TaskBase including due_date and due_time


class TaskUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    tags: Optional[List[str]] = None
    due_date: Optional[date] = None
    due_time: Optional[time] = None
    recurrence_pattern: Optional[str] = None  # JSON string for recurrence
    reminder_settings: Optional[str] = None  # JSON string for reminders
    completed_at: Optional[datetime] = None


class TaskRead(TaskBase):
    id: uuid.UUID
    user_id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime] = None