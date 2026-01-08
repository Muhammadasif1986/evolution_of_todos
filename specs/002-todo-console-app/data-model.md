# Data Model: Todo In-Memory Python Console App

## Entity: Task

### Attributes
- **id** (int): Unique identifier for the task; auto-incremented
- **title** (str): Required title of the task; min length 1 character
- **description** (str): Optional description of the task; can be empty
- **completed** (bool): Status indicating if task is completed; default False
- **created_at** (datetime): Timestamp when task was created; auto-generated

### Validation Rules
- Title must not be empty or contain only whitespace
- ID must be unique within the application session
- Created timestamp must be set when task is created

### State Transitions
- Pending (completed=False) → Completed (completed=True): When user marks task as complete
- Completed (completed=True) → Pending (completed=False): When user marks task as incomplete

### Relationships
- None (standalone entity for this phase)

## Entity: TodoList

### Attributes
- **tasks** (list[Task]): Collection of Task objects in the list
- **next_id** (int): Counter for generating unique task IDs; auto-incremented

### Validation Rules
- Task IDs must remain unique within the list
- No duplicate tasks allowed

### Relationships
- Contains: 0..* Task entities

## Business Rules
1. A task must have a non-empty title
2. Each task must have a unique ID within the application session
3. Task completion status can be toggled by the user
4. Tasks are stored in memory only during the application session
5. Task descriptions are optional and can be modified after creation