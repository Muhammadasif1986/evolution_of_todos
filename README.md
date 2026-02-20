# Advanced Todo Chatbot - Cloud Deployment

An intelligent todo management system that allows users to interact with their tasks through natural language conversations. This fullstack application extends the basic todo functionality with AI-powered features using OpenAI Agents and MCP tools. The system includes advanced task management with recurring tasks, due dates, and reminder notifications, deployed with event-driven architecture using Kafka and Dapr integration.

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
- **Advanced Task Management**: Support for recurring tasks, due dates, and reminders
- **Event-Driven Architecture**: Asynchronous processing with Kafka for high scalability
- **Dapr Integration**: Service mesh and infrastructure abstraction
- **Cloud-Native**: Kubernetes-ready with Helm charts for deployment

## 🛡️ Security & Ownership

- **JWT Authentication**: Secure token-based authentication with proper validation
- **User Ownership**: Each task is tied to a specific user with ownership validation
- **Authorization Middleware**: All API endpoints verify user permissions
- **Password Security**: Bcrypt hashing with proper salt management
- **Input Validation**: All inputs are validated to prevent injection and errors
- **Secure Architecture**: Follows security best practices with layered architecture
- **Event Validation**: All Kafka events are validated against schemas before processing
- **Dapr Security**: Secure service-to-service communication with Dapr sidecar
- **Secret Management**: Dapr-managed secrets for configuration values

## ⚙️ Tech Stack

- **Frontend**: Next.js 16+, React, TypeScript, OpenAI ChatKit
- **Backend**: Python 3.11+, FastAPI, SQLModel
- **AI Framework**: OpenAI Agents SDK, Google Gemini
- **MCP Server**: Python MCP SDK
- **Database**: Neon Serverless PostgreSQL
- **Authentication**: Better Auth, JWT tokens
- **ORM**: SQLModel (SQLAlchemy + Pydantic)
- **Event Streaming**: Kafka/Redpanda
- **Service Mesh**: Dapr (Distributed Application Runtime)
- **Observability**: Prometheus, Jaeger for tracing
- **Containerization**: Docker, Docker Compose
- **Orchestration**: Kubernetes, Helm
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

3. Install and initialize Dapr:
   ```bash
   # Install Dapr CLI
   wget -q https://raw.githubusercontent.com/dapr/cli/master/install/install.sh -O - | /bin/bash

   # Initialize Dapr in standalone mode
   dapr init
   ```

4. Set up environment variables:
   ```bash
   # Backend (.env in backend directory)
   DATABASE_URL="your_postgresql_connection_string"
   SECRET_KEY="your_secret_key_for_jwt"
   KAFKA_BROKERS="localhost:9092"
   DAPR_HTTP_ENDPOINT="http://localhost:3500"
   DAPR_GRPC_ENDPOINT="http://localhost:50001"

   # Frontend (.env.local in frontend directory)
   NEXT_PUBLIC_API_BASE_URL="https://asifabdulqadir-phase-3-backend.hf.space"
   NEXT_PUBLIC_API_URL="http://localhost:8000"
   ```

5. Start Kafka/Redpanda locally:
   ```bash
   # Option 1: Use Redpanda (Kafka-compatible)
   docker run -d --pull=always --name=redpanda-1 \
     --rm -p 9092:9092 -p 9644:9644 \
     docker.redpanda.com/redpandadata/redpanda:latest \
     redpanda start --mode dev-container --smp 1 --memory 1G --reserve-memory 100M --overprovisioned
   ```

## ▶️ Usage

### Local Development

To run the fullstack application locally:

