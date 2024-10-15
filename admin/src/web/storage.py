from minio import Minio

BUCKET_NAME = 'grupo43'

class Storage:
    def __init__(self, app=None):
        self._client = None
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """Initializate the MinIO client and """
        minio_server = app.config.get('MINIO_SERVER')
        access_key = app.config.get('MINIO_ACCESS_KEY')
        secret_key = app.config.get('MINIO_SECRET_KEY')
        secure = app.config.get('MINIO_SECURE', True)

        # Initialize the MinIO client
        self._client = Minio(
            minio_server, access_key=access_key, secret_key=secret_key, secure=secure
        )

        # Attach the client to the app context
        app.storage = self

        return app
    
    @property
    def client(self):
        """ Property to get the MinIO client """
        return self._client
    
    @client.setter
    def client(self, client):
        """ Property to set the MinIO client """
        self._client = client

storage = Storage()