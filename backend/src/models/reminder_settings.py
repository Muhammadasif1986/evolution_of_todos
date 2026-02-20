from sqlmodel import SQLModel
from typing import Optional, List
from pydantic import BaseModel


class ReminderSettingsBase(BaseModel):
    """Pydantic model for reminder settings to be embedded in Task"""
    enabled: bool = True
    time_before: Optional[int] = 15  # Minutes before due time
    notification_channels: List[str] = ["email"]  # email, push, sms


class ReminderSettingsCreate(ReminderSettingsBase):
    pass


class ReminderSettingsUpdate(BaseModel):
    enabled: Optional[bool] = None
    time_before: Optional[int] = None
    notification_channels: Optional[List[str]] = None


class ReminderSettings(ReminderSettingsBase):
    pass