1. Start the backend server with Dapr:
   ```bash
   cd backend
   dapr run --app-id todo-backend --app-port 8000 -- uvicorn src.api.main:app --reload --port 8000
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
   - Dapr Dashboard: http://localhost:8080
   - Metrics: http://localhost:8000/metrics
   - Dapr Health: http://localhost:8000/dapr/health

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
.
├── backend/
│   ├── src/
│   │   ├── api/
│   │   │   └── v1/
│   │   │       ├── endpoints/
│   │   │       │   ├── auth.py           # Authentication endpoints
│   │   │       │   ├── tasks.py          # Task management endpoints
│   │   │       │   └── chat.py           # Chatbot interaction endpoints
│   │   │       └── main.py               # Main application with Dapr and tracing
│   │   ├── models/
│   │   │   ├── user.py                   # User model with authentication
│   │   │   ├── task.py                   # Task model with user relationships
│   │   │   ├── event.py                  # Event and Notification models
│   │   │   ├── recurrence_pattern.py     # Recurring task pattern model
│   │   │   └── reminder_settings.py      # Reminder settings model
│   │   ├── schemas/
│   │   │   ├── task.py                   # Task data schemas
│   │   │   └── ...                       # Other data schemas
│   │   ├── services/
│   │   │   ├── user_service.py           # User business logic
│   │   │   ├── task_service.py           # Task business logic
│   │   │   ├── recurring_service.py      # Recurring task logic
│   │   │   ├── reminder_service.py       # Reminder system logic
│   │   │   ├── kafka_service.py          # Kafka integration
│   │   │   ├── event_processor.py        # Event processing
│   │   │   ├── audit_service.py          # Audit logging
│   │   │   └── dapr_service.py           # Dapr integration
│   │   ├── middleware/
│   │   │   ├── tracing.py                # Distributed tracing
│   │   │   └── event_validation.py       # Event schema validation
│   │   ├── health/
│   │   │   └── dapr_health.py            # Dapr health checks
│   │   ├── database.py                   # Database configuration
│   │   └── config.py                     # Application configuration
│   ├── tests/
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   └── services/
│   ├── Dockerfile
│   └── package.json
├── kubernetes/
│   ├── charts/
│   │   └── todo-chatbot/                # Helm chart for deployment
│   ├── kafka/
│   │   └── kafka-cluster.yaml           # Kafka/Redpanda configuration
│   └── dapr/
├── mcp-servers/
│   └── todo-mcp/
│       ├── src/
│       │   └── server.py                # MCP server for chatbot integration
│       ├── config/
│       │   └── server.json              # MCP server configuration
│       └── requirements.txt
├── specs/
│   └── 004-advanced-cloud-deployment/   # Feature specifications
│       ├── spec.md
│       ├── plan.md
│       └── tasks.md
├── docker-compose.yml                   # Local development composition
├── docker-compose.cloud.yml             # Cloud deployment composition
├── .dockerignore
└── README.md
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

The application follows a secure, event-driven, cloud-native architecture:
- **Frontend**: Next.js application with token-based authentication
- **Backend**: FastAPI with JWT authentication middleware and Dapr integration
- **Database**: PostgreSQL with proper foreign key relationships
- **Event Streaming**: Kafka/Redpanda for asynchronous event processing
- **Service Mesh**: Dapr for service-to-service communication and infrastructure abstraction
- **Security**: Layered authentication and authorization with proper validation
- **API Design**: RESTful endpoints with consistent error handling
- **Observability**: Distributed tracing with OpenTelemetry and Prometheus metrics
- **Monitoring**: Health checks and performance monitoring
- **Deployment**: Kubernetes-ready with Helm charts for cloud deployment

## 🔒 Error Handling & Security

The application includes comprehensive error handling and security measures:
- **JWT Validation**: All protected endpoints verify token validity and user permissions
- **User Isolation**: Users can only access and modify their own tasks
- **Input Validation**: All API inputs are validated using Pydantic schemas
- **Database Relationships**: Proper foreign keys and relationships prevent data corruption
- **Secure Operations**: Authentication required for all task operations
- **Spec Compliance**: Follows spec-driven development with comprehensive testing
- **Event Validation**: All Kafka events are validated against schemas before processing
- **Dead Letter Queue**: Failed events are sent to a dead letter queue for manual processing
- **Idempotency**: Event processing is idempotent to handle duplicate messages safely

## 🌐 Advanced API Endpoints

### Task Management (Enhanced)
- `GET /api/v1/tasks` - Get all tasks with filtering, sorting, and pagination
- `POST /api/v1/tasks` - Create a new task (with optional recurrence and reminders)
- `GET /api/v1/tasks/{id}` - Get a specific task
- `PUT /api/v1/tasks/{id}` - Update a task
- `POST /api/v1/tasks/{id}/complete` - Mark task as complete
- `DELETE /api/v1/tasks/{id}` - Delete a task
- `GET /api/v1/tasks/search` - Search tasks by text content

### Chatbot Interaction
- `POST /api/v1/chat` - Natural language interaction with the task management system

### Health and Monitoring
- `GET /health` - Application health check
- `GET /dapr/health` - Dapr sidecar health check
- `GET /metrics` - Prometheus metrics