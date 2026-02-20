from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime
import uuid
from src.models.base import Base
from sqlalchemy import Column, DateTime, func


class EventBase(SQLModel):
    event_type: str  # created, updated, completed, deleted, recurring-triggered, reminder-scheduled
    task_id: Optional[uuid.UUID] = None  # ID of the associated task (nullable for system events)
    task_data: Optional[str] = None  # JSON string of full task object at time of event
    user_id: str  # ID of the user who triggered the event
    source: str  # Component that generated the event


class Event(EventBase, Base, table=True):
    __tablename__ = "events"

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    timestamp: datetime = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now())
    )

    # Additional fields for event processing
    processed: bool = Field(default=False)
    error_message: Optional[str] = Field(default=None, max_length=1000)


class EventCreate(EventBase):
    pass


class EventUpdate(SQLModel):
    processed: Optional[bool] = None
    error_message: Optional[str] = None


class EventRead(EventBase):
    id: str
    timestamp: datetime
    processed: bool
    error_message: Optional[str] = None


class NotificationBase(SQLModel):
    task_id: uuid.UUID  # ID of the associated task
    title: str  # Notification title/text
    due_at: datetime  # When the task is due
    remind_at: datetime  # When to send the reminder (must be before due_at)
    user_id: str  # User to notify
    notification_type: str = "email"  # Type (email, push, sms)
    status: str = "pending"  # Status (pending, sent, failed, cancelled)


class Notification(NotificationBase, Base, table=True):
    __tablename__ = "notifications"

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    created_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now())
    )
    sent_at: Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True), nullable=True)
    )


class NotificationCreate(NotificationBase):
    pass


class NotificationUpdate(SQLModel):
    status: Optional[str] = None
    sent_at: Optional[datetime] = None


class NotificationRead(NotificationBase):
    id: str
    created_at: datetime
    sent_at: Optional[datetime] = None