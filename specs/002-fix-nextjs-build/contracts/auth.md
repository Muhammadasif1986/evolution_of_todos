# Auth API Contracts

## Endpoints

### POST `/v1/auth/login`
Authenticates a user and returns a JWT token.

**Request Body**:
```json
{
  "email": "user@example.com",
  "password": "securepassword"
}
```

**Response**:
```json
{
  "access_token": "jwt_token_string",
  "token_type": "bearer",
  "user": {
    "id": "uuid",
    "email": "user@example.com",
    "username": "user123",
    "first_name": "John",
    "last_name": "Doe",
    "created_at": "timestamp",
    "updated_at": "timestamp"
  }
}
```

### POST `/v1/auth/register`
Registers a new user.

**Request Body**:
```json
{
  "email": "user@example.com",
  "username": "user123",
  "password": "securepassword",
  "first_name": "John",
  "last_name": "Doe"
}
```

**Response**:
```json
{
  "id": "uuid",
  "email": "user@example.com",
  "username": "user123",
  "first_name": "John",
  "last_name": "Doe",
  "created_at": "timestamp",
  "updated_at": "timestamp"
}
```

### GET `/v1/auth/me`
Retrieves the currently authenticated user profile.

**Headers**:
- `Authorization: Bearer <token>`

**Response**:
```json
{
  "id": "uuid",
  "email": "user@example.com",
  "username": "user123",
  "first_name": "John",
  "last_name": "Doe",
  "created_at": "timestamp",
  "updated_at": "timestamp"
}
```
