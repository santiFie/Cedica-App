from src.core.database import db
from src.core.models.users import Permission, User
from flask import session
from src.core import auth
from src.core.models.users import RolePermission, Role


def find_users(page=1, email=None, active=None, role_name=None, sort_by=None, exclude_user=None):
    """
    Search for all users with the given parameters
    """
    per_page = 25

    # consulta general, obtengo todos los usuarios
    query = User.query

    # excluyo el mail del usuario que inicio sesion
    if(exclude_user):
        query = query.filter(User.email != exclude_user)
    

    # Filtros opcionales
    if email:
        query = query.filter(User.email.ilike(f'%{email}%'))  # búsqueda insensible a mayúsculas
    if active is not None:
        query = query.filter(User.active == active)
    if role_name:
        # averiguo el nro de rol por que desde el formulario llega el nombre del rol
        role = Role.query.filter(Role.name == role_name).first()
        if role:
            query = query.filter(User.role_id == role.id)
        else:
            pass 

    # Ordenamiento
    if sort_by == 'email_asc':
        query = query.order_by(User.email.asc())
    elif sort_by == 'email_desc':
        query = query.order_by(User.email.desc())
    elif sort_by == 'inserted_at_asc':
        query = query.order_by(User.inserted_at.asc())
    elif sort_by == 'inserted_at_desc':
        query = query.order_by(User.inserted_at.desc())
        
    total_users = query.count()

    # Si no hay usuarios, aseguramos que page sea 1 y no haya paginación
    if total_users == 0:
        return [], 1
    
    max_pages = (total_users + per_page - 1) // per_page  # Redondeo hacia arriba
        
    # Aseguramos que page sea al menos 1
    if page < 1:
        page = 1
    
    # Aseguramos que la página solicitada no sea mayor que el número máximo de páginas
    if page > max_pages:
        page = max_pages
        
        
    offset = (page - 1) * per_page
    users = query.offset(offset).limit(per_page).all()

    return users, max_pages 


def get_permissions(user):
    """
    Returns the names of the permissions of the user
    """
    permissions = Permission.query.join(RolePermission).filter_by(role_id=user.role_id).all()
    return [permission.name for permission in permissions]

def has_permissions(session, permission):
    """
    Checks if the user has the required permission
    """
    user_email = session.get("user")
    # Get the user
    user = auth.find_user_by_email(user_email)

    if(user):
        # If the user is a system admin, return True
        if(user.system_admin):
            return True
        
        # Get the permissions of the user
        permissions = get_permissions(user)

        return permission in permissions
    else:
        return False


def user_delete(user_email):
    """
    Deletes a user
    """
    print(user_email)
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
        db.session.commit()
        return user
    return None

def switch_state(user_email):
    """
    If the user given by parameter id admin, then can change the state of a user
    """

    user = auth.find_user_by_email(user_email)

    ##Chequeo que no se intente desactivar un system admin
    if(user.system_admin):
        return False
    

    if user.active:
        user.active = False
    else:
        user.active = True
    db.session.commit()
    ##Devuelvo verdadero si se pudo hacer el cambio
    return True





