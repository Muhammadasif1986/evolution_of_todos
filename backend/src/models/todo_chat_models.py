from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel
import uuid


def generate_uuid():
    return str(uuid.uuid4())


class ConversationBase(SQLModel):
    pass


class Conversation(ConversationBase, table=True):
    """Conversation entity model"""
    __tablename__ = "conversations"

    conversation_id: str = Field(default_factory=generate_uuid, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="users.id")  # Use the same type as existing user model
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class ConversationCreate(SQLModel):
    """Schema for creating a new conversation"""
    pass


class ConversationPublic(SQLModel):
    """Public representation of a conversation"""
    conversation_id: str
    user_id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class MessageBase(SQLModel):
    role: str = Field(regex="^(user|assistant|tool)$")
    content: str


class Message(MessageBase, table=True):
    """Message entity model"""
    __tablename__ = "messages"

    message_id: str = Field(default_factory=generate_uuid, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="users.id")  # Use the same type as existing user model
    conversation_id: str = Field(foreign_key="conversations.conversation_id")
    created_at: datetime = Field(default_factory=datetime.utcnow)


class MessageCreate(MessageBase):
    """Schema for creating a new message"""
    pass


class MessagePublic(MessageBase):
    """Public representation of a message"""
    message_id: str
    user_id: uuid.UUID
    conversation_id: str
    created_at: datetime