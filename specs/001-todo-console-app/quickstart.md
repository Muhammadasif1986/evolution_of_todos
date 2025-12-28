# Quickstart Guide: Todo Console App

## Getting Started

### Prerequisites
- Python 3.11 or higher
- No additional dependencies required

### Running the Application

1. **Clone or navigate to the project directory**
   ```bash
   cd /path/to/evolution-of-todo
   ```

2. **Run the console application**
   ```bash
   python src/cli/main.py
   ```

3. **Follow the on-screen menu prompts**
   - The application will display a numbered menu of available operations
   - Enter the number corresponding to your desired action
   - Follow the prompts to provide required information

## Basic Operations

### Adding a Task
1. Select "Add Task" from the main menu
2. Enter the task title when prompted
3. Optionally enter a description when prompted
4. The system will confirm the task has been added

### Viewing Tasks
1. Select "View Tasks" from the main menu
2. All tasks will be displayed with their ID, title, description, and completion status
3. Completed tasks will be marked with a checkmark

### Marking a Task Complete
1. Select "Mark Task Complete" from the main menu
2. Enter the task ID when prompted
3. The system will toggle the completion status of the task

### Updating a Task
1. Select "Update Task" from the main menu
2. Enter the task ID when prompted
3. Enter the new title and/or description when prompted
4. The system will confirm the update

### Deleting a Task
1. Select "Delete Task" from the main menu
2. Enter the task ID when prompted
3. Confirm the deletion when prompted
4. The system will confirm the task has been deleted

## Error Handling

- If you enter invalid input, the system will display an error message and prompt you again
- If you try to access a non-existent task, the system will inform you that the task was not found
- Empty task lists will be clearly indicated

## Development

### Running Tests
```bash
pytest tests/
```

### Project Structure
- `src/models/task.py`: Task model definition
- `src/services/todo_service.py`: Core business logic
- `src/cli/main.py`: Console interface and menu system
- `tests/`: Unit and integration tests

## Troubleshooting

- **"Command not found"**: Ensure you're running Python from the correct directory
- **"Module not found"**: Make sure you're running the application from the project root
- **"Invalid input"**: Follow the exact format requested by the prompts