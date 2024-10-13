from src.core.database import db
from src.core.models.collection import Collection, PaymentMethod
from src.core.models.team_member import TeamMember
from datetime import datetime
from sqlalchemy.orm import aliased


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

   # Crear alias para la tabla TeamMember para evitar el 'DuplicateAlias'
    if name or last_name:
        team_member_alias_name = aliased(TeamMember)
        team_member_alias_last_name = aliased(TeamMember)

    # Filtro por nombre del receptor del pago (miembro del equipo)
    if name:
        query = query.join(team_member_alias_name, team_member_alias_name.email == Collection.team_member_id).filter(team_member_alias_name.name.ilike(f'%{name}%'))
    
    # Filtro por apellido del receptor del pago (miembro del equipo)
    if last_name:
        query = query.join(team_member_alias_last_name, team_member_alias_last_name.email == Collection.team_member_id).filter(team_member_alias_last_name.last_name.ilike(f'%{last_name}%'))


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


def create_collection(**kwargs):

    payment_type_str = kwargs["payment_method"]  # Captura el string del metodo de pago

    collection = Collection(
        amount=kwargs["amount"],
        payment_date=kwargs["payment_date"],
        payment_method=payment_type_str,
        observations=kwargs.get("observations", ""),
        team_member_id=kwargs["team_member_id"],
        rider_dni=kwargs["rider_dni"],

        # PREGUNTAR TEMA DE LA DEUDA, SI SE GENERA EL COBRO ES POR QUE NO DEBE ESTE COBRO, PERO COMO REGISTRO LO DEMAS QUE DEBE
        # POR MES TENGO QUE TENER UN COBRO CREADO Y CUANDO SE PAGA CAMBIAR EL VALOR DE DEBT?
        debt=False   # cambio el valor de la deuda a false ya que se realizo el pago
    )

    # Agregar el pago a la base de datos
    db.session.add(collection)
    db.session.commit()

    return collection

def find_collection(id):

    collection = Collection.query.get(id)

    return collection


def edit_a_collection(**kwargs):

    collection = find_collection(kwargs["collection_id"])

    if collection:

        collection.rider_dni = kwargs.get('rider_dni', collection.rider_dni)
        collection.team_member_id = kwargs.get('team_member_id', collection.team_member_id)
        collection.amount = kwargs.get('amount', collection.amount)
        collection.payment_date = datetime.strptime(kwargs.get('payment_date'), '%Y-%m-%d')
        collection.payment_method = kwargs.get('payment_method', collection.payment_method)
        collection.observations = kwargs.get('description', collection.observations)

        db.session.commit()
        return collection
    return None


def delete_a_collection(collection):

    db.session.delete(collection)
    db.session.commit()

    return True


def create_enums_collection():
   # from src.core.models.payment import PaymentType

    PaymentMethod.create(db.engine, checkfirst=True)
