# Service Interface Contracts: Todo Console App

## Service: TodoService

### Interface: ITodoService

#### add_task(title: str, description: str = "") -> Task
- **Purpose**: Add a new task to the todo list
- **Input**:
  - title (str): Required task title (min 1 char)
  - description (str): Optional task description
- **Output**: Task object with assigned ID and creation timestamp
- **Errors**:
  - ValueError if title is empty or contains only whitespace
- **Side Effects**: Increments internal ID counter

#### get_all_tasks() -> List[Task]
- **Purpose**: Retrieve all tasks in the todo list
- **Input**: None
- **Output**: List of all Task objects, sorted by ID
- **Errors**: None
- **Side Effects**: None

#### get_task(task_id: int) -> Task
- **Purpose**: Retrieve a specific task by ID
- **Input**: task_id (int): Unique identifier of the task
- **Output**: Task object matching the ID
- **Errors**:
  - ValueError if task with given ID does not exist
- **Side Effects**: None

#### update_task(task_id: int, title: str = None, description: str = None) -> Task
- **Purpose**: Update an existing task's details
- **Input**:
  - task_id (int): Unique identifier of the task to update
  - title (str, optional): New title (if provided)
  - description (str, optional): New description (if provided)
- **Output**: Updated Task object
- **Errors**:
  - ValueError if task with given ID does not exist
  - ValueError if new title is empty or contains only whitespace
- **Side Effects**: None

#### toggle_task_status(task_id: int) -> Task
- **Purpose**: Toggle a task's completion status
- **Input**: task_id (int): Unique identifier of the task
- **Output**: Task object with toggled completion status
- **Errors**:
  - ValueError if task with given ID does not exist
- **Side Effects**: Changes completed status from True to False or False to True

#### delete_task(task_id: int) -> bool
- **Purpose**: Remove a task from the todo list
- **Input**: task_id (int): Unique identifier of the task to delete
- **Output**: True if task was successfully deleted, False otherwise
- **Errors**:
  - ValueError if task with given ID does not exist
- **Side Effects**: Task is removed from internal storage

## Service: TaskFactory

### Interface: ITaskFactory

#### create_task(title: str, description: str = "") -> Task
- **Purpose**: Create a new Task object with proper initialization
- **Input**:
  - title (str): Required task title
  - description (str): Optional task description
- **Output**: New Task object with assigned ID and current timestamp
- **Errors**:
  - ValueError if title is empty or contains only whitespace
- **Side Effects**: None