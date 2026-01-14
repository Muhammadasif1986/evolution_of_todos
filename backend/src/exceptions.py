class TodoException(Exception):
    """Base exception for todo application"""
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class UserNotFoundException(TodoException):
    """Raised when user is not found"""
    def __init__(self, user_id: str):
        super().__init__(f"User with id {user_id} not found", 404)


class TodoNotFoundException(TodoException):
    """Raised when todo item is not found"""
    def __init__(self, todo_id: str):
        super().__init__(f"Todo with id {todo_id} not found", 404)


class DuplicateEmailException(TodoException):
    """Raised when trying to create user with existing email"""
    def __init__(self):
        super().__init__("Email already registered", 409)


class UnauthorizedException(TodoException):
    """Raised when user is not authorized"""
    def __init__(self):
        super().__init__("Not authorized", 401)


class InvalidCredentialsException(TodoException):
    """Raised when credentials are invalid"""
    def __init__(self):
        super().__init__("Invalid credentials", 401)