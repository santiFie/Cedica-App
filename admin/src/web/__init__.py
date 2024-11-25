from flask import Flask
from flask_session import Session
from flask_bcrypt import Bcrypt
from src.web.storage import storage
from src.web.oauth import configure_oauth
from src.web import routes
from src.web import errors
from src.core import database
from src.core.models.post import Post
from src.core.models.riders_and_horsewomen import RiderAndHorsewoman, File, disability_certificate_enum, disability_type_enum, family_allowance_enum, pension_enum
from src.core.models.health_insurance import HealthInsurance
from src.core.models.team_member import TeamMember, ProfessionEnum, JobEnum, ConditionEnum
from src.core.models.equestrian import Equestrian
from src.core.models.users import User, Role, RolePermission, Permission
from src.core.users import has_permissions
from src.core.utils import is_link
from src.core.config import config
from os import environ, urandom
from flask_cors import CORS
import os

session = Session()
bcrypt = Bcrypt()


def create_app(env="production", static_folder="../../static"):
    app = Flask(__name__, static_folder= static_folder)
    # Init secret key for session
    app.secret_key = environ.get("SECRET_KEY") or urandom(24)

    # configure CORS
    CORS(app)

    # Init configuration
    app.config.from_object(config[env])

    # Init database
    database.init_app(app)
    # Init session
    session.init_app(app)
    # Init bcrypt
    bcrypt.init_app(app)
    # Init storage
    storage.init_app(app)
    # Register routes
    routes.register(app)
    # Init OAuth
    configure_oauth(app)
    # Error handlers
    errors.register_errors(app)
    
    app.jinja_env.globals.update(check_permissions=has_permissions)
    app.jinja_env.globals.update(is_link=is_link)

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

