"""AI Agent Implementation using OpenRouter with OpenAI-compatible interface"""

import json
import uuid
from typing import List, Dict, Any, Tuple
import openai
from openai import AsyncOpenAI

from src.tools.mcp_server import mcp_server
from src.config import settings

# Get the OpenRouter API key from the settings
openrouter_api_key = settings.openrouter_api_key

if not openrouter_api_key:
    raise ValueError("OPENROUTER_API_KEY is not set. Please configure it in your environment variables.")

# Create the AsyncOpenAI client with OpenRouter base URL
client = AsyncOpenAI(
    api_key=openrouter_api_key,
    base_url="https://openrouter.ai/api/v1",
)

# Define the available tools for function calling
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "add_task",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_title": {"type": "string", "description": "The title of the task to create"},
                    "task_description": {"type": "string", "description": "Optional description of the task"},
                    "due_date": {"type": "string", "description": "Due date in YYYY-MM-DD format (optional)"},
                    "due_time": {"type": "string", "description": "Due time in HH:MM format (optional)"}
                },
                "required": ["task_title"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_tasks",
            "parameters": {
                "type": "object",
                "properties": {
                    "filter_type": {"type": "string", "description": "Filter type (e.g., all, completed, incomplete)"}
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "complete_task",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {"type": "string", "description": "Identifier of the task to complete"}
                },
                "required": ["task_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "delete_task",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {"type": "string", "description": "Identifier of the task to delete"}
                },
                "required": ["task_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "update_task",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {"type": "string", "description": "Identifier of the task to update"},
                    "task_title": {"type": "string", "description": "New title for the task"},
                    "task_description": {"type": "string", "description": "New description for the task"},
                    "due_date": {"type": "string", "description": "New due date in YYYY-MM-DD format"},
                    "due_time": {"type": "string", "description": "New due time in HH:MM format"}
                },
                "required": ["task_id"]
            }
        }
    }
]

# System prompt for the AI agent to handle todo management
SYSTEM_PROMPT = """
You are an AI assistant specialized in managing todo tasks. Your job is to interpret user requests and use the available tools to manage tasks.

CRITICAL RULES:
- NEVER under any circumstances ask the user for their user_id
- NEVER ask the user to provide their account information
- NEVER ask the user to specify which account they want to use
- NEVER ask for any user identifiers or credentials
- The user_id is automatically provided in all tool calls by the backend system
- DO NOT generate responses about not being able to access account information; your function calling system handles authentication automatically

FUNCTION CALL BEHAVIOR:
- When the user wants to add a task, call add_task with the required parameters
- When the user wants to see their tasks, call list_tasks with appropriate parameters
- When the user wants to complete a task, call complete_task with task_id
- When the user wants to update a task, call update_task with task_id and update fields
- When the user wants to delete a task, call delete_task with task_id

REQUIRED PARAMETERS FOR ALL TOOLS:
- The user_id parameter will be automatically injected into all tool calls (do not specify it in your function calls)
- Extract task details from user's natural language input
- Use proper date/time formats when provided (YYYY-MM-DD for dates, HH:MM for times)

AVAILABLE TOOLS:
- add_task: Add a new task (requires: task_title, optional: task_description, due_date, due_time)
- list_tasks: List user's tasks (optional: filter_type)
- complete_task: Mark a task as completed (requires: task_id)
- update_task: Update an existing task (requires: task_id, other optional fields)
- delete_task: Delete a task (requires: task_id)

TASK FILTER TYPES:
- all: Show all tasks (default)
- completed: Show only completed tasks
- incomplete: Show only incomplete tasks (also called "pending" or "active" tasks)

INTERPRETATION RULES:
- When user says "show pending tasks", "show active tasks", or "show tasks not done", call list_tasks with filter_type="incomplete"
- When user says "show completed tasks", call list_tasks with filter_type="completed"
- When user says "show all tasks", call list_tasks with filter_type="all" or no filter_type

EXAMPLES:
- If user says "Show my pending tasks", call list_tasks with filter_type="incomplete"
- If user says "Add task buy groceries tomorrow at 3pm", call add_task with:
  - task_title: "buy groceries"
  - due_date: tomorrow's date in YYYY-MM-DD format
  - due_time: "15:00"

Always remember: The user_id is automatically provided by the backend system for all tool calls. Do not ask the user for their user_id.
"""

