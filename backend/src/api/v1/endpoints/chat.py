"""Chat API Endpoint for AI-Powered Todo Management"""

from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any, Optional
import uuid
from datetime import datetime
from sqlmodel import Session, select
from pydantic import BaseModel

from src.database import get_session
from src.models.todo_chat_models import (
    Conversation, Message, MessageCreate, ConversationCreate,
    ConversationPublic, MessagePublic
)
from src.models.user import User
from src.tools.mcp_server import mcp_server
from src.auth.middleware import get_current_user

router = APIRouter(tags=["chat"])

# Request and Response models
class ChatRequest(BaseModel):
    user_message: str
    conversation_id: Optional[str] = None


class ToolCallResult(BaseModel):
    tool_name: str
    parameters: Dict[str, Any]
    result: Dict[str, Any]


class ChatResponse(BaseModel):
    success: bool
    message: str
    conversation_id: str
    tool_calls: Optional[list[ToolCallResult]] = []


@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(
    request: ChatRequest,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
) -> ChatResponse:
    """
    Main chat endpoint for AI-powered todo management

    Args:
        request: Chat request containing user message and optional conversation ID
        current_user: The authenticated user extracted from JWT token
        session: Database session for queries

    Returns:
        Chat response with AI message and any tool calls executed
    """
    user_id = current_user["user_id"]

    # Validate that user_id is a proper UUID
    try:
        user_uuid = uuid.UUID(user_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid user ID format")

    try:
        # Validate user exists
        user_exists = session.exec(select(User).where(User.id == user_uuid)).first()
        if not user_exists:
            raise HTTPException(status_code=404, detail="User not found")

        # Get or create conversation
        conversation = None
        if request.conversation_id:
            # Validate that conversation_id is a proper UUID string format
            try:
                uuid.UUID(request.conversation_id)
            except ValueError:
                raise HTTPException(status_code=400, detail="Invalid conversation ID format")

            # Try to find existing conversation
            conversation = session.exec(
                select(Conversation)
                .where(Conversation.conversation_id == request.conversation_id)
                .where(Conversation.user_id == user_uuid)
            ).first()

            if not conversation:
                raise HTTPException(status_code=404, detail="Conversation not found or unauthorized")
        else:
            # Create new conversation
            conversation_data = ConversationCreate()
            conversation = Conversation(
                user_id=user_uuid
            )
            session.add(conversation)
            session.commit()
            session.refresh(conversation)

        # Store user's message
        user_message = Message(
            role="user",
            content=request.user_message,
            user_id=user_uuid,
            conversation_id=conversation.conversation_id
        )
        session.add(user_message)
        session.commit()

        # Get recent conversation history for context (last 10 messages)
        recent_messages = session.exec(
            select(Message)
            .where(Message.conversation_id == conversation.conversation_id)
            .order_by(Message.created_at.desc())
            .limit(10)
        ).all()
        # Reverse to get chronological order
        recent_messages.reverse()

        # Prepare conversation history for AI agent
        ai_history = []
        for msg in recent_messages:
            ai_history.append({
                "role": msg.role,
                "content": msg.content
            })

        # Add current user message
        ai_history.append({
            "role": "user",
            "content": request.user_message
        })

        # Process with AI agent (placeholder implementation)
        # In a real implementation, this would call the OpenAI API
        ai_response, tool_calls_executed = await process_with_ai_agent(
            user_message=request.user_message,
            conversation_history=ai_history,
            user_id=str(user_uuid)  # Pass as string to maintain compatibility with existing code
        )

        # Store AI's response
        ai_message = Message(
            role="assistant",
            content=ai_response,
            user_id=user_uuid,
            conversation_id=conversation.conversation_id
        )
        session.add(ai_message)
        session.commit()

        # Update conversation timestamp
        conversation.updated_at = datetime.utcnow()
        session.add(conversation)
        session.commit()

        # Format tool calls for response
        tool_call_results = []
        for tool_call in tool_calls_executed:
            tool_call_results.append(
                ToolCallResult(
                    tool_name=tool_call["tool_name"],
                    parameters=tool_call["parameters"],
                    result=tool_call["result"]
                )
            )

        return ChatResponse(
            success=True,
            message=ai_response,
            conversation_id=conversation.conversation_id,
            tool_calls=tool_call_results
        )

    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


# Import the new AI agent implementation
from src.ai.ai_agent import process_with_gemini_agent


async def process_with_ai_agent(
    user_message: str,
    conversation_history: list,
    user_id: str
) -> tuple[str, list]:
    """
    Process user message with AI agent and execute any required tools

    Args:
        user_message: The user's natural language input
        conversation_history: Historical context for the AI
        user_id: The ID of the current user

    Returns:
        Tuple of (AI response message, list of executed tool calls)
    """
    # Delegate to the new Google Gemini agent implementation
    return await process_with_gemini_agent(
        user_message=user_message,
        conversation_history=conversation_history,
        user_id=user_id
    )