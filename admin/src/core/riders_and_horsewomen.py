from src.core.database import db
from src.core.models.riders_and_horsewomen import RiderAndHorsewoman
from sqlalchemy.orm import aliased


def create_enums():
    from src.core.models.riders_and_horsewomen import disability_certificate_enum, disability_type_enum, family_allowance_enum, pension_enum, days_enum, condition_enum, seat_enum, proposal_enum, education_level_enum

    disability_certificate_enum.create(db.engine, checkfirst=True)
    disability_type_enum.create(db.engine, checkfirst=True)
    family_allowance_enum.create(db.engine, checkfirst=True)
    pension_enum.create(db.engine, checkfirst=True)
    days_enum.create(db.engine, checkfirst=True)
    condition_enum.create(db.engine, checkfirst=True)
    seat_enum.create(db.engine, checkfirst=True)
    proposal_enum.create(db.engine, checkfirst=True)
    education_level_enum.create(db.engine, checkfirst=True)


def find_rider(dni):

    rider = RiderAndHorsewoman.query.filter_by(dni=dni).first()

    return rider


# FALTA EL PARAM Y FILTRO DE PROFESIONALES QUE LO ATIENDEN !!!!!!!!!!
def find_all_riders(name=None, last_name=None, dni=None, order_by='asc', page=1):

    per_page = 25

    query = RiderAndHorsewoman.query

    # Filtro por DNI
    if dni:
        query = query.filter(RiderAndHorsewoman.dni == dni)

    if name or last_name:
        # para poder buscar por ambos campos al mismo tiempo 
        rider_alias_name = aliased(RiderAndHorsewoman)
        rider_alias_last_name = aliased(RiderAndHorsewoman)

        # Filtro por nombre del rider
        if name:
            query = query.filter(rider_alias_name.name.ilike(f'%{name}%'))
        
        # Filtro por apellido del rider
        if last_name:
            query = query.filter(rider_alias_last_name.last_name.ilike(f'%{last_name}%'))

    

    # Ordeno por el campo adecuado
    if order_by == 'asc':
        query = query.order_by(RiderAndHorsewoman.name.asc())  # Puedes cambiarlo por el campo adecuado
    else:
        query = query.order_by(RiderAndHorsewoman.name.desc())  # Puedes cambiarlo por el campo adecuado

    total_riders = query.count()

    # Manejo del caso en el que no haya jinetes
    if total_riders == 0:
        return [], 0

    max_pages = (total_riders + per_page - 1) // per_page  # Redondeo hacia arriba

    # Aseguramos que la página solicitada no sea menor que 1
    if page < 1:
        page = 1

    # Aseguramos que la página solicitada no sea mayor que el número máximo de páginas
    if page > max_pages:
        page = max_pages

    offset = (page - 1) * per_page
    riders = query.offset(offset).limit(per_page).all()

    return riders, max_pages



def delete_a_rider(rider):

    db.session.delete(rider)
    db.session.commit()

    return True



