# Data Model: Advanced Cloud Deployment

## Entity Definitions

### Task
**Description**: A user task with various attributes including recurrence patterns and scheduling information

**Fields**:
- `id` (integer): Unique identifier for the task
- `title` (string): Task title/description
- `description` (string): Detailed task description
- `status` (string): Task status (pending, completed, archived)
- `priority` (string): Task priority level (low, medium, high, urgent)
- `tags` (array): Array of tag strings for categorization
- `due_date` (datetime): Date/time when task is due
- `recurrence_pattern` (object): Pattern for recurring tasks (type, interval, end_date)
- `created_at` (datetime): Timestamp when task was created
- `updated_at` (datetime): Timestamp when task was last updated
- `user_id` (string): ID of the user who owns the task
- `completed_at` (datetime): Timestamp when task was completed (nullable)

**Validation Rules**:
- Title is required and must be 1-200 characters
- Priority must be one of the defined values
- Due date must be in the future if set
- Recurrence pattern must follow defined schema if present

**State Transitions**:
- `pending` → `completed` (when user marks task as done)
- `completed` → `pending` (when user reopens task)
- `pending` → `archived` (when user archives task)
- `completed` → `archived` (when user archives task)

### User
**Description**: System user with authentication and task ownership

**Fields**:
- `id` (string): Unique identifier for the user
- `email` (string): User's email address (unique)
- `name` (string): User's display name
- `created_at` (datetime): Account creation timestamp
- `updated_at` (datetime): Account last update timestamp
- `preferences` (object): User preferences including notification settings

**Validation Rules**:
- Email must be valid and unique
- Name must be 1-100 characters

### Event
**Description**: Structured event message for Kafka-based communication

**Fields**:
- `event_id` (string): Unique event identifier
- `event_type` (string): Type of event (created, updated, completed, deleted, recurring-triggered, reminder-scheduled)
- `task_id` (integer): ID of the associated task (nullable for system events)
- `task_data` (object): Full task object at time of event
- `user_id` (string): ID of the user who triggered the event
- `timestamp` (datetime): When the event occurred
- `source` (string): Component that generated the event

**Validation Rules**:
- Event type must be one of the defined values
- Task data must be a valid task object if task_id is present

### Notification
**Description**: Reminder or alert to be sent to users

**Fields**:
- `id` (string): Unique notification identifier
- `task_id` (integer): ID of the associated task
- `title` (string): Notification title/text
- `due_at` (datetime): When the task is due
- `remind_at` (datetime): When to send the reminder
- `user_id` (string): User to notify
- `notification_type` (string): Type (email, push, sms)
- `status` (string): Status (pending, sent, failed, cancelled)
- `created_at` (datetime): When notification was scheduled
- `sent_at` (datetime): When notification was sent (nullable)

**Validation Rules**:
- Remind_at must be before due_at
- Status must be one of the defined values
- User must exist in the system

## Entity Relationships

```
User (1) -----> (Many) Task
Task (1) -----> (Many) Event (via task events)
Task (1) -----> (Many) Notification (reminders for task)
User (1) -----> (Many) Notification (notifications for user)
```

## Kafka Event Schemas

### Task Event Schema
```json
{
  "event_type": "string (created|updated|completed|deleted|recurring-triggered)",
  "task_id": "integer",
  "task_data": {
    "id": "integer",
    "title": "string",
    "description": "string",
    "status": "string",
    "priority": "string",
    "tags": ["string"],
    "due_date": "datetime (nullable)",
    "recurrence_pattern": "{...} (nullable)",
    "created_at": "datetime",
    "updated_at": "datetime",
    "user_id": "string",
    "completed_at": "datetime (nullable)"
  },
  "user_id": "string",
  "timestamp": "datetime"
}
```

### Reminder Event Schema
```json
{
  "task_id": "integer",
  "title": "string",
  "due_at": "datetime",
  "remind_at": "datetime",
  "user_id": "string"
}
```