from os import fstat
from io import BytesIO
from src.web.storage import BUCKET_NAME
from flask import current_app
from datetime import datetime

def delete_file(prefix, filename, user_id):
    """
    Delete a file from MinIO
    """
    object_name = f"{prefix}/{user_id}-{filename}"

    client = current_app.storage.client
    try:
        client.remove_object(BUCKET_NAME, object_name)
    except Exception as e:
        current_app.logger.error(f"Error deleting file from MinIO: {str(e)}")


def upload_file(file, prefix, user_id):
    """
    Upload a file to Minio server
    """
    size = fstat(file.fileno()).st_size
    client = current_app.storage.client
    meta = {"X-Amz-Meta-Uploaded-Date": datetime.now().isoformat()}
    #client.fput_object(BUCKET_NAME, f"{prefix}/{user_id}-{file.filename}", size, file.content_type, metadata={"uploaded-date": datetime.now().isoformat()})
    client.put_object(BUCKET_NAME, f"{prefix}/{user_id}-{file.filename}", file, size, content_type= file.content_type, metadata=meta)


def get_file(prefix, user_id, filename):
    """
    Get a file from MinIO
    """
    client = current_app.storage.client
    object_name = f"{prefix}/{user_id}-{filename}"
    try:
        response = client.get_object(BUCKET_NAME, object_name)
        stat = client.stat_object(BUCKET_NAME, object_name)
        # Metadata is in `stat.metadata`
        uploaded_date = datetime.fromisoformat(stat.metadata["X-Amz-Meta-Uploaded-Date"])
        return BytesIO(response.read()), response.headers['content-type']
    except Exception as e:
        return None, None
    
def get_file_date(prefix, user_id, filename):
    """
    Get the uploaded date of a file from MinIO
    """
    client = current_app.storage.client
    object_name = f"{prefix}/{user_id}-{filename}"
    try:
        stat = client.stat_object(BUCKET_NAME, object_name)
        return datetime.fromisoformat(stat.metadata["X-Amz-Meta-Uploaded-Date"])
    except Exception as e:
        return None