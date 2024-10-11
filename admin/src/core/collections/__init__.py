from src.core.database import db
from src.core.models.collection import Collection, PaymentMethod
from src.core.models.team_member import TeamMember
from datetime import datetime


def find_collections(start_date=None, end_date=None, payment_method=None, name=None, last_name=None, order_by='asc', page=1):
    
    per_page = 25

    # query general
    query = Collection.query

    # Filtro por rango de fechas
    if start_date:
        query = query.filter(Collection.payment_date >= datetime.strptime(start_date, '%Y-%m-%d'))
    if end_date:
        query = query.filter(Collection.payment_date <= datetime.strptime(end_date, '%Y-%m-%d'))

    # Filtro por tipo de pago
    if payment_method:
        query = query.filter(Collection.payment_method == payment_method)

    # Filtro por nombre del receptor del pago (miembro del equipo)
    if name:
        query = query.join(TeamMember).filter(TeamMember.first_name.ilike(f'%{name}%'))
    
    # Filtro por apellido del receptor del pago (miembro del equipo)
    if last_name:
        query = query.join(TeamMember).filter(TeamMember.last_name.ilike(f'%{last_name}%'))


    # Ordeno por fecha de pago
    if order_by == 'asc':
        query = query.order_by(Collection.payment_date.asc())
    else:
        query = query.order_by(Collection.payment_date.desc())



    total_collections = query.count()

    # Manejo del caso en el que no haya pagos
    if total_collections == 0:
        return [], 0

    max_pages = (total_collections + per_page - 1) // per_page  # Redondeo hacia arriba

    # Aseguramos que la página solicitada no sea menor que 1
    if page < 1:
        page = 1
        
    # Aseguramos que la página solicitada no sea mayor que el número máximo de páginas
    if page > max_pages:
        page = max_pages
        
        
    offset = (page - 1) * per_page
    collections = query.offset(offset).limit(per_page).all()

    return collections, max_pages 