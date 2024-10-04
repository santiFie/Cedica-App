from src.core import database

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

def create(**kwargs):
    """
    Create a new team member
    """
    from src.core.models.team_member import TeamMember

    team_member = TeamMember(
        name=kwargs.get('name'),
        last_name=kwargs.get('last_name'),
        address=kwargs.get('address'),
        email=kwargs.get('email'),
        locality=kwargs.get('locality'),
        phone=kwargs.get('phone'),
        initial_date=kwargs.get('initial_date'),
        end_date=kwargs.get('end_date'),
        emergency_contact=kwargs.get('emergency_contact'),
        emergency_phone=kwargs.get('emergency_phone'),
        active=kwargs.get('active'),
        health_insurance_id=kwargs.get('health_insurance_id'),
        condition = kwargs.get('condition').upper(),
        job_position = kwargs.get('job').upper(),
        proffesion = kwargs.get('profession').upper(),

    )

    database.db.session.add(team_member)
    database.db.session.commit()

    return team_member