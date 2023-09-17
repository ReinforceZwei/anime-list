from typing import Dict
import bcrypt
from time import time
import jwt

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

def str2bool(x: str) -> bool:
    return str(x).lower() in ("true", "t", "1")

def generate_access_token(jwt_key: str, id: int, name: str, password: str) -> str:
    jwt_payload = {
        'id': id,
        'name': name,
        'sub': 'access',
        'iat': timestamp(),
        'exp': timestamp()+days_to_seconds(3)
    }
    return jwt.encode(jwt_payload, jwt_key + password, algorithm='HS256')

def generate_refresh_token(jwt_key: str, id: int, name: str, password: str) -> str:
    jwt_payload = {
        'id': id,
        'name': name,
        'sub': 'refresh',
        'iat': timestamp(),
        'exp': timestamp()+days_to_seconds(30)
    }
    return jwt.encode(jwt_payload, jwt_key + password, algorithm='HS256')

def decode_user_token_no_verify(token: str) -> Dict:
    return jwt.decode(token, '', ['HS256'], options={"verify_signature": False})

def decode_user_token(jwt_key: str, password: str, token: str) -> Dict:
    return jwt.decode(token, jwt_key + password, ['HS256'])

def generate_update_sql(table_name: str, key_value_map: Dict, where_clause: str = None) -> str:
    sql = 'UPDATE `{}` SET {}'.format(table_name, ', '.join('`{}`=%s'.format(k) for k in key_value_map))
    if where_clause is not None:
        sql = '{} WHERE {}'.format(sql, where_clause.strip())
    return sql