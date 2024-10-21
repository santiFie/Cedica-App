from datetime import datetime
from flask import current_app, flash
from os import fstat
from io import BytesIO
from src.web.storage import BUCKET_NAME

def validate_dates(initial_date, end_date=None):
    """
    Check if the date/s are valid
    """
    
    if initial_date > datetime.now():
        return False

    if end_date is not None:
        if initial_date > end_date:
            return False

    return True


def string_to_date(string_date):
    """
    Converts the given parameter to a date
    """
    try:
        return datetime.strptime(string_date, '%Y-%m-%d')
    except ValueError:
        try:
            return datetime.strptime(string_date, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            return Exception("Invalid date format in 'string_to_date' function")


def date_to_string(date):
    """
    Converts the given parameter to a string
    """
    return date.strftime('%Y-%m-%d')

def riders_and_horsewomen_errors(riders_form):
    """
    Return errors from a form
    """
    flash("Error al crear el jinete/Amazona", "error")
    field_labels = {
            "dni": "DNI",
            "name": "Nombre",
            "last_name": "Apellido",
            "age": "Edad",
            "date_of_birth": "Fecha de Nacimiento",
            "place_of_birth": "Lugar de Nacimiento",
            "address": "Dirección",
            "phone": "Teléfono",
            "emergency_contact": "Contacto de Emergencia",
            "emergency_phone": "Teléfono de Emergencia",
            "scholarship_percentage": "Porcentaje de Beca",
            "observations": "Observaciones",
            "disability_certificate": "Certificado de Discapacidad",
            "others": "Otros",
            "disability_type": "Tipo de Discapacidad",
            "family_allowance": "Asignación Familiar",
            "pension": "Pensión",
            "name_institution": "Nombre de la Institución",
            "address_institution": "Dirección de la Institución",
            "phone_institution": "Teléfono de la Institución",
            "current_grade": "Grado Actual",
            "observations_institution": "Observaciones de la Institución",
            "health_insurance": "Obra Social",
            "membership_number": "Número de Afiliado",
            "curatela": "Curatela",
            "pension_situation_observations": "Observaciones de la Situación de Pensión"
    }

    for field, errors in riders_form.errors.items():
        label = field_labels.get(field, field)
        for error in errors:
            flash(f"Error en {label}: {error}")


def is_link(file_id):
    """
    Check if a file is a link
    """
    from src.core.models.riders_and_horsewomen import File

    return File.query.get(file_id).is_link