# Quickstart Guide: Full-Stack Todo Web Application

## Prerequisites

- Node.js 18+ and npm/yarn
- Python 3.11+
- Docker and Docker Compose
- Git
- A Neon Serverless PostgreSQL account

## Environment Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-name>
```

2. Create environment files:
```bash
# Backend
cp backend/.env.example backend/.env

# Frontend
cp frontend/.env.example frontend/.env
```

3. Configure environment variables:
```bash
# In backend/.env
DATABASE_URL="postgresql://username:password@ep-xxxxxx.us-east-1.aws.neon.tech/todo_db"
SECRET_KEY="your-super-secret-key-here"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30

# In frontend/.env
NEXT_PUBLIC_API_URL="http://localhost:8000"
```

## Backend Setup (FastAPI)

1. Navigate to backend directory:
```bash
cd backend
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run database migrations:
```bash
python -m scripts.migrate
```

5. Start the backend server:
```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

The backend API will be available at `http://localhost:8000`.

## Frontend Setup (Next.js)

1. Navigate to frontend directory:
```bash
cd frontend  # From project root
```

2. Install dependencies:
```bash
npm install
# or
yarn install
```

3. Start the development server:
```bash
npm run dev
# or
yarn dev
```

The frontend will be available at `http://localhost:3000`.

## Docker Setup (Recommended)

1. Build and start all services:
```bash
docker-compose up --build
```

2. The services will be available at:
   - Frontend: `http://localhost:3000`
   - Backend: `http://localhost:8000`
   - Database: `postgresql://localhost:5432/todo_db`

## API Documentation

The backend automatically provides API documentation at:
- `http://localhost:8000/docs` (Swagger UI)
- `http://localhost:8000/redoc` (ReDoc)

## Running Tests

### Backend Tests
```bash
cd backend
source venv/bin/activate  # Activate virtual environment
pytest
```

### Frontend Tests
```bash
cd frontend
npm test
# or
yarn test
```

## Database Migrations

To run database migrations:
```bash
cd backend
python -m scripts.migrate
```

To create a new migration:
```bash
cd backend
python -m scripts.create-migration "migration description"
```

## Production Deployment

1. Build the frontend for production:
```bash
cd frontend
npm run build
```

2. Use the production docker-compose file:
```bash
docker-compose -f docker-compose.prod.yml up -d
```

## Troubleshooting

### Common Issues

1. **Port already in use**: Change ports in `.env` files or docker-compose.yml
2. **Database connection errors**: Verify Neon PostgreSQL connection string and credentials
3. **Authentication errors**: Ensure JWT secret keys match between frontend and backend
4. **CORS errors**: Check that frontend URL is included in backend CORS settings

### Reset Development Data

To reset all development data:
```bash
docker-compose down -v  # Removes all data
docker-compose up --build  # Rebuilds with fresh data
```