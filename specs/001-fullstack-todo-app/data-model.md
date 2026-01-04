# Data Model: Full-Stack Todo Web Application

## Entity: User

### Fields
- `id` (UUID): Unique identifier for the user
- `email` (String, unique): User's email address for login
- `username` (String, unique): User's display name
- `hashed_password` (String): BCrypt hashed password
- `first_name` (String, nullable): User's first name
- `last_name` (String, nullable): User's last name
- `is_active` (Boolean): Whether the account is active
- `created_at` (DateTime): Timestamp when account was created
- `updated_at` (DateTime): Timestamp when account was last updated

### Relationships
- One-to-many: User has many TodoItems
- One-to-many: User has many Sessions

### Validation Rules
- Email must be a valid email format
- Email and username must be unique
- Password must meet minimum security requirements (8+ characters)
- Username must not be empty

## Entity: TodoItem

### Fields
- `id` (UUID): Unique identifier for the todo item
- `title` (String): Title/description of the todo item
- `description` (Text, nullable): Detailed description of the task
- `status` (String): Status of the task (pending, in_progress, completed)
- `priority` (String): Priority level (low, medium, high, urgent)
- `due_date` (DateTime, nullable): Deadline for the task
- `created_at` (DateTime): Timestamp when item was created
- `updated_at` (DateTime): Timestamp when item was last updated
- `completed_at` (DateTime, nullable): Timestamp when item was completed
- `user_id` (UUID): Foreign key to User who owns the item

### Relationships
- Many-to-one: TodoItem belongs to one User
- One-to-many: TodoItem has many TodoItemHistory entries (for tracking changes)

### Validation Rules
- Title must not be empty
- Status must be one of: pending, in_progress, completed
- Priority must be one of: low, medium, high, urgent
- Due date must be in the future if provided
- User_id must reference an existing user

## Entity: Session

### Fields
- `id` (UUID): Unique identifier for the session
- `token` (String, unique): JWT token value
- `user_id` (UUID): Foreign key to User
- `expires_at` (DateTime): Expiration timestamp
- `created_at` (DateTime): Timestamp when session was created
- `last_accessed_at` (DateTime): Timestamp of last access
- `is_active` (Boolean): Whether the session is still valid

### Relationships
- Many-to-one: Session belongs to one User

### Validation Rules
- Token must be unique
- Expires_at must be in the future
- User_id must reference an existing user

## Entity: TodoItemHistory

### Fields
- `id` (UUID): Unique identifier for the history entry
- `todo_item_id` (UUID): Foreign key to TodoItem
- `previous_status` (String): Previous status of the item
- `new_status` (String): New status of the item
- `changed_at` (DateTime): Timestamp when change occurred
- `changed_by_user_id` (UUID): User who made the change

### Relationships
- Many-to-one: TodoItemHistory belongs to one TodoItem
- Many-to-one: TodoItemHistory belongs to one User (changer)

### Validation Rules
- Todo_item_id must reference an existing todo item
- New_status must be one of: pending, in_progress, completed
- Changed_at must be current or past timestamp

## State Transitions

### TodoItem Status Transitions
- `pending` → `in_progress`: When user starts working on the task
- `in_progress` → `completed`: When user finishes the task
- `in_progress` → `pending`: When user decides to postpone the task
- `completed` → `pending`: When user needs to reopen the task

### User Account States
- `active` → `inactive`: When account is deactivated
- `inactive` → `active`: When account is reactivated

## Indexes

### Required Indexes
- User.email: For efficient login lookups
- User.username: For efficient username lookups
- TodoItem.user_id: For efficient user todo queries
- TodoItem.status: For efficient filtering by status
- TodoItem.due_date: For efficient sorting by due date
- TodoItem.created_at: For efficient chronological queries
- Session.token: For efficient session validation
- Session.expires_at: For efficient session cleanup