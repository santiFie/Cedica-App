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
    db.session.add(user)
    db.session.commit()
    return user


def find_user_by_email(email):
    user = User.query.filter_by(email = email).first()

    return user


def check_user(email, password):
    user = find_user_by_email(email)

    if user and bcrypt.check_password_hash(user.password, password):
        return user

    return None