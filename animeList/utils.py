import bcrypt

def set_password(password_raw: str) -> str:
    """Hash the password using bcrypt and return the hash"""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password_raw.encode('utf-8'), salt).decode('utf-8')

def verify_password(password_raw: str, hash: str) -> bool:
    """Verify the password with hash. Return Ture if match"""
    return bcrypt.checkpw(password_raw.encode('utf-8'), hash.encode('utf-8'))