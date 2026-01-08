from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING, List
from datetime import datetime
from enum import Enum
from src.models.base import UUIDModel
from sqlalchemy import Column, DateTime, func
import uuid


if TYPE_CHECKING:
    from src.models.user import User
    from src.models.todo_item_history import TodoItemHistory


class TodoStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class TodoPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class TodoItemBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    status: TodoStatus = Field(default=TodoStatus.PENDING)
    priority: TodoPriority = Field(default=TodoPriority.MEDIUM)
    due_date: Optional[datetime] = Field(default=None)
    completed_at: Optional[datetime] = Field(default=None)


class TodoItem(TodoItemBase, UUIDModel, table=True):
    __tablename__ = "todo_items"

    # Timestamp fields
    created_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now())
    )
    updated_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    )

    user_id: uuid.UUID = Field(foreign_key="users.id", nullable=False)

    # Relationship to User
    user: Optional["User"] = Relationship(back_populates="todos")


class TodoItemCreate(TodoItemBase):
    pass


class TodoItemUpdate(SQLModel):
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