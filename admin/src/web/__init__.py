from flask import Flask
from flask_session import Session
from flask_bcrypt import Bcrypt
from src.web import routes
from src.web import errors
from src.core import database
from src.core.models.riders_and_horsewomen import RiderAndHorsewoman, disability_certificate_enum, disability_type_enum, family_allowance_enum, pension_enum
from src.core.models.health_insurance import HealthInsurance
from src.core.models.team_member import TeamMember, ProfessionEnum, JobEnum, ConditionEnum
from src.core.models.equestrian import Equestrian
from src.core.models.users import User, Role, RolePermission, Permission
from src.core.config import config

session = Session()
bcrypt = Bcrypt()

def create_app(env="development", static_folder="../../static"):
    app = Flask(__name__, static_folder= static_folder)
    # Init configuration
    app.config.from_object(config[env])
    # Init database
    database.init_app(app)
    # Init session
    session.init_app(app)
    # Init bcrypt
    bcrypt.init_app(app)

    # Register routes
    routes.register(app)

    # Error handlers
    errors.register_errors(app)

    @app.cli.command(name="reset-db")
    def reset_db():
        database.reset()

    @app.cli.command(name="reset-model")
    def reset_model():
        database.reset_model(TeamMember)
 

    @app.cli.command(name="users-db")
    def users_db():
        database.seeds()

    return app