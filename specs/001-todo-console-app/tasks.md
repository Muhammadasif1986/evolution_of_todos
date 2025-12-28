# Implementation Tasks: Todo In-Memory Python Console App

## Feature Overview
Implement a console-based todo application in Python that allows users to manage tasks in memory. The application will provide core functionality for adding, viewing, updating, deleting, and marking tasks as complete through a command-line interface.

## Dependencies
- Python 3.11+
- Built-in Python libraries only (no external dependencies)
- pytest for unit and integration tests

## User Story Priority Order
1. US1 - Add Task to Todo List (P1)
2. US2 - View Task List (P1)
3. US3 - Mark Task as Complete (P2)
4. US4 - Update Task Details (P3)
5. US5 - Delete Task (P3)

## Parallel Execution Examples
- T001-T003 can be done in parallel (setup tasks)
- T007, T008, T009 can be done in parallel (foundational models/services)
- US1 and US2 can be developed in parallel after foundational tasks

## Implementation Strategy
MVP includes US1 and US2 (add and view tasks). Subsequent user stories can be implemented incrementally.

---

## Phase 1: Setup

- [X] T001 Create project structure per implementation plan in src/ directory
- [X] T002 Create tests directory structure per implementation plan
- [X] T003 Create initial requirements.txt or setup.py file (even if no external dependencies)

---

## Phase 2: Foundational

- [X] T004 [P] Create Task model in src/models/task.py with id, title, description, completed status, and created_at timestamp
- [X] T005 [P] Create TodoService interface and implementation in src/services/todo_service.py with add_task, get_all_tasks, get_task, update_task, toggle_task_status, delete_task methods
- [X] T006 [P] Create TaskFactory in src/services/todo_service.py with create_task method
- [X] T007 [P] Create CLI main module in src/cli/main.py with basic application structure
- [X] T008 [P] Create utility functions in src/lib/utils.py for input validation and formatting
- [X] T009 [P] Create unit tests for Task model in tests/unit/test_task.py
- [X] T010 [P] Create unit tests for TodoService in tests/unit/test_todo_service.py

---

## Phase 3: US1 - Add Task to Todo List (P1)

**Story Goal**: A user can create a new task in their todo list by entering a title and optional description.

**Independent Test Criteria**: Can be fully tested by adding a task through the console interface and verifying it appears in the list.

- [X] T011 [P] [US1] Implement add_task method validation in src/services/todo_service.py (title not empty)
- [X] T012 [P] [US1] Implement Task creation with auto-generated ID and timestamp in src/models/task.py
- [X] T013 [US1] Implement add_task functionality in TodoService to store tasks in memory
- [X] T014 [US1] Create console menu option for adding tasks in src/cli/main.py
- [X] T015 [US1] Implement user input handling for task creation in src/cli/main.py
- [X] T016 [P] [US1] Create unit tests for add task functionality in tests/unit/test_todo_service.py
- [X] T017 [US1] Create integration test for adding tasks via CLI in tests/integration/test_cli_integration.py

---

## Phase 4: US2 - View Task List (P1)

**Story Goal**: A user can see all their current tasks in a readable format with status and details.

**Independent Test Criteria**: Can be fully tested by adding tasks and then viewing the list to confirm they appear correctly.

- [X] T018 [P] [US2] Implement get_all_tasks method in src/services/todo_service.py
- [X] T019 [P] [US2] Implement get_task method in src/services/todo_service.py
- [X] T020 [US2] Create console menu option for viewing tasks in src/cli/main.py
- [X] T021 [US2] Implement task display formatting in src/cli/main.py
- [X] T022 [US2] Implement clear differentiation of completed vs pending tasks in display
- [X] T023 [P] [US2] Create unit tests for view task functionality in tests/unit/test_todo_service.py
- [X] T024 [US2] Create integration test for viewing tasks via CLI in tests/integration/test_cli_integration.py

---

## Phase 5: US3 - Mark Task as Complete (P2)

**Story Goal**: A user can mark a task as completed to track their progress.

**Independent Test Criteria**: Can be fully tested by marking a task as complete and then viewing the list to confirm the status has changed.

- [X] T025 [P] [US3] Implement toggle_task_status method in src/services/todo_service.py
- [X] T026 [US3] Create console menu option for marking tasks as complete in src/cli/main.py
- [X] T027 [US3] Implement user input handling for task selection in src/cli/main.py
- [X] T028 [US3] Implement status toggle functionality in src/cli/main.py
- [X] T029 [P] [US3] Create unit tests for mark complete functionality in tests/unit/test_todo_service.py
- [X] T030 [US3] Create integration test for marking tasks via CLI in tests/integration/test_cli_integration.py

---

## Phase 6: US4 - Update Task Details (P3)

**Story Goal**: A user can modify an existing task's title or description.

**Independent Test Criteria**: Can be fully tested by updating a task's details and verifying the changes persist.

- [X] T031 [P] [US4] Implement update_task method in src/services/todo_service.py with validation
- [X] T032 [US4] Create console menu option for updating tasks in src/cli/main.py
- [X] T033 [US4] Implement user input handling for task updates in src/cli/main.py
- [X] T034 [US4] Implement update confirmation and validation in src/cli/main.py
- [X] T035 [P] [US4] Create unit tests for update task functionality in tests/unit/test_todo_service.py
- [X] T036 [US4] Create integration test for updating tasks via CLI in tests/integration/test_cli_integration.py

---

## Phase 7: US5 - Delete Task (P3)

**Story Goal**: A user can remove a task from their list when it's no longer needed.

**Independent Test Criteria**: Can be fully tested by deleting a task and verifying it no longer appears in the list.

- [X] T037 [P] [US5] Implement delete_task method in src/services/todo_service.py
- [X] T038 [US5] Create console menu option for deleting tasks in src/cli/main.py
- [X] T039 [US5] Implement user confirmation for task deletion in src/cli/main.py
- [X] T040 [US5] Implement deletion validation and error handling in src/cli/main.py
- [X] T041 [P] [US5] Create unit tests for delete task functionality in tests/unit/test_todo_service.py
- [X] T042 [US5] Create integration test for deleting tasks via CLI in tests/integration/test_cli_integration.py

---

## Phase 8: Polish & Cross-Cutting Concerns

- [X] T043 Implement error handling for invalid task IDs across all operations
- [X] T044 Implement handling for empty task lists when performing operations
- [X] T045 Add validation for special characters in task titles/descriptions
- [X] T046 Implement graceful handling of user input errors
- [X] T047 Create comprehensive integration tests for all user flows
- [X] T048 Add documentation strings to all public methods
- [X] T049 Create README.md with setup and usage instructions
- [X] T050 Run full test suite and ensure all tests pass
- [X] T051 Perform end-to-end testing of all user stories