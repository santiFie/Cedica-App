from dataclasses import dataclass
from flask import render_template

@dataclass
class Error:
    code: int
    title: str
    subtitle: str
    description: str
    helper: str

def not_found_error_404(e):
    error = Error(404, "404 - Página no encontrada", "Página no encontrada", "La página que estás buscando no existe", "Verifica la URL que ingresaste o elige una opción debajo")

    return render_template("error.html", error=error), 404

def server_error_500(e):
    error = Error(500, "500 - Error interno del servidor", "Error interno del servidor", "Ocurrio un error inesperado en el servidor", "Intenta nuevamente mas tarde")

    return render_template("error.html", error=error), 500

def unauthorized_401(e):
    error = Error(401, "401 - No autorizado", "No autorizado", "No tienes permiso para acceder a este recurso", "Verifica tus credenciales e intenta nuevamente")

    return render_template("error.html", error=error), 401