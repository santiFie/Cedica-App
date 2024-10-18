from src.core import users
from functools import wraps
from flask import abort
from flask import session

def check_permissions(permission):
    """
    Checks if the user has the required permission
    """

    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if not users.has_permissions(session,permission):
                return abort(403)
            
            return f(*args, **kwargs)
        
        return wrapper
    
    return decorator