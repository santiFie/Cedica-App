from src.web.handlers import error
 

def register_errors(app):
    app.register_error_handler(404, error.not_found_error_404)
    app.register_error_handler(500, error.server_error_500)
    app.register_error_handler(401, error.unauthorized_401)