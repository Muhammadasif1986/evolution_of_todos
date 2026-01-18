from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING
from datetime import datetime, date, time
import uuid
from src.models.base import Base
from sqlalchemy import Column, DateTime, func, Date, Time, ForeignKey

if TYPE_CHECKING:
    from src.models.user import User




class TaskBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)
    due_date: Optional[date] = Field(default=None, sa_column=Column(Date, nullable=True))
    due_time: Optional[time] = Field(default=None, sa_column=Column(Time, nullable=True))


class Task(TaskBase, Base, table=True):
    __tablename__ = "tasks"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)  # UUID primary key
    user_id: uuid.UUID = Field(nullable=False, foreign_key="users.id")  # Foreign key to users table

    # Relationship to User
    user: "User" = Relationship(back_populates="tasks")

    # Timestamp fields
    created_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now())
    )
    updated_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    )



class TaskCreate(TaskBase):
    pass  # Inherits all fields from TaskBase including due_date and due_time


class TaskUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    due_date: Optional[date] = None
    due_time: Optional[time] = None


class TaskRead(TaskBase):
    id: uuid.UUID
    user_id: uuid.UUID
    created_at: datetime
    updated_at: datetime