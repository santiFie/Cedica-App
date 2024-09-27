from src.web.controllers.auth import bp as auth_bp
from flask import render_template
from src.web.handlers.auth import login_required


def register(app):

    @login_required
    @app.route("/")
    def home():
        return render_template("home.html")

    # Blueprints
    app.register_blueprint(auth_bp)