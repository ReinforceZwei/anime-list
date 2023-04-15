import bcrypt
from time import time

def set_password(password_raw: str) -> str:
    """Hash the password using bcrypt and return the hash"""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password_raw.encode('utf-8'), salt).decode('utf-8')

def verify_password(password_raw: str, hash: str) -> bool:
    """Verify the password with hash. Return Ture if match"""
    return bcrypt.checkpw(password_raw.encode('utf-8'), hash.encode('utf-8'))

def timestamp() -> int:
    """Return current timestamp in seconds"""
    return int(time())

def days_to_seconds(days: int) -> int:
    return days * 86400