# Data Model: AI-Powered Todo Chatbot

## Entity Models

### Task Entity
- **Entity Name**: Task
- **Fields**:
  - `task_id`: UUID, Primary Key, Required
  - `user_id`: UUID, Foreign Key to User, Required
  - `task_title`: String, Required, Max Length 255
  - `task_description`: Text, Optional
  - `completed`: Boolean, Default False
  - `created_at`: Timestamp, Auto-generated
  - `updated_at`: Timestamp, Auto-generated
- **Relationships**: Belongs to User, part of Conversation (through messages)
- **Validation Rules**: task_title required, length validation, user_id ownership verification
- **State Transitions**: pending → completed (via complete_task tool)

### Conversation Entity
- **Entity Name**: Conversation
- **Fields**:
  - `conversation_id`: UUID, Primary Key, Required
  - `user_id`: UUID, Foreign Key to User, Required
  - `created_at`: Timestamp, Auto-generated
  - `updated_at`: Timestamp, Auto-generated
- **Relationships**: Belongs to User, has many Messages
- **Validation Rules**: user_id required, ownership verification
- **State Transitions**: active (no explicit state changes)

### Message Entity
- **Entity Name**: Message
- **Fields**:
  - `message_id`: UUID, Primary Key, Required
  - `user_id`: UUID, Foreign Key to User, Required
  - `conversation_id`: UUID, Foreign Key to Conversation, Required
  - `role`: String, Required, Values: "user", "assistant", "tool"
  - `content`: Text, Required
  - `created_at`: Timestamp, Auto-generated
- **Relationships**: Belongs to User and Conversation
- **Validation Rules**: role in allowed values, content required
- **State Transitions**: none (immutable after creation)

### User Entity (Referenced)
- **Entity Name**: User
- **Fields**:
  - `user_id`: UUID, Primary Key, Required
  - (Additional fields managed by Better Auth)
- **Relationships**: Has many Tasks, has many Conversations, has many Messages
- **Validation Rules**: Managed by Better Auth service

## Database Relationships

- **User → Task**: One-to-Many (User has many Tasks)
- **User → Conversation**: One-to-Many (User has many Conversations)
- **User → Message**: One-to-Many (User has many Messages)
- **Conversation → Message**: One-to-Many (Conversation has many Messages)
- **Task → Message**: Many-to-Many (indirect relationship through messages mentioning tasks)

## Indexing Strategy

- **Primary Indexes**: All primary keys are indexed by default (UUID fields)
- **Foreign Key Indexes**: user_id, conversation_id, task_id fields for fast joins
- **Query Optimization**: Index on user_id for user-specific queries, conversation_id for conversation history

## Validation Rules from Requirements

- **Task Creation**: task_title is required and must not be empty
- **Ownership Verification**: All operations verify user_id matches resource owner
- **Role Validation**: Message role must be one of allowed values (user, assistant, tool)
- **Data Integrity**: Foreign key constraints ensure referential integrity
- **Authorization**: All operations require valid authentication token