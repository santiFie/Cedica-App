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

def unauthorized_403(e):
    error = Error(403, "403 - Prohibido", "Acceso denegado", "No tienes permiso para acceder a este recurso.", "Contacta al administrador si crees que esto es un error.")

    return render_template("error.html", error=error), 403

def unauthorized_502(e):
    error = Error(502, "502 - Error de puerta de enlace", "Error en el servidor", "El servidor no pudo procesar la solicitud.", "Intenta nuevamente más tarde.")

    return render_template("error.html", error=error), 502

def method_not_allowed_405(e):
    error = Error(405, "405 - Método no permitido", "Método no permitido", "El método HTTP utilizado no está permitido para este recurso.", "Revisa el método permitido e intenta nuevamente.")

    return render_template("error.html", error=error), 405
