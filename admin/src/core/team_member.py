from src.core import database

def create_enums():
    from src.core.models.team_member import ProfessionEnum, JobEnum, ConditionEnum

    ProfessionEnum.create(database.db.engine, checkfirst=True)
    JobEnum.create(database.db.engine, checkfirst=True)
    ConditionEnum.create(database.db.engine, checkfirst=True)
