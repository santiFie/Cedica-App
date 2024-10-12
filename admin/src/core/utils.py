from datetime import datetime
from flask import current_app
from os import fstat
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
    except:
        return Exception("Invalid date format in 'string_to_date' function")

def date_to_string(date):
    return date.strftime('%Y-%m-%d')


def upload_file(file, prefix, user_id):
    """
    Upload a file to Minio server
    """
    size = fstat(file.fileno()).st_size
    client = current_app.storage.client
    client.put_object(BUCKET_NAME, f"{prefix}/{user_id}-{file.filename}", file, size, content_type=file.content_type)

def delete_file_from_minio(prefix, filename, user_id):
    """
    Delete a file from MinIO
    """
    object_name = f"{prefix}/{user_id}-{filename}"
    print(object_name)

    client = current_app.storage.client
    try:
        client.remove_object(BUCKET_NAME, object_name)
    except Exception as e:
        current_app.logger.error(f"Error deleting file from MinIO: {str(e)}")