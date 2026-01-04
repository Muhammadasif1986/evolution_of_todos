#!/bin/bash

# Setup script for Full-Stack Todo Web Application

echo "Setting up Full-Stack Todo Web Application..."

# Setup backend
echo "Setting up backend..."
cd backend
if [ ! -f ".env" ]; then
    echo "Creating backend .env file..."
    cat > .env << EOF
DATABASE_URL=postgresql://todo_user:todo_password@localhost:5432/todo_db
SECRET_KEY=your-super-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
FRONTEND_URL=http://localhost:3000
EOF
fi

# Setup frontend
echo "Setting up frontend..."
cd ../frontend
if [ ! -f ".env" ]; then
    echo "Creating frontend .env file..."
    cat > .env << EOF
NEXT_PUBLIC_API_URL=http://localhost:8000
EOF
fi

echo "Setup complete!"
echo ""
echo "To run the application:"
echo "1. Start backend: cd backend && uvicorn src.main:app --reload"
echo "2. Start frontend: cd frontend && npm run dev"
echo ""
echo "Or use Docker: cd docker && docker-compose up --build"