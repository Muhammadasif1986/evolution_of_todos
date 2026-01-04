# API Documentation

## Authentication Endpoints

### Register User
```
POST /auth/register
```

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securePassword123",
  "username": "username"
}
```

**Response:**
```json
{
  "id": "user_id",
  "email": "user@example.com",
  "username": "username",
  "created_at": "2023-01-01T00:00:00Z"
}
```

### Login User
```
POST /auth/login
```

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securePassword123"
}
```

**Response:**
```json
{
  "access_token": "jwt_token_here",
  "token_type": "bearer"
}
```

## Todo Endpoints

### Get All Todos
```
GET /todos
```

**Query Parameters:**
- `status`: Filter by status (pending, completed)
- `priority`: Filter by priority (low, medium, high)
- `sort`: Sort by field (due_date, created_at, priority)
- `limit`: Number of results to return
- `offset`: Number of results to skip

**Response:**
```json
[
  {
    "id": "todo_id",
    "title": "Todo title",
    "description": "Todo description",
    "status": "pending",
    "priority": "medium",
    "due_date": "2023-01-01T00:00:00Z",
    "created_at": "2023-01-01T00:00:00Z",
    "updated_at": "2023-01-01T00:00:00Z",
    "user_id": "user_id"
  }
]
```

### Create Todo
```
POST /todos
```

**Request Body:**
```json
{
  "title": "Todo title",
  "description": "Todo description",
  "priority": "medium",
  "due_date": "2023-01-01T00:00:00Z"
}
```

**Response:**
```json
{
  "id": "todo_id",
  "title": "Todo title",
  "description": "Todo description",
  "status": "pending",
  "priority": "medium",
  "due_date": "2023-01-01T00:00:00Z",
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-01T00:00:00Z",
  "user_id": "user_id"
}
```

### Update Todo
```
PUT /todos/{id}
```

**Request Body:**
```json
{
  "title": "Updated title",
  "description": "Updated description",
  "priority": "high",
  "due_date": "2023-01-01T00:00:00Z"
}
```

**Response:**
```json
{
  "id": "todo_id",
  "title": "Updated title",
  "description": "Updated description",
  "status": "pending",
  "priority": "high",
  "due_date": "2023-01-01T00:00:00Z",
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-01T00:00:00Z",
  "user_id": "user_id"
}
```

### Update Todo Status
```
PATCH /todos/{id}/status
```

**Request Body:**
```json
{
  "status": "completed"
}
```

**Response:**
```json
{
  "id": "todo_id",
  "status": "completed"
}
```

### Delete Todo
```
DELETE /todos/{id}
```

**Response:**
```
Status: 204 No Content
```