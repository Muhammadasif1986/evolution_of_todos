# Fullstack Todo Application

A secure, spec-driven fullstack todo application featuring a Next.js frontend with authentication and a FastAPI backend with PostgreSQL database integration. The application follows modern security practices and spec-driven development principles.

## 🚀 Key Features

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

- **Frontend**: Next.js 16+, React, TypeScript
- **Backend**: Python 3.11+, FastAPI, SQLModel
- **Database**: Neon Serverless PostgreSQL
- **Authentication**: JWT tokens with custom auth system
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
   NEXT_PUBLIC_API_BASE_URL="http://localhost:8000"
   ```

## ▶️ Usage

To run the fullstack application:

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
   - API Documentation: http://localhost:8000/docs

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