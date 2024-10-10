from flask_sqlalchemy import SQLAlchemy
<<<<<<< HEAD
#from src.core.payments import create_enums

=======
from src.core import team_member as tm 
>>>>>>> dev
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
    from src.core.payments import create_enums
    db.drop_all()

    # Creates the team member enums
    tm.create_enums()

    db.create_all()
<<<<<<< HEAD
    create_enums()
    #db.session.commit()
=======
>>>>>>> dev
    print("Database reset complete.")

def reset_model(model):
    """
    Resets a specific model in the database
    """
    # Creates the team member enums
    tm.create_enums()
    model.__table__.drop(db.engine)
    model.__table__.create(db.engine)
    print(f"Model {model.__name__} reset complete.")
