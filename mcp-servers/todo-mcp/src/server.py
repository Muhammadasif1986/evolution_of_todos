import json
from typing import Dict, Any, List
from mcp import server
from mcp.types import TextContent, Prompt, PromptResult, Tool
from pydantic import BaseModel
import asyncio
import httpx
from datetime import datetime

class TodoMCPService:
    """Service to handle todo-related operations for the MCP server"""

    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.http_client = httpx.AsyncClient()

    async def get_tasks(self, user_id: str) -> List[Dict[str, Any]]:
        """Get tasks for a user"""
        try:
            # This would integrate with your backend service via Dapr or directly
            # For now, using placeholder implementation
            headers = {"Authorization": f"Bearer {user_id}"}
            response = await self.http_client.get(f"{self.base_url}/api/v1/tasks", headers=headers)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error getting tasks: {e}")
            return []

    async def create_task(self, user_id: str, title: str, description: str = "", due_date: str = None, priority: str = "medium") -> Dict[str, Any]:
        """Create a new task"""
        try:
            headers = {"Authorization": f"Bearer {user_id}"}
            task_data = {
                "title": title,
                "description": description,
                "priority": priority
            }
            if due_date:
                task_data["due_date"] = due_date
            response = await self.http_client.post(f"{self.base_url}/api/v1/tasks", headers=headers, json=task_data)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error creating task: {e}")
            return {}

    async def update_task(self, user_id: str, task_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """Update a task"""
        try:
            headers = {"Authorization": f"Bearer {user_id}"}
            response = await self.http_client.put(f"{self.base_url}/api/v1/tasks/{task_id}", headers=headers, json=updates)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error updating task: {e}")
            return {}

    async def complete_task(self, user_id: str, task_id: str) -> Dict[str, Any]:
        """Mark a task as complete"""
        try:
            headers = {"Authorization": f"Bearer {user_id}"}
            response = await self.http_client.post(f"{self.base_url}/api/v1/tasks/{task_id}/complete", headers=headers)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error completing task: {e}")
            return {}


# Initialize the service
todo_service = TodoMCPService()


async def main():
    """Main function to start the MCP server"""

    async with server("todo-mcp") as srv:
        # Define prompts for the todo chatbot
        await srv.publish_prompts([
            Prompt(
                name="create-task",
                description="Create a new task",
                parameters={
                    "title": {"type": "string", "description": "Title of the task"},
                    "description": {"type": "string", "description": "Description of the task", "optional": True},
                    "due_date": {"type": "string", "description": "Due date (YYYY-MM-DD format)", "optional": True},
                    "priority": {"type": "string", "description": "Priority (low, medium, high, urgent)", "default": "medium"}
                }
            ),
            Prompt(
                name="list-tasks",
                description="List all tasks for the user",
                parameters={}
            ),
            Prompt(
                name="complete-task",
                description="Mark a task as complete",
                parameters={
                    "task_id": {"type": "string", "description": "ID of the task to complete"}
                }
            )
        ])

        # Define tools for the todo chatbot
        await srv.publish_tools([
            Tool(
                name="get_tasks",
                description="Get all tasks for a user",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "The user's ID"}
                    }
                }
            ),
            Tool(
                name="create_task",
                description="Create a new task",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "The user's ID"},
                        "title": {"type": "string", "description": "Title of the task"},
                        "description": {"type": "string", "description": "Description of the task", "optional": True},
                        "due_date": {"type": "string", "description": "Due date in YYYY-MM-DD format", "optional": True},
                        "priority": {"type": "string", "description": "Task priority", "default": "medium"}
                    }
                }
            ),
            Tool(
                name="complete_task",
                description="Mark a task as complete",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "The user's ID"},
                        "task_id": {"type": "string", "description": "ID of the task to complete"}
                    }
                }
            )
        ])

        @srv.request_handler("tools/call")
        async def handle_tool_call(context, tool_name: str, arguments: Any) -> Any:
            """Handle tool call requests"""
            user_id = arguments.get("user_id", "default")

            if tool_name == "get_tasks":
                tasks = await todo_service.get_tasks(user_id)
                return {"tasks": tasks}
            elif tool_name == "create_task":
                result = await todo_service.create_task(
                    user_id=user_id,
                    title=arguments.get("title", ""),
                    description=arguments.get("description", ""),
                    due_date=arguments.get("due_date"),
                    priority=arguments.get("priority", "medium")
                )
                return {"task": result}
            elif tool_name == "complete_task":
                result = await todo_service.complete_task(user_id, arguments.get("task_id"))
                return {"result": result}
            else:
                return {"error": f"Unknown tool: {tool_name}"}

        @srv.request_handler("prompts/get")
        async def handle_prompt(context, name: str, arguments: Dict[str, Any]) -> PromptResult:
            """Handle prompt requests"""
            user_id = arguments.get("user_id", "default")

            if name == "list-tasks":
                tasks = await todo_service.get_tasks(user_id)
                content = f"Your tasks:\n"
                for task in tasks:
                    status = task.get('status', 'pending')
                    title = task.get('title', 'No title')
                    content += f"- [{status}] {title}\n"
                return PromptResult(messages=[TextContent(type="text", text=content)])

            elif name == "create-task":
                result = await todo_service.create_task(
                    user_id=user_id,
                    title=arguments.get("title", ""),
                    description=arguments.get("description", ""),
                    due_date=arguments.get("due_date"),
                    priority=arguments.get("priority", "medium")
                )
                content = f"Task created: {result.get('title', 'Unknown')}"
                return PromptResult(messages=[TextContent(type="text", text=content)])

            elif name == "complete-task":
                result = await todo_service.complete_task(user_id, arguments.get("task_id"))
                content = f"Task completed: {arguments.get('task_id')}"
                return PromptResult(messages=[TextContent(type="text", text=content)])

            else:
                return PromptResult(messages=[TextContent(type="text", text="Unknown prompt")])

        # Keep the server running
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())