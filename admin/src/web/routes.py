from src.web.controllers.auth import bp as auth_bp
from src.web.controllers.users import bp as users_bp
from src.web.controllers.payments import bp as payments_bp
from src.web.controllers.team_members import bp as team_members_bp
from src.web.controllers.equestrian import bp as equestrian_bp
from src.web.controllers.riders_and_horsewoman import bp as riders_horsewoman_bp
from src.web.controllers.collections import bp as collections_bp
from src.web.api.posts import bp as posts_api_bp
from src.web.api.contacts import bp as contacts_api_bp
from src.web.controllers.contacts import bp as contacts_bp
from src.web.controllers.posts import bp as posts_bp
from src.web.controllers.graphics import bp as graphics_bp
from src.web.controllers.reports import bp as reports_bp
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
    app.register_blueprint(payments_bp)
    app.register_blueprint(team_members_bp)
    app.register_blueprint(equestrian_bp)
    app.register_blueprint(collections_bp)
    app.register_blueprint(riders_horsewoman_bp)
    app.register_blueprint(posts_api_bp)
    app.register_blueprint(contacts_api_bp)
    app.register_blueprint(contacts_bp)
    app.register_blueprint(posts_bp)
    app.register_blueprint(graphics_bp)
    app.register_blueprint(reports_bp)
