from flask import Flask, abort
from flask import render_template
from src.web.handlers import error

def create_app(env="development", static_folder="../../static"):
    app = Flask(__name__, static_folder= static_folder)

    @app.route("/")
    def home():
        return render_template("home.html")
    
    app.register_error_handler(404, error.not_found_error_404)
    
    # queda ruta para chequear que esta bien
    @app.route("/error500")
    def error500():
        abort(500)

    app.register_error_handler(500, error.server_error_500)


    return app