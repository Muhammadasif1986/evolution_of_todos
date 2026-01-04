from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING, List
from datetime import datetime
from src.models.base import UUIDModel
from sqlalchemy import Column, DateTime, func
import uuid


if TYPE_CHECKING:
    from src.models.todo_item import TodoItem
    from src.models.user import User


class TodoItemHistoryBase(SQLModel):
    todo_item_id: uuid.UUID = Field(foreign_key="todo_items.id", nullable=False)
    previous_status: Optional[str] = Field(max_length=50)
    new_status: str = Field(max_length=50)
    changed_by_user_id: uuid.UUID = Field(foreign_key="users.id", nullable=False)


class TodoItemHistory(TodoItemHistoryBase, UUIDModel, table=True):
    __tablename__ = "todo_item_history"

    # Timestamp fields
    created_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now())
    )
    updated_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    )

    # Relationships
    todo_item: "TodoItem" = Relationship()
    changed_by_user: "User" = Relationship()


class TodoItemHistoryCreate(TodoItemHistoryBase):
    pass


class TodoItemHistoryRead(TodoItemHistoryBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime