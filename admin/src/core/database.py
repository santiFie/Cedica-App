from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import inspect

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
    db.session.commit()
    db.create_all()
    db.session.commit()
    print("Database reset complete.")

def seeds():
    pass