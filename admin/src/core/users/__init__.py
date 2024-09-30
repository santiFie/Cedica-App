from src.core.database import db
from src.core.models.users import User


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
