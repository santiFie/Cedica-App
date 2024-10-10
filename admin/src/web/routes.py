from src.web.controllers.auth import bp as auth_bp
from src.web.controllers.users import bp as users_bp
from src.web.controllers.team_members import bp as team_members_bp
from src.web.controllers.equestrian import bp as equestrian_bp
from flask import render_template
from src.web.handlers.auth import login_required


def register(app):

    
    @app.route("/")
    @login_required
    def home():
        return render_template("home.html")

    # Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(users_bp) 
    app.register_blueprint(team_members_bp)
    app.register_blueprint(equestrian_bp)