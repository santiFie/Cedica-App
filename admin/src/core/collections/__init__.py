from src.core.database import db
from src.core.models.collection import Collection, PaymentMethod
from src.core.models.team_member import TeamMember
from src.core.models.riders_and_horsewomen import RiderAndHorsewoman
from src.core.riders_and_horsewomen import find_rider
from datetime import datetime, timedelta
import locale
from sqlalchemy.orm import aliased
from sqlalchemy import extract


def find_collections(start_date=None, end_date=None, payment_method=None, name=None, last_name=None, order_by='asc', page=1):
    """
    Search for all collections with the given parameters
    """
    
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
    """
    Creates a collection with the given parameters
    """

    payment_type_str = kwargs["payment_method"]  # Captura el string del metodo de pago

    collection = Collection(
        amount=kwargs["amount"],
        payment_date=kwargs["payment_date"],
        payment_method=payment_type_str,
        observations=kwargs.get("observations", ""),
        team_member_id=kwargs["team_member_id"],
        rider_dni=kwargs["rider_dni"],
    )

    # Agregar el pago a la base de datos
    db.session.add(collection)
    db.session.commit()

    # calcular si el rider es deudor, si no lo es le cambio debtor = False
    rider = find_rider(kwargs["rider_dni"])

    if rider:
        has_debt = check_debtor(rider)
        rider.debtor = has_debt
        db.session.commit()

    return collection

def find_collection(id):
    """
    Search for a collection with the given parameter
    """

    collection = Collection.query.get(id)

    return collection


def edit_a_collection(**kwargs):
    """
    Updates a collection with the given parameters
    """

    collection = find_collection(kwargs["collection_id"])

    if collection:

        collection.rider_dni = kwargs.get('rider_dni', collection.rider_dni)
        collection.team_member_id = kwargs.get('team_member_id', collection.team_member_id)
        collection.amount = kwargs.get('amount', collection.amount)
        collection.payment_date = kwargs.get('payment_date')
        collection.payment_method = kwargs.get('payment_method', collection.payment_method)
        collection.observations = kwargs.get('observations', collection.observations)

        db.session.commit()
        return collection
    return None


def delete_a_collection(collection):
    """
    Deletes the collection given by parameter
    """

    db.session.delete(collection)
    db.session.commit()

    return True


def create_enums_collection():
    """
    Creates the enums values for collections
    """
   # from src.core.models.payment import PaymentType

    PaymentMethod.create(db.engine, checkfirst=True)


def find_debtors(start_date=None, end_date=None, dni=None, order_by='asc', page=1):
    """
    Search for all debtors with the given parameters
    """

    per_page = 25

    # me quedo con todos los riders que son deudores
    query = RiderAndHorsewoman.query.filter(RiderAndHorsewoman.debtor == True)
    
     # Filtro por rango de fechas (opcional)
    if start_date:
        query = query.filter(RiderAndHorsewoman.inserted_at >= datetime.strptime(start_date, '%Y-%m-%d'))
    if end_date:
        query = query.filter(RiderAndHorsewoman.inserted_at <= datetime.strptime(end_date, '%Y-%m-%d'))

    # Filtro por DNI (opcional)
    if dni:
        query = query.filter(RiderAndHorsewoman.dni.ilike(f'%{dni}%'))

    # Ordenar por fecha de pago
    if order_by == 'asc':
        query = query.order_by(RiderAndHorsewoman.inserted_at.asc())
    else:
        query = query.order_by(RiderAndHorsewoman.inserted_at.desc())

    # Contar el número total de deudores que cumplen los filtros
    total_debtors = query.count()

    # Si no hay resultados, retornamos una lista vacía y 0 páginas
    if total_debtors == 0:
        return [], 0

    max_pages = (total_debtors + per_page - 1) // per_page  # Redondeo hacia arriba para calcular las páginas

    # Aseguramos que la página solicitada esté dentro del rango válido
    if page < 1:
        page = 1
    
    if page > max_pages:
        page = max_pages

    # Paginación: calculamos el offset y limitamos los resultados
    offset = (page - 1) * per_page
    debtors = query.offset(offset).limit(per_page).all()

    return debtors, max_pages


def check_debtor(rider):
    """
    Checks if the rider given by parameter is a debtor
    """
    # Obtener la fecha actual
    current_date = datetime.now()

    # Si no tiene fecha de inserción, pasamos al siguiente rider
    if not rider.inserted_at:
        return False

    # Calcular la diferencia en meses desde su fecha de inserción hasta el mes actual
    months_diff = (current_date.year - rider.inserted_at.year) * 12 + current_date.month - rider.inserted_at.month

    # Verificar si falta algún pago de cada mes transcurrido
    for month_offset in range(months_diff):
        # Obtener el primer día del mes transcurrido
        first_day_of_month = rider.inserted_at.replace(year=current_date.year, month=current_date.month, day=1)
           
        # Obtener el primer y el último día del mes en formato de fecha completa
        start_of_month = first_day_of_month
        end_of_month = (first_day_of_month + timedelta(days=32)).replace(day=1) - timedelta(days=1)

        # Verificar si existe un pago para ese mes
        existing_payment = Collection.query.filter_by(rider_dni=rider.dni).filter(Collection.payment_date >= start_of_month, Collection.payment_date <= end_of_month).first()

        # Si no hay pago para ese mes, el rider tiene deuda
        if not existing_payment:
            return True

    return False


def calculate_debt(debtor_dni):
    """
    Calculate all debts of the given parameter
    """ 

    # arreglo de meses en Español
    meses = [
        "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
        "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
    ]

    # Obtener la fecha de inserción del rider
    rider = find_rider(debtor_dni)
    insertion_date = rider.inserted_at
    current_date = datetime.now()

    # Lista de los meses que debe
    missing_payments = []

    # Recorrer cada mes desde la fecha de inserción hasta la fecha actual
    # Desde el año y mes de la inserción hasta el año y mes actuales
    current_year = current_date.year
    current_month = current_date.month
    start_year = insertion_date.year
    start_month = insertion_date.month

    # Iterar a través de los meses entre la fecha de inserción y la fecha actual
    for year in range(start_year, current_year + 1):
        # Calcular el rango de meses a iterar para cada año
        start = start_month if year == start_year else 1
        end = current_month if year == current_year else 12

        for month in range(start, end + 1):
            # Verificar si hay cobro para ese mes y año
            payment = (db.session.query(Collection)
                       .filter_by(rider_dni=rider.dni)
                       .filter(extract('month', Collection.payment_date) == month)
                       .filter(extract('year', Collection.payment_date) == year)
                       .first())

            if not payment:
                # obtengo el nombre del mes
                month_name = meses[month - 1]  # Restamos 1 porque el arreglo empieza en 0
                missing_payments.append(f"{month_name} de {year}")

    return missing_payments, rider