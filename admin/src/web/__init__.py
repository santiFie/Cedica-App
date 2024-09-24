from flask import Flask
from flask_session import Session
from flask_bcrypt import Bcrypt
from src.web import routes
from src.web import errors
from src.core import database
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

    @app.cli.command(name="users-db")
    def users_db():
        database.seeds()

    return app