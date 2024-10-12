from minio import Minio

class Storage:
    def __init__(self, app=None):
        self.client = None
        if app is not None:
            self.__init__(app)

    def init_app(self, app):
        """Initializate the MinIO client and """
        minio_server = app.config.get('MINIO_SERVER')
        access_key = app.config.get('MINIO_ACCESS_KEY')
        secret_key = app.config.get('MINIO_SECRET_KEY')
        secure = app.config.get('MINIO_SECURE', False)

        # Initialize the MinIO client
        self.client = Minio(
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