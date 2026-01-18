from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date, time
import uuid
from uuid import UUID


class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False
    due_date: Optional[date] = None
    due_time: Optional[time] = None


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None


class TaskRead(TaskBase):
    id: uuid.UUID
    user_id: uuid.UUID
    due_date: Optional[date] = None
    due_time: Optional[time] = None
    created_at: datetime
    updated_at: datetime