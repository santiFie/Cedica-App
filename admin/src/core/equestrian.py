from src.core import database   
from src.core.models.equestrian import Equestrian


db = database.db

def equestrian_create(**kwargs):
    """
    Creates a new equestrian
    """
    equestrian = Equestrian(**kwargs)
    db.session.add(equestrian)
    db.session.commit()
    return equestrian