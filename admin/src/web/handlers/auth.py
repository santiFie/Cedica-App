from functools import wraps
from flask import session, abort, redirect, url_for, request

def is_authenticated(session):
    return session.get("user") is not None

def login_required(func):

    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not is_authenticated(session):
            if request.path == '/':
                return redirect(url_for('auth.login'))
            else:
                abort(401)

        return func(*args, **kwargs)
    
    return decorated_function