from datetime import datetime
from flask import current_app
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
    try:
        return datetime.strptime(string_date, '%Y-%m-%d')
    except ValueError:
        try:
            return datetime.strptime(string_date, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            return Exception("Invalid date format in 'string_to_date' function")


def date_to_string(date):
    return date.strftime('%Y-%m-%d')
