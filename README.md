# AI-Powered Todo Chatbot

An intelligent todo management system that allows users to interact with their tasks through natural language conversations. This fullstack application extends the basic todo functionality with AI-powered features using OpenAI Agents and MCP tools.

## 🚀 Key Features

- **Natural Language Processing**: AI-powered chat interface for todo management using OpenAI
- **MCP Tools Integration**: Secure task operations through standardized MCP tools
- **Persistent Conversations**: Conversation history and context management
- **User Authentication**: Complete registration and login system with JWT tokens
- **Task Management**: Create, read, update, and delete tasks with full CRUD operations
- **User Isolation**: Tasks are securely isolated by user with proper ownership validation
- **Responsive UI**: Modern Next.js interface with clean user experience
- **Secure API**: FastAPI backend with proper authentication and authorization
- **Database Integration**: Neon Serverless PostgreSQL with SQLModel ORM
- **Security-focused**: Input validation, authentication middleware, and secure data handling
- **Spec-driven development**: Comprehensive testing and architecture documentation

## 🛡️ Security & Ownership

- **JWT Authentication**: Secure token-based authentication with proper validation
- **User Ownership**: Each task is tied to a specific user with ownership validation
- **Authorization Middleware**: All API endpoints verify user permissions
- **Password Security**: Bcrypt hashing with proper salt management
- **Input Validation**: All inputs are validated to prevent injection and errors
- **Secure Architecture**: Follows security best practices with layered architecture

## ⚙️ Tech Stack

- **Frontend**: Next.js 16+, React, TypeScript, OpenAI ChatKit
- **Backend**: Python 3.11+, FastAPI, SQLModel
- **AI Framework**: OpenAI Agents SDK
- **MCP Server**: Python MCP SDK
- **Database**: Neon Serverless PostgreSQL
- **Authentication**: Better Auth, JWT tokens
- **ORM**: SQLModel (SQLAlchemy + Pydantic)
- **Testing**: pytest for backend, Jest for frontend

## 📦 Installation

1. Clone the repository or download the source code
2. Install dependencies for both frontend and backend:
   ```bash
   # Backend setup
   cd backend
   pip install -r requirements.txt

   # Frontend setup
   cd ../frontend
   npm install
   ```

3. Set up environment variables:
   ```bash
   # Backend (.env in backend directory)
   DATABASE_URL="your_postgresql_connection_string"
   SECRET_KEY="your_secret_key_for_jwt"

   # Frontend (.env.local in frontend directory)
   NEXT_PUBLIC_API_BASE_URL="https://asifabdulqadir-phase-3-backend.hf.space"
   ```

## ▶️ Usage

### Local Development

To run the fullstack application locally:

1. Start the backend server:
   ```bash
   cd backend
   uvicorn src.main:app --reload --port 8000
   ```

2. In a new terminal, start the frontend:
   ```bash
   cd frontend
   npm run dev
   ```

3. Access the application:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000

### Production Deployment

#### Backend
The backend is already deployed at: https://asifabdulqadir-phase-3-backend.hf.space

#### Frontend (Vercel Deployment)
To deploy the frontend to Vercel:

1. Make sure your `NEXT_PUBLIC_API_URL` is set to the deployed backend URL in `frontend/.env`
2. Install Vercel CLI: `npm i -g vercel`
3. Navigate to the frontend directory: `cd frontend`
4. Deploy: `vercel --prod`

Or connect your GitHub repository to Vercel for automatic deployments.

### Access the Application
   - Frontend: Deployed on Vercel (your frontend URL)
   - Backend API: https://asifabdulqadir-phase-3-backend.hf.space
   - API Documentation: https://asifabdulqadir-phase-3-backend.hf.space/docs

## 📁 Project Structure

```
backend/
├── src/
│   ├── api/
│   │   └── v1/
│   │       ├── endpoints/
│   │       │   ├── auth.py      # Authentication endpoints
│   │       │   └── tasks.py     # Task management endpoints
│   │       └── deps.py          # Dependency injection
│   ├── models/
│   │   ├── user.py              # User model with authentication
│   │   └── task.py              # Task model with user relationships
│   ├── schemas/
│   │   ├── user.py              # User data schemas
│   │   └── task.py              # Task data schemas
│   ├── services/
│   │   ├── user_service.py      # User business logic
│   │   └── task_service.py      # Task business logic
│   ├── utils/
│   │   └── security.py          # Authentication utilities
│   └── database.py              # Database configuration
├── tests/
└── requirements.txt

frontend/
├── app/
│   ├── login/                   # Login page
│   ├── signup/                  # Registration page
│   └── tasks/                   # Task management page
├── components/
│   └── ui/
│       └── Header.tsx           # Navigation header
├── lib/
│   └── api.ts                   # API client with authentication
└── package.json

specs/
├── 001-fullstack-todo-app/
│   ├── spec.md                  # Feature specification
│   ├── plan.md                  # Architecture plan
│   └── tasks.md                 # Implementation tasks
```

## 🧪 Testing

To run the backend tests:

```bash
cd backend
pytest tests/
```

To run the frontend tests:

```bash
cd frontend
npm test
```

## 🏗️ Architecture

The application follows a secure, fullstack architecture:
- **Frontend**: Next.js application with token-based authentication
- **Backend**: FastAPI with JWT authentication middleware
- **Database**: PostgreSQL with proper foreign key relationships
- **Security**: Layered authentication and authorization with proper validation
- **API Design**: RESTful endpoints with consistent error handling

## 🔒 Error Handling & Security

The application includes comprehensive error handling and security measures:
- **JWT Validation**: All protected endpoints verify token validity and user permissions
- **User Isolation**: Users can only access and modify their own tasks
- **Input Validation**: All API inputs are validated using Pydantic schemas
- **Database Relationships**: Proper foreign keys and relationships prevent data corruption
- **Secure Operations**: Authentication required for all task operations
- **Spec Compliance**: Follows spec-driven development with comprehensive testing