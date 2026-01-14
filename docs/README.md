# Full-Stack Todo Web Application

## Overview
A full-stack todo application built with FastAPI (backend) and Next.js (frontend), featuring user authentication, todo management, and filtering/sorting capabilities.

## Features
- User registration and authentication
- Create, read, update, and delete todo items
- Filter and sort todos by status, priority, and date
- Secure user sessions with JWT tokens
- Responsive UI for desktop and mobile devices

## Architecture
- **Frontend**: Next.js 14+ with TypeScript, Tailwind CSS
- **Backend**: FastAPI with Python 3.11+
- **Database**: Neon Serverless PostgreSQL with SQLModel ORM
- **Authentication**: JWT-based authentication
- **Deployment**: Docker containers with docker-compose

## API Endpoints

### Authentication
- `POST /auth/register` - Register a new user
- `POST /auth/login` - Login to existing account
- `POST /auth/logout` - Logout from current session

### Todo Management
- `GET /todos` - Get all user's todos (with optional filters)
- `POST /todos` - Create a new todo
- `GET /todos/{id}` - Get a specific todo
- `PUT /todos/{id}` - Update a specific todo
- `PATCH /todos/{id}/status` - Update todo status
- `DELETE /todos/{id}` - Delete a specific todo

## Setup Instructions
See the quickstart guide for local development setup instructions.