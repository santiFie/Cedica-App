import base64
from os import fstat
from io import BytesIO
from urllib.parse import urlparse
from src.web.storage import BUCKET_NAME
from flask import current_app, flash
from datetime import datetime, timedelta

def delete_file(prefix, filename, user_id):
    """
    Delete a file from MinIO
    """
    object_name = f"{prefix}/{user_id}-{filename}"

    client = current_app.storage.client
    try:
        client.remove_object(BUCKET_NAME, object_name)
    except Exception as e:
        flash(f"Error al eliminar el archivo: {str(e)}", "error")


def upload_file(prefix, file, user_id, filename=None):
    """
    Upload a file to Minio server
    """
    if not filename:
        filename = file.filename
    size = fstat(file.fileno()).st_size
    client = current_app.storage.client
    meta = {"X-Amz-Meta-Uploaded-Date": datetime.now().isoformat()}

    client.put_object(BUCKET_NAME, f"{prefix}/{user_id}-{filename}", file, size, content_type= file.content_type, metadata=meta)


def get_file(prefix, user_id, filename):
    """
    Get a file from MinIO
    """
    client = current_app.storage.client
    object_name = f"{prefix}/{user_id}-{filename}"
    try:
        response = client.get_object(BUCKET_NAME, object_name)
        return BytesIO(response.read()), response.headers['content-type']
    except Exception as e:
        raise Exception(f"Error getting file from MinIO: {str(e)}")
    
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
    
    
def upload_link(prefix, link, filename, user_id):
    """
    Upload a link to Minio server
    """
    client = current_app.storage.client

    # Convert the link to bytes
    link_bytes = link.encode('utf-8')
    
    # Create a BytesIO object with the link bytes
    link_stream = BytesIO(link_bytes)
    
    # Generate a unique name for the object
    object_name = f"{prefix}/{user_id}-{filename}.txt"
    
    # Metadata
    meta = {
        "X-Amz-Meta-Uploaded-Date": datetime.now().isoformat(),
        "X-Amz-Meta-Content-Type": "text/plain"
    }
    
    # Upload the object to Minio
    client.put_object(
        BUCKET_NAME,
        object_name,
        link_stream,
        len(link_bytes),
        content_type="text/plain",
        metadata=meta
    )
    
    return object_name

def get_link(prefix, filename, user_id):
    """
    Get a link from Minio server
    """
    client = current_app.storage.client

    # Generate a unique name for the object
    object_name = f"{prefix}/{user_id}-{filename}.txt"
    print(object_name)
    try:
        # Get the object from Minio
        response = client.get_object(BUCKET_NAME, object_name)
        
        link = response.read().decode('utf-8')
        
        # Get the metadata of the object
        stat = client.stat_object(BUCKET_NAME, object_name)
        metadata = stat.metadata

        print(link.strip())
        
        return link.strip(),metadata.get('X-Amz-Meta-Content-Type')
    
    except Exception as e:
        raise Exception(f"Error getting link from Minio: {str(e)}")
        flash(f"Error al obtener el enlace: {str(e)}")
        return None


