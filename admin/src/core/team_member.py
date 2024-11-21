from src.core import database
from datetime import datetime
from flask import flash
from sqlalchemy import or_
from src.core import utils, minio
from sqlalchemy import func


PREFIX = "team_members"


def create_enums():
    """
    Creates the enums values for the team member
    """
    from src.core.models.team_member import ProfessionEnum, JobEnum, ConditionEnum

    ProfessionEnum.create(database.db.engine, checkfirst=True)
    JobEnum.create(database.db.engine, checkfirst=True)
    ConditionEnum.create(database.db.engine, checkfirst=True)


def create(form, files):
    """
    Create a new team member
    """
    from src.core.models.team_member import TeamMember

    end_date = form["end_date"]
    if end_date == "":
        end_date = None
    else:
        end_date = utils.string_to_date(end_date)

    initial_date = utils.string_to_date(form["initial_date"])

    if not utils.validate_dates(initial_date, end_date):
        return flash("Las fechas ingresadas no son válidas", "error")

    time = datetime.now()
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
        associated_number=form["associated_number"],
        inserted_at=time,
        condition=form["condition"],
        job_position=form["job_position"],
        profession=form["profession"],
    )
    try:
        database.db.session.add(team_member)
        database.db.session.flush()
    except:
        database.db.session.rollback()
        return flash("Error al crear el miembro de equipo", "info")
    try:
        for key, file in files.items():
            if file:
                minio.upload_file(prefix=PREFIX, file=file, user_id=team_member.id)
                setattr(team_member, key, file.filename)

        database.db.session.flush()

    except Exception as e:
        database.db.session.rollback()
        return flash("Error al crear miembro de equipo", "info")

    database.db.session.commit()
    return flash("Miembro de equipo creado exitosamente")


def find_team_members(
    page=1, email=None, name=None, last_name=None, jobs=None, dni=None, sort_by=None
):
    """
    Search for all team members with the given parameters
    """
    from src.core.models.team_member import TeamMember

    per_page = 25

    # General query
    query = TeamMember.query

    # Optional filters
    if email:
        query = query.filter(
            TeamMember.email.ilike(f"%{email}%")
        )  # case-insensitive search
    if name:
        query = query.filter(TeamMember.name.ilike(f"%{name}%"))
    if last_name:
        query = query.filter(TeamMember.last_name.ilike(f"%{last_name}%"))
    if jobs:
        query = query.filter(TeamMember.job_position == jobs)
    if dni:
        query = query.filter(TeamMember.dni.ilike(f"%{dni}%"))

    # Sorting
    if sort_by == "name_asc":
        query = query.order_by(TeamMember.name.asc())
    elif sort_by == "name_desc":
        query = query.order_by(TeamMember.name.desc())
    elif sort_by == "last_name_asc":
        query = query.order_by(TeamMember.last_name.asc())
    elif sort_by == "last_name_desc":
        query = query.order_by(TeamMember.last_name.desc())
    elif sort_by == "inserted_at_asc":
        query = query.order_by(TeamMember.inserted_at.asc())
    elif sort_by == "inserted_at_desc":
        query = query.order_by(TeamMember.inserted_at.desc())

    all_team_members = query.count()

    # If there are no users, ensure page is 1 and there is no pagination
    if all_team_members == 0:
        return [], 1

    max_pages = (all_team_members + per_page - 1) // per_page  # Round up

    # Ensure page is at least 1
    if page < 1:
        page = 1

    # Ensure the requested page is not greater than the maximum number of pages
    if page > max_pages:
        page = max_pages

    offset = (page - 1) * per_page
    team_members = query.offset(offset).limit(per_page).all()

    return team_members, max_pages


def update_team_member_files(team_member, files):
    """
    Updates a team member files with the given parameters
    """

    for key, file in files.items():
        if file:
            minio.delete_file(PREFIX, getattr(team_member, key), team_member.id)
            minio.upload_file(prefix=PREFIX, file=file, user_id=team_member.id)
            setattr(team_member, key, file.filename)


def edit(email, form, files):
    """
    Updates a team member with the given parameters
    """
    from src.core.models.team_member import TeamMember

    team_member = TeamMember.query.filter_by(email=email).first()

    end_date = form["end_date"]
    if end_date == "":
        end_date = None

    if team_member:

        team_member.name = form["name"]
        team_member.last_name = form["last_name"]
        team_member.address = form["address"]
        team_member.locality = form["locality"]
        team_member.phone = form["phone"]
        team_member.end_date = end_date
        team_member.emergency_contact = form["emergency_contact"]
        team_member.emergency_phone = form["emergency_phone"]
        team_member.health_insurance_id = form["health_insurance"]
        team_member.associated_number = form["associated_number"]
        team_member.condition = form["condition"]
        team_member.job_position = form["job_position"]
        team_member.profession = form["profession"]

    update_team_member_files(team_member, files)

    try:
        database.db.session.flush()
    except Exception as e:
        database.db.session.rollback()
        return flash("Error al editar el miembro de equipo")

    database.db.session.commit()
    return team_member


def list_emails_from_trainers_and_handlers(**kwargs):
    """
    List emails from trainers and handlers
    """
    from src.core.models.team_member import TeamMember

    query = TeamMember.query.filter(
        or_(
            TeamMember.job_position == "Profesor de entrenamiento",
            TeamMember.job_position == "Manejador",
        ),
        TeamMember.active == True
    )

    # Execute the query and get only the emails
    emails = [member.email for member in query.all()]

    return emails


def find_team_member_by_email(email):
    """
    Find a team member by email
    """
    from src.core.models.team_member import TeamMember

    team_member = TeamMember.query.filter_by(email=email).first()

    return team_member


def get_all():
    """
    Search for all the team members
    """
    from src.core.models.team_member import TeamMember

    team_members = TeamMember.query.filter_by(active=True).all()

    return team_members


def get_all_therapists():
    """
    Search for all team members who are therapists
    """
    from src.core.models.team_member import TeamMember

    therapists = TeamMember.query.filter_by(job_position="Terapeuta", active=True).all()

    return therapists


def get_all_riders():
    """
    Search for all team members who are horse handlers
    """
    from src.core.models.team_member import TeamMember

    riders = TeamMember.query.filter_by(job_position="Manejador", active=True).all()

    return riders


def get_all_track_assistants():
    """
    Search for all team members who are track assistants
    """
    from src.core.models.team_member import TeamMember

    track_assistants = TeamMember.query.filter_by(
        job_position="Asistente de pista", 
        active=True
    ).all()

    return track_assistants


def find_team_member_by_id(id):
    """
    Search for the team member with the given parameter
    """
    from src.core.models.team_member import TeamMember

    team_member = TeamMember.query.filter_by(id=id).first()

    return team_member


def switch_state(team_member):
    """
    Switch the state of the team member given by parameter
    """

    if team_member.active == False:
        team_member.active = True
        team_member.end_date = None
    else:
        team_member.active = False
        team_member.end_date = datetime.now()
    database.db.session.commit()
    return team_member


def check_dni_exist(dni):
    """
    Checks if a team member with the given parameter exists
    """
    from src.core.models.team_member import TeamMember

    team_member_dni = TeamMember.query.filter_by(dni=dni).first()

    return team_member_dni

def get_ranking_jobs():
    from src.core.models.team_member import TeamMember
    jobs = (
        database.db.session.query(
            TeamMember.job_position,
            func.count(TeamMember.job_position).label('cant')
        )
        .group_by(TeamMember.job_position)
        .order_by(func.count(TeamMember.job_position).desc())  
    )

    return jobs
