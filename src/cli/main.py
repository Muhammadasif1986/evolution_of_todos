'''
Main CLI module for the Todo Console App
'''
import sys
import os
from typing import Optional

# Add the project root to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.services.todo_service import TodoService


class TodoCLI:
    """
    Console interface and menu system for the Todo Console App.
    """

    def __init__(self):
        """Initialize the CLI with a TodoService instance."""
        self.service = TodoService()
        self.running = True

    def display_menu(self):
        """Display the main menu options."""
        print("\n" + "="*50)
        print("TODO CONSOLE APPLICATION")
        print("="*50)
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Mark Task Complete/Incomplete")
        print("4. Update Task")
        print("5. Delete Task")
        print("6. Exit")
        print("="*50)

    def get_user_choice(self) -> str:
        """Get and validate user menu choice."""
        try:
            choice = input("Enter your choice (1-6): ").strip()
            if choice in ['1', '2', '3', '4', '5', '6']:
                return choice
            else:
                print("Invalid choice. Please enter a number between 1 and 6.")
                return None
        except (EOFError, KeyboardInterrupt):
            print("\nExiting application...")
            return '6'  # Treat as exit choice

    def add_task(self):
        """Handle adding a new task."""
        print("\n--- Add New Task ---")
        try:
            title = input("Enter task title: ").strip()
            if not title:
                print("Task title cannot be empty.")
                return

            description = input("Enter task description (optional, press Enter to skip): ").strip()
            if not description:  # If empty, use empty string
                description = ""

            task = self.service.add_task(title, description)
            print(f"Task added successfully! ID: {task.id}, Title: {task.title}")
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def view_tasks(self):
        """Handle viewing all tasks."""
        print("\n--- Task List ---")
        try:
            tasks = self.service.get_all_tasks()
            if not tasks:
                print("No tasks found.")
                return

            for task in tasks:
                status = "✓" if task.completed else "○"
                print(f"[{status}] ID: {task.id} | Title: {task.title}")
                if task.description:
                    print(f"    Description: {task.description}")
                print(f"    Created: {task.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
                print("-" * 40)
        except Exception as e:
            print(f"An error occurred while retrieving tasks: {e}")

    def toggle_task_status(self):
        """Handle marking a task as complete/incomplete."""
        print("\n--- Toggle Task Status ---")
        try:
            task_id_str = input("Enter task ID to toggle status: ").strip()
            if not task_id_str:
                print("Task ID cannot be empty.")
                return

            try:
                task_id = int(task_id_str)
            except ValueError:
                print("Invalid task ID. Please enter a number.")
                return

            task = self.service.toggle_task_status(task_id)
            status = "completed" if task.completed else "pending"
            print(f"Task '{task.title}' marked as {status}.")
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def update_task(self):
        """Handle updating an existing task."""
        print("\n--- Update Task ---")
        try:
            task_id_str = input("Enter task ID to update: ").strip()
            if not task_id_str:
                print("Task ID cannot be empty.")
                return

            try:
                task_id = int(task_id_str)
            except ValueError:
                print("Invalid task ID. Please enter a number.")
                return

            # Get current task to show current values
            current_task = self.service.get_task(task_id)
            print(f"Current title: {current_task.title}")
            print(f"Current description: {current_task.description}")

            new_title = input(f"Enter new title (press Enter to keep '{current_task.title}'): ").strip()
            if new_title == "":  # If user pressed Enter without typing
                new_title = None  # Use None to indicate no change
            elif not new_title:  # If user entered only whitespace
                print("Task title cannot be empty or contain only whitespace.")
                return

            new_description = input(f"Enter new description (press Enter to keep '{current_task.description}'): ").strip()
            if new_description == "":  # If user pressed Enter without typing
                new_description = None  # Use None to indicate no change

            # Perform update
            updated_task = self.service.update_task(task_id, new_title, new_description)
            print(f"Task updated successfully! ID: {updated_task.id}, Title: {updated_task.title}")
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def delete_task(self):
        """Handle deleting a task."""
        print("\n--- Delete Task ---")
        try:
            task_id_str = input("Enter task ID to delete: ").strip()
            if not task_id_str:
                print("Task ID cannot be empty.")
                return

            try:
                task_id = int(task_id_str)
            except ValueError:
                print("Invalid task ID. Please enter a number.")
                return

            # Confirm deletion
            try:
                task = self.service.get_task(task_id)
                confirm = input(f"Are you sure you want to delete task '{task.title}'? (y/N): ").strip().lower()
                if confirm not in ['y', 'yes']:
                    print("Deletion cancelled.")
                    return
            except ValueError:
                print(f"Task with ID {task_id} does not exist.")
                return

            self.service.delete_task(task_id)
            print(f"Task '{task.title}' deleted successfully.")
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def run(self):
        """Main application loop."""
        print("Welcome to the Todo Console Application!")

        while self.running:
            self.display_menu()
            choice = self.get_user_choice()

            if choice == '1':
                self.add_task()
            elif choice == '2':
                self.view_tasks()
            elif choice == '3':
                self.toggle_task_status()
            elif choice == '4':
                self.update_task()
            elif choice == '5':
                self.delete_task()
            elif choice == '6':
                print("Thank you for using the Todo Console Application. Goodbye!")
                self.running = False


def main():
    """Entry point for the application."""
    app = TodoCLI()
    app.run()


if __name__ == "__main__":
    main()