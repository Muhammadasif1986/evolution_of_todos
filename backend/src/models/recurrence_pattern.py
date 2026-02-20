from sqlmodel import SQLModel
from typing import Optional, List
from pydantic import BaseModel
from datetime import date


class RecurrencePatternBase(BaseModel):
    """Pydantic model for recurrence pattern to be embedded in Task"""
    type: Optional[str] = "daily"  # daily, weekly, monthly, yearly, custom
    interval: Optional[int] = 1  # How many intervals between recurrences
    days_of_week: Optional[List[str]] = []  # For weekly recurrence: monday, tuesday, etc.
    day_of_month: Optional[int] = None  # For monthly recurrence
    end_date: Optional[date] = None  # When to stop recurrence
    occurrence_count: Optional[int] = None  # Max number of occurrences


class RecurrencePatternCreate(RecurrencePatternBase):
    pass


class RecurrencePatternUpdate(BaseModel):
    type: Optional[str] = None
    interval: Optional[int] = None
    days_of_week: Optional[List[str]] = None
    day_of_month: Optional[int] = None
    end_date: Optional[date] = None
    occurrence_count: Optional[int] = None


class RecurrencePattern(RecurrencePatternBase):
    pass