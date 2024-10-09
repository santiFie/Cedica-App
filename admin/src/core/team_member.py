from src.core import database
from datetime import datetime
from flask import flash

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

    #if not validate_dates(form["initial_date"], end_date):
    #    return flash("Las fechas no son válidas")

    team_member = TeamMember(
        name=form["name"],
        last_name=form["last_name"],
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


def find_team_members(page=1):
    from src.core.models.team_member import TeamMember

    per_page = 25
    total_team_members = TeamMember.query.count()
   
    # Calcula el número máximo de páginas (redondeo hacia arriba)
    max_pages = (total_team_members + per_page - 1) // per_page
    
    # Aseguramos que la página solicitada esté dentro de los límites
    if page < 1:
        page = 1
    elif page > max_pages:
        page = max_pages
    
    offset = (page - 1) * per_page
    
    # Si no hay miembros de equipo, devolver una lista vacía
    if total_team_members == 0:
        return []
    
    team_members = TeamMember.query.offset(offset).limit(per_page).all()
    
    return team_members