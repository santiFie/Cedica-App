from flask_sqlalchemy import SQLAlchemy
from src.core import riders_and_horsewomen as rh

db = SQLAlchemy()

def init_app(app):
    """
    Initializes the database with the app
    """
    db.init_app(app)
    config(app)

    return app

    
def config(app):
    """
    Hooks configutation for the database
    """

    @app.teardown_appcontext
    def close_session(exception=None):
        """
        When the request finishes, close the session of the database
        """
        db.session.close()

    return app

def reset():
    db.drop_all()
    
    # Create all the rideders and horsewomen enums
    rh.create_enums()

    db.create_all()
    print("Database reset complete.")