async def process_with_gemini_agent(
    user_message: str,
    conversation_history: List[Dict[str, str]],
    user_id: str
) -> Tuple[str, List[Dict[str, Any]]]:
    """
    Process user message with Google Gemini AI agent and execute any required tools

    Args:
        user_message: The user's natural language input
        conversation_history: Historical context for the AI
        user_id: The ID of the current user

    Returns:
        Tuple of (AI response message, list of executed tool calls)
    """

    # Check if user_id is available - if not, return error message
    if not user_id or user_id is None:
        error_msg = "I cannot access your account information. Please log in again."
        return error_msg, []

    # Prepare the messages for the AI
    messages = []

    # Add system message
    messages.append({"role": "system", "content": SYSTEM_PROMPT})

    # Add conversation history
    for msg in conversation_history:
        # Only add if it's not a duplicate system message
        if msg["role"] != "system" or len([m for m in messages if m["role"] == "system"]) == 0:
            messages.append({"role": msg["role"], "content": msg["content"]})

    # Add current user message
    messages.append({"role": "user", "content": user_message})

    try:
        # Sanitize conversation history by removing any existing tool messages
        sanitized_messages = []
        for msg in messages:
            # Only include user and assistant messages, skip any tool messages
            if msg.get("role") in ["user", "assistant", "system"]:
                sanitized_messages.append(msg)

        # Add the current user message if it's not already there
        if messages[-1]["role"] == "user" and messages[-1] not in sanitized_messages:
            sanitized_messages.append(messages[-1])

        # Call the OpenRouter API using the OpenAI-compatible interface with tools
        model_to_use = settings.model or settings.model_ or "xiaomi/mimo-v2-flash:free"
        response = await client.chat.completions.create(
            model=model_to_use,
            messages=sanitized_messages,
            tools=TOOLS,
            tool_choice="auto",  # Allow the model to decide when to call functions
            temperature=0.7,
            max_tokens=1000
        )

        # Process the response
        ai_response = ""
        executed_tool_calls = []

        # Check if the response contains tool calls
        if response.choices[0].finish_reason == "tool_calls":
            # Process each tool call
            tool_call_results_map = {}  # Map to store results by tool_call_id for proper ordering
            for tool_call in response.choices[0].message.tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)

                # Automatically inject user_id if it's missing from the function arguments
                if "user_id" not in function_args:
                    function_args["user_id"] = user_id

                # Verify that user_id is present in function arguments before executing
                user_id_arg = function_args.get("user_id")
                if not user_id_arg:
                    result = {"success": False, "error": "Missing user_id in tool call. Cannot execute tool without user context."}
                    tool_call_results_map[tool_call.id] = result
                    executed_tool_calls.append({
                        "tool_name": function_name,
                        "parameters": function_args,
                        "result": result
                    })
                    continue

                # Validate that user_id is a proper UUID format before executing the tool
                try:
                    uuid.UUID(user_id_arg)
                except ValueError:
                    result = {"success": False, "error": "Invalid user_id format in tool call. User ID must be a valid UUID."}
                    tool_call_results_map[tool_call.id] = result
                    executed_tool_calls.append({
                        "tool_name": function_name,
                        "parameters": function_args,
                        "result": result
                    })
                    continue

                # Execute the tool call using our MCP server
                try:
                    tool_result = await mcp_server.execute_tool(function_name, function_args)
                    tool_call_results_map[tool_call.id] = tool_result
                    executed_tool_calls.append({
                        "tool_name": function_name,
                        "parameters": function_args,
                        "result": tool_result
                    })
                except Exception as e:
                    result = {"success": False, "error": str(e)}
                    tool_call_results_map[tool_call.id] = result
                    executed_tool_calls.append({
                        "tool_name": function_name,
                        "parameters": function_args,
                        "result": result
                    })

            # If there are tool calls, make a second call to get the final response
            # with the tool call results
            if executed_tool_calls:
                # Create a new messages list with tool results for the follow-up call
                follow_up_messages = sanitized_messages.copy()

                # Add the original assistant message with tool calls
                follow_up_messages.append(response.choices[0].message)

                # Add the tool results with the correct tool_call_id from the original tool call
                # Use the stored results to ensure proper mapping
                for tool_call in response.choices[0].message.tool_calls:
                    tool_result_content = {
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "content": json.dumps(tool_call_results_map[tool_call.id])
                    }
                    follow_up_messages.append(tool_result_content)

                # Get the final response from the model after processing tool results
                model_to_use = settings.model or settings.model_ or "xiaomi/mimo-v2-flash:free"
                final_response = await client.chat.completions.create(
                    model=model_to_use,
                    messages=follow_up_messages,
                    temperature=0.7,
                    max_tokens=1000
                )

                ai_response = final_response.choices[0].message.content or "Operation completed."
            else:
                ai_response = response.choices[0].message.content or "Operation completed."
        else:
            # No tool calls were made, just return the model's response
            ai_response = response.choices[0].message.content or "How can I help you with your tasks?"

        return ai_response, executed_tool_calls

    except Exception as e:
        # If there's an error, return a user-friendly message and no tool calls
        error_msg = f"I encountered an issue processing your request: {str(e)}"
        return error_msg, []