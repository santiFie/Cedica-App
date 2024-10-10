from datetime import datetime
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
    except:
        return Exception("Invalid date format in 'string_to_date' function")
