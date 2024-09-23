from src.core.database import db
from src.core.models.users import User



def find_user_by_email_and_password(email, password):
    user = User.query.filter_by(email = email, password = password).first()

    return user

def create_user(**kwargs):
    user = User(**kwargs)
    db.session.add(user)
    db.session.commit()
    
    return user

