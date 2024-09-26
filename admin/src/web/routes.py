from src.web.controllers.auth import bp as auth_bp
from flask import render_template


def register(app):
    @app.route("/")
    def home():
        return render_template("home.html")

    # Blueprints
    app.register_blueprint(auth_bp)