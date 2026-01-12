# Quickstart Guide: AI-Powered Todo Chatbot

## Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL (or Neon Serverless PostgreSQL account)
- OpenAI API key
- Better Auth account

## Setup Instructions

### Backend Setup
1. Install dependencies: `pip install fastapi sqlmodel openai python-mcp-sdk`
2. Set environment variables:
   - `OPENAI_API_KEY`: Your OpenAI API key
   - `DATABASE_URL`: PostgreSQL connection string
   - `BETTER_AUTH_SECRET`: Better Auth secret
3. Run database migrations: `alembic upgrade head`
4. Start the server: `uvicorn main:app --reload`

### Frontend Setup
1. Install dependencies: `npm install @openai/chatkit`
2. Set environment variables:
   - `NEXT_PUBLIC_API_URL`: Backend API URL
3. Run development server: `npm run dev`

### MCP Tools Configuration
1. Define your MCP tools using the python-mcp-sdk
2. Register tools with the AI agent
3. Ensure all tools are stateless and use database for persistence

## API Endpoints
- `POST /api/{user_id}/chat` - Main chat endpoint
- Authentication handled via Better Auth tokens

## Key Components
- `Task`, `Conversation`, `Message` models in SQLModel
- MCP tools: `add_task`, `list_tasks`, `complete_task`, `delete_task`, `update_task`
- OpenAI agent configured with MCP tools
- Better Auth for user management