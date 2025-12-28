# Todo Console Application

A simple console-based todo application implemented in Python that allows users to manage tasks in memory.

## Features

- Add new tasks with titles and optional descriptions
- View all tasks with their completion status
- Mark tasks as complete/incomplete
- Update existing task details
- Delete tasks from the list
- In-memory storage (tasks persist only during the session)

## Requirements

- Python 3.11+
- No external dependencies required (using built-in libraries only)
- Optional: pytest for running tests

## Installation

1. Clone the repository or download the source code
2. Ensure you have Python 3.11+ installed
3. Install optional dependencies for testing:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

To run the application:

```bash
python src/cli/main.py
```

Follow the on-screen menu prompts to manage your tasks:
- **1**: Add Task - Create a new task with title and optional description
- **2**: View Tasks - Display all tasks with their status and details
- **3**: Mark Task Complete/Incomplete - Toggle the completion status of a task
- **4**: Update Task - Modify an existing task's title or description
- **5**: Delete Task - Remove a task from the list with confirmation
- **6**: Exit - Quit the application

## Project Structure

```
src/
├── models/
│   └── task.py          # Task model with ID, title, description, completed status
├── services/
│   └── todo_service.py  # Core business logic for task management
├── cli/
│   └── main.py          # Console interface and menu system
└── lib/
    └── utils.py         # Helper functions

tests/
├── unit/
│   ├── test_task.py     # Unit tests for Task model
│   └── test_todo_service.py  # Unit tests for TodoService
├── integration/
│   └── test_cli_integration.py  # Integration tests for CLI flow
└── contract/
    └── test_api_contract.py  # Contract tests (if API endpoints added later)
```

## Testing

To run the unit tests:

```bash
pytest tests/unit/
```

To run the integration tests:

```bash
pytest tests/integration/
```

To run all tests:

```bash
pytest tests/
```

## Architecture

The application follows a layered architecture:
- **Models**: Define the data structures (Task)
- **Services**: Implement the business logic (TodoService)
- **CLI**: Handle user interface and input/output
- **Lib**: Provide utility functions

## Error Handling

The application includes comprehensive error handling:
- Validation of task titles (must not be empty)
- Proper handling of invalid task IDs
- User confirmation for destructive operations
- Graceful handling of input errors