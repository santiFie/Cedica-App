from src.core.database import db
from src.core.models.users import User

from src.core.bcrypt import bcrypt

def create_user(**kwargs):
    """
    Creates a user with the given parameters
    """
    hash = bcrypt.generate_password_hash(kwargs["password"].encode("utf-8"))
    kwargs["password"] = hash.decode("utf-8")
    user = User(**kwargs)
    try:
        db.session.add(user)
    except:
        db.session.rollback()
        return None
    
    db.session.commit()
    return user


def find_user_by_email(email):
    """
    Search a user with the given parameter
    """
    user = User.query.filter_by(email = email).first()

    return user

def find_user_by_id(id):
    """
    Search a user with the given parameter
    """
    user = User.query.filter_by(id = id).first()
    return user

def user_is_active(user):
    """
    Return the state of the user given by parameter
    """
    return user.active

def check_user(email, password):
    """
    Checks and returns the user if the given parameters are correct
    """
    user = find_user_by_email(email)

    if user and bcrypt.check_password_hash(user.password, password):
        return user

    return None