from src.core import users
from functools import wraps
from flask import abort

def check_permissions(permission):
    """
    Checks if the user has the required permission
    """

    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if not users.has_permissions(permission):
                return abort(403)
            
            return f(*args, **kwargs)
        
        return wrapper
    
    return decorator