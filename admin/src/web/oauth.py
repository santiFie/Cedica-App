from authlib.integrations.flask_client import OAuth

oauth = OAuth()

def configure_oauth(app):
    # Inicializa OAuth con la aplicación Flask
    oauth.init_app(app)

    # Configuración de Google OAuth
    oauth.register(
        name="google",
        open_id=True,
        client_id=app.config.get("GOOGLE_CLIENT_ID"),
        client_secret=app.config.get("GOOGLE_CLIENT_SECRET"),
        redirect_uri=app.config.get("GOOGLE_REDIRECT_URI"),
        client_kwargs={"scope": "openid profile email"},
        server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
        
    )
    
    return oauth