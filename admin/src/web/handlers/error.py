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