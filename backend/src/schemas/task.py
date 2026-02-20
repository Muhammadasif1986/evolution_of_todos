from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, date, time
import uuid
from uuid import UUID


class RecurrencePattern(BaseModel):
    type: Optional[str] = "daily"  # daily, weekly, monthly, yearly, custom
    interval: Optional[int] = 1  # How many intervals between recurrences
    days_of_week: Optional[List[str]] = []  # For weekly recurrence: monday, tuesday, etc.
    day_of_month: Optional[int] = None  # For monthly recurrence
    end_date: Optional[date] = None  # When to stop recurrence
    occurrence_count: Optional[int] = None  # Max number of occurrences


class ReminderSettings(BaseModel):
    enabled: bool = True
    time_before: Optional[int] = 15  # Minutes before due time
    notification_channels: List[str] = ["email"]  # email, push, sms


class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: str = "pending"  # pending, completed, archived
    priority: str = "medium"  # low, medium, high, urgent
    tags: List[str] = []
    due_date: Optional[date] = None
    due_time: Optional[time] = None
    recurrence_pattern: Optional[RecurrencePattern] = None
    reminder_settings: Optional[ReminderSettings] = None


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    tags: Optional[List[str]] = None
    due_date: Optional[date] = None
    due_time: Optional[time] = None
    recurrence_pattern: Optional[RecurrencePattern] = None
    reminder_settings: Optional[ReminderSettings] = None


class TaskRead(TaskBase):
    id: uuid.UUID
    user_id: uuid.UUID
    due_date: Optional[date] = None
    due_time: Optional[time] = None
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime] = None