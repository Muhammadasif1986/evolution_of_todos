"""MCP Server for Todo Operations"""

import asyncio
from typing import Dict, Any, Callable
from fastapi import FastAPI, HTTPException
import json

# Import the task operation tools
from .task_operations import (
    add_task,
    list_tasks,
    complete_task,
    delete_task,
    update_task
)

# Dictionary to hold all available tools
TOOLS_REGISTRY: Dict[str, Callable] = {
    "add_task": add_task,
    "list_tasks": list_tasks,
    "complete_task": complete_task,
    "delete_task": delete_task,
    "update_task": update_task
}


class MCPServer:
    """MCP Server to handle tool registrations and executions"""

    def __init__(self):
        self.tools = TOOLS_REGISTRY.copy()

    async def execute_tool(self, tool_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a registered tool with given parameters

        Args:
            tool_name: Name of the tool to execute
            parameters: Parameters to pass to the tool

        Returns:
            Result of the tool execution
        """
        if tool_name not in self.tools:
            raise HTTPException(status_code=404, detail=f"Tool '{tool_name}' not found")

        tool_func = self.tools[tool_name]

        try:
            # Execute the tool asynchronously
            result = await tool_func(**parameters)
            return result
        except TypeError as e:
            # Handle case where parameters don't match tool signature
            raise HTTPException(
                status_code=400,
                detail=f"Invalid parameters for tool '{tool_name}': {str(e)}"
            )
        except Exception as e:
            # Handle any other errors during tool execution
            raise HTTPException(
                status_code=500,
                detail=f"Error executing tool '{tool_name}': {str(e)}"
            )

    def register_tool(self, name: str, func: Callable):
        """Register a new tool with the server"""
        self.tools[name] = func

    def get_tool_schema(self, tool_name: str) -> Dict[str, Any]:
        """Get the schema for a specific tool (for AI agent integration)"""
        import inspect

        if tool_name not in self.tools:
            return {}

        func = self.tools[tool_name]
        sig = inspect.signature(func)

        # Build parameter schema
        params = {}
        for param_name, param in sig.parameters.items():
            param_info = {"type": "string"}  # Default to string

            # Try to infer type from annotation
            if param.annotation != inspect.Parameter.empty:
                if param.annotation == str:
                    param_info["type"] = "string"
                elif param.annotation == int:
                    param_info["type"] = "integer"
                elif param.annotation == float:
                    param_info["type"] = "number"
                elif param.annotation == bool:
                    param_info["type"] = "boolean"
                elif param.annotation == dict:
                    param_info["type"] = "object"
                elif param.annotation == list:
                    param_info["type"] = "array"

            # Check if parameter has a default value
            if param.default != inspect.Parameter.empty:
                param_info["default"] = param.default
            else:
                param_info["required"] = True

            params[param_name] = param_info

        return {
            "name": tool_name,
            "description": func.__doc__.strip() if func.__doc__ else "",
            "parameters": {
                "type": "object",
                "properties": params
            }
        }

    def get_all_tools_schemas(self) -> list:
        """Get schemas for all registered tools"""
        schemas = []
        for tool_name in self.tools.keys():
            schema = self.get_tool_schema(tool_name)
            if schema:
                schemas.append({
                    "type": "function",
                    "function": schema
                })
        return schemas


# Global MCP server instance
mcp_server = MCPServer()


# FastAPI app for MCP endpoints
app = FastAPI(title="Todo MCP Tools Server", version="1.0.0")


@app.post("/mcp/execute")
async def execute_mcp_tool(tool_name: str, parameters: Dict[str, Any]):
    """Execute an MCP tool with the provided parameters"""
    result = await mcp_server.execute_tool(tool_name, parameters)
    return result


@app.get("/mcp/tools")
async def list_available_tools():
    """List all available MCP tools"""
    return {"tools": list(mcp_server.tools.keys())}


@app.get("/mcp/tools/{tool_name}")
async def get_tool_details(tool_name: str):
    """Get details about a specific tool"""
    schema = mcp_server.get_tool_schema(tool_name)
    if not schema:
        raise HTTPException(status_code=404, detail=f"Tool '{tool_name}' not found")
    return schema


@app.get("/mcp/openapi")
async def get_openapi_schema():
    """Get OpenAPI schema for all tools (for AI agent integration)"""
    return mcp_server.get_all_tools_schemas()