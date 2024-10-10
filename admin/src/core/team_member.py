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

def list_emails_from_trainers_and_handlers(**kwargs):
    """
    List emails from trainers and handlers
    """
    from src.core.models.team_member import TeamMember

    query = TeamMember.query.filter(
    or_(
        TeamMember.job_position == 'TRAINING_TEACHER',
        TeamMember.job_position == 'HANDLER'
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