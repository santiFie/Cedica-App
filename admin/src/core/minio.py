import base64
from os import fstat
from io import BytesIO
from urllib.parse import urlparse
from src.web.storage import BUCKET_NAME
from flask import current_app
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
        current_app.logger.error(f"Error deleting file from MinIO: {str(e)}")


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
        stat = client.stat_object(BUCKET_NAME, object_name)
        # Metadata is in `stat.metadata`
        uploaded_date = datetime.fromisoformat(stat.metadata["X-Amz-Meta-Uploaded-Date"])
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

    # Encode the entire link in base64
    #encoded_link = base64.urlsafe_b64encode(link.encode()).decode()
    
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
    
    try:
        # Obtener el objeto de Minio
        response = client.get_object(BUCKET_NAME, object_name)
        
        link = response.read().decode('utf-8')
        
        # Obtener los metadatos
        stat = client.stat_object(BUCKET_NAME, object_name)
        metadata = stat.metadata
        
        return link.strip(),metadata.get('X-Amz-Meta-Content-Type')
    
    except Exception as e:
        current_app.logger.error(f"Error al obtener el enlace: {str(e)}")
        return None


