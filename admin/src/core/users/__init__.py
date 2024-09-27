from src.core.database import db
from src.core.models.users import User


def find_users(page=1):
    # Definimos cuántos registros mostrar por página
    per_page = 25
    # Calculamos el "offset" (cuántos registros saltar) en función de la página actual
    offset = (page - 1) * per_page
    # Realizamos la consulta con el offset y el límite de 25 usuarios
    users = User.query.offset(offset).limit(per_page).all()
    
    return users
