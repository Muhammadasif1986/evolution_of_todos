# Data Model: Fix Next.js Build Errors

## Entities

### User
Represents an authenticated user in the system. Required for `AuthContext` and `authService` type safety.

- **id**: string (UUID)
- **email**: string
- **username**: string
- **first_name**: string (optional)
- **last_name**: string (optional)
- **created_at**: string (ISO Date)
- **updated_at**: string (ISO Date)

## Validation Rules
- `User` object must be provided by the backend `/auth/me` endpoint.
- Type definitions in `src/types/todo.ts` must align with backend response structures.

## Relationships
- `TodoItem` belongs to a `User` via `user_id`.
