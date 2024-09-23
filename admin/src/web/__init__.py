from flask import Flask, abort
from flask import render_template
from src.web.handlers import error
from src.core import database
from src.core.config import config
from src.web.handlers.auth import bp as auth_bp

def create_app(env="development", static_folder="../../static"):
    app = Flask(__name__, static_folder= static_folder)

    app.config.from_object(config[env])

    database.init_app(app)

    @app.route("/")
    def home():
        return render_template("home.html")
    
    app.register_error_handler(404, error.not_found_error_404)
    
    # queda ruta para chequear que esta bien
    @app.route("/error500")
    def error500():
        abort(500)

    app.register_error_handler(500, error.server_error_500)
    app.register_blueprint(auth_bp)

    @app.route("/error401")
    def error401():
        abort(401)

    app.register_error_handler(401, error.unauthorized_401)

    @app.cli.command(name="reset-db")
    def reset_db():
        database.reset()

    @app.cli.command(name="seeds-db")
    def seeds_db():
        database.seeds()

    return app