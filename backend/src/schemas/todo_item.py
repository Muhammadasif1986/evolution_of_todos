from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from enum import Enum
import uuid


class TodoStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class TodoPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class TodoItemBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: TodoStatus = TodoStatus.PENDING
    priority: TodoPriority = TodoPriority.MEDIUM
    due_date: Optional[datetime] = None


class TodoItemCreate(TodoItemBase):
    pass


class TodoItemUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TodoStatus] = None
    priority: Optional[TodoPriority] = None
    due_date: Optional[datetime] = None


class TodoItemRead(TodoItemBase):
    id: uuid.UUID
    user_id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime] = None


class TodoItemUpdateStatus(BaseModel):
    status: TodoStatus


class TodoItemList(BaseModel):
    items: List[TodoItemRead]
    total: int
    offset: int
    limit: int


class TodoItemFilter(BaseModel):
    status: Optional[TodoStatus] = None
    priority: Optional[TodoPriority] = None
    limit: int = 20
    offset: int = 0
    sort: Optional[str] = "created_at"