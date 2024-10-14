from src.core import database
from datetime import datetime
from flask import flash
from sqlalchemy import or_
from src.core import utils


def create_enums():
    from src.core.models.team_member import ProfessionEnum, JobEnum, ConditionEnum

    ProfessionEnum.create(database.db.engine, checkfirst=True)
    JobEnum.create(database.db.engine, checkfirst=True)
    ConditionEnum.create(database.db.engine, checkfirst=True)

def check_team_member_by_email(email):
    """
    Check if a team member exists by its email
    """
    from src.core.models.team_member import TeamMember

    team_member = TeamMember.query.filter_by(email=email).first()

    return team_member



def create(form):
    """
    Create a new team member
    """
    from src.core.models.team_member import TeamMember

    end_date = form["end_date"]
    if end_date == '':
        end_date = None
    else:
        end_date = utils.string_to_date(end_date)



    initial_date = utils.string_to_date(form["initial_date"])

    if not utils.validate_dates(initial_date, end_date):
        return flash("Las fechas ingresadas no son válidas")

    team_member = TeamMember(
        name=form["name"],
        last_name=form["last_name"],
        dni=form["dni"],
        address=form["address"],
        email=form["email"],
        locality=form["locality"],
        phone=form["phone"],
        initial_date=form["initial_date"],
        end_date=end_date,
        emergency_contact=form["emergency_contact"],
        emergency_phone=form["emergency_phone"],
        health_insurance_id=form["health_insurance_id"],
        condition=form["condition"].upper(),
        job_position=form["job_position"].upper(),
        profession=form["profession"].upper(),
    )

    database.db.session.add(team_member)
    database.db.session.commit()

    return flash("Miembro de equipo creado exitosamente")


def find_team_members(page=1, email=None, name=None, last_name=None, jobs=None, dni=None, sort_by=None):
    from src.core.models.team_member import TeamMember

    per_page = 25

    # consulta general
    query = TeamMember.query

    # Filtros opcionales
    if email:
        query = query.filter(TeamMember.email.ilike(f'%{email}%'))  # búsqueda insensible a mayúsculas
    if name:
        query = query.filter(TeamMember.name.ilike(f'%{name}%'))
    if last_name:
        query = query.filter(TeamMember.last_name.ilike(f'%{last_name}%'))
    if jobs:
        query = query.filter(TeamMember.job_position == jobs)
    if dni:
        query = query.filter(TeamMember.dni.ilike(f'%{dni}%'))

    # Ordenamiento
    if sort_by == 'name_asc':
        query = query.order_by(TeamMember.name.asc())
    elif sort_by == 'name_desc':
        query = query.order_by(TeamMember.name.desc())
    elif sort_by == 'last_name_asc':
        query = query.order_by(TeamMember.last_name.asc())
    elif sort_by == 'last_name_desc':
        query = query.order_by(TeamMember.last_name.desc())
        
    all_team_members = query.count()

    # Si no hay usuarios, aseguramos que page sea 1 y no haya paginación
    if all_team_members == 0:
        return [], 1
    
    max_pages = (all_team_members + per_page - 1) // per_page  # Redondeo hacia arriba
        
    # Aseguramos que page sea al menos 1
    if page < 1:
        page = 1
    
    # Aseguramos que la página solicitada no sea mayor que el número máximo de páginas
    if page > max_pages:
        page = max_pages
        
    offset = (page - 1) * per_page
    team_members = query.offset(offset).limit(per_page).all()

    return team_members, max_pages 

def edit(**kwargs):
    from src.core.models.team_member import TeamMember

    team_member = TeamMember.query.filter_by(email=kwargs['email']).first()

    end_date = kwargs['end_date']
    if(end_date == ''):
        end_date = None
    

    if team_member:
        team_member.name = kwargs['name']
        team_member.last_name = kwargs['last_name']
        team_member.address = kwargs['address']
        team_member.locality = kwargs['locality']
        team_member.phone = kwargs['phone']
        team_member.end_date = end_date
        team_member.emergency_contact = kwargs['emergency_contact']
        team_member.emergency_phone = kwargs['emergency_phone']
        team_member.health_insurance_id = kwargs['health_insurance']
        team_member.condition = kwargs['condition']
        team_member.job_position = kwargs['job_position']
        team_member.profession = kwargs['profession']
        database.db.session.commit()
    return team_member



def list_emails_from_trainers_and_handlers(**kwargs):
    """
    List emails from trainers and handlers
    """
    from src.core.models.team_member import TeamMember

    query = TeamMember.query.filter(
    or_(
        TeamMember.job_position == 'PROFESOR_DE_ENTRENAMIENTO',
        TeamMember.job_position == 'MANEJADOR'
        )
    )

    

    # Ejecutar la consulta y obtener solo los correos electrónicos
    emails = [member.email for member in query.all()]

    return emails

def find_team_member_by_email(email):
    """
    Find a team member by email
    """
    from src.core.models.team_member import TeamMember

    team_member = TeamMember.query.filter_by(email=email).first()

    return team_member
