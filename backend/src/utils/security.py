import bcrypt
from typing import Optional


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password."""
    # Truncate password to 72 bytes if needed (bcrypt limitation)
    if len(plain_password) > 72:
        plain_password = plain_password[:72]

    # Encode the password and hashed password if they're not already bytes
    if isinstance(plain_password, str):
        plain_password = plain_password.encode('utf-8')
    if isinstance(hashed_password, str):
        hashed_password = hashed_password.encode('utf-8')

    return bcrypt.checkpw(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Generate a hash for the given password."""
    # Truncate password to 72 bytes if needed (bcrypt limitation)
    if len(password) > 72:
        password = password[:72]

    # Encode the password if it's not already bytes
    if isinstance(password, str):
        password = password.encode('utf-8')

    # Generate the hash
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password, salt)

    # Return as string
    return hashed.decode('utf-8')


def validate_email(email: str) -> bool:
    """Validate email format."""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None