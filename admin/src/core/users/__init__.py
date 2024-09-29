from flask import session
from src.core import auth
from src.core.models.users import RolePermission

def get_permissions(user):
    """
    Returns the permissions of the user
    """

    return RolePermission.query.filter_by(role_id = user.role_id).all()

def has_permissions(session, permission):
    """
    Checks if the user has the required permission
    """
    user_email = session.get("user")
    # Get the user
    user = auth.find_user_by_email(user_email)

    # If the user is a system admin, return True
    if(user.system_admin):
        return True
    
    # Get the permissions of the user
    permissions = get_permissions(user)

    return permission in permissions

def edit(**kwargs):
    """
    Edits a user with the given parameters and returns the user
    """
    user = auth.find_user_by_email(kwargs["email"])
    if user:
        user.nickname = kwargs["nickname"]
        user.system_admin = kwargs["system_admin"]
        user.role_id = kwargs["role_id"]
        auth.db.session.commit()
        return user
    return None
    