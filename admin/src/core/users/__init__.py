from src.core.database import db
from src.core.models.users import User
from flask import session
from src.core import auth
from src.core.models.users import RolePermission


def find_users(page=1):
   per_page = 25
   total_users = User.query.count()
   
   max_pages = (total_users + per_page - 1) // per_page  # Redondeo hacia arriba
    
    # Aseguramos que la página solicitada no sea mayor que el número máximo de páginas
   if page > max_pages:
     page = max_pages
    
   offset = (page - 1) * per_page
   users = User.query.offset(offset).limit(per_page).all()
    
   return users

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


def user_delete(user_email):
    """
    Deletes a user
    """
    user = auth.find_user_by_email(user_email)
    auth.db.session.delete(user)
    auth.db.session.commit()
    return True


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


