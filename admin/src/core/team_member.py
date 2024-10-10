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

def validate_dates(initial_date, end_date):
    """
    Check if the dates are valid
    """
    initial_date = datetime.strptime(initial_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d') if end_date is not None else None

    print(type(initial_date))
    if initial_date > datetime.now():
        return False

    if end_date is not None:
        if initial_date > end_date:
            return False

    return True

def create(form):
    """
    Create a new team member
    """
    from src.core.models.team_member import TeamMember

    end_date = form["end_date"]
    if end_date == '':
        end_date = None

    if not validate_dates(form["initial_date"], end_date):
        return flash("Las fechas ingresadas no son válidas")

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