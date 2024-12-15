from os import environ
from datetime import timedelta

class Config(object):
    TESTING = False
    SECRET_KEY = "my_secret_key"
    SESSION_TYPE = "filesystem"
    SESSION_PERMANENT = False
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=60)
    CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'

class ProductionConfig(Config):
    MINIO_SERVER = environ.get("MINIO_SERVER")
    MINIO_ACCESS_KEY = environ.get("MINIO_ACCESS_KEY")
    MINIO_SECRET_KEY = environ.get("MINIO_SECRET_KEY")
    MINIO_SECURE = True
    SQLALCHEMY_DATABASE_URI = environ.get("DATABASE_URL")
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_size": 10,
        "pool_recycle": 60,
        "pool_pre_ping": True,
    }
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    GOOGLE_CLIENT_ID = environ.get("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = environ.get("GOOGLE_CLIENT_SECRET")
    GOOGLE_REDIRECT_URI = environ.get("GOOGLE_REDIRECT_URI")
    
    class DevelopmentConfig(Config):
        MINIO_SERVER = environ.get("MINIO_SERVER")
        MINIO_ACCESS_KEY = environ.get("MINIO_ACCESS_KEY")
        MINIO_SECRET_KEY = environ.get("MINIO_SECRET_KEY")
        MINIO_SECURE = environ.get("MINIO_SECURE") == 'True'
        DEBUG = environ.get("DEBUG") == 'True'
        DB_USER = environ.get("DB_USER")
        DB_PASSWORD = environ.get("DB_PASSWORD")
        DB_HOST = environ.get("DB_HOST")
        DB_PORT = environ.get("DB_PORT")
        DB_NAME = environ.get("DB_NAME")
        SQLALCHEMY_DATABASE_URI = environ.get("SQLALCHEMY_DATABASE_URI")
        SQLALCHEMY_TRACK_MODIFICATIONS = environ.get("SQLALCHEMY_TRACK_MODIFICATIONS") == 'True'
        GOOGLE_CLIENT_ID = environ.get("GOOGLE_CLIENT_ID")
        GOOGLE_CLIENT_SECRET = environ.get("GOOGLE_CLIENT_SECRET")
        GOOGLE_REDIRECT_URI = environ.get("GOOGLE_REDIRECT_URI")
        CONF_URL = environ.get("CONF_URL")

class TestingConfig(Config):
    TESTING = True

config = {
    "production": "src.core.config.ProductionConfig",
    "development": "src.core.config.DevelopmentConfig",
    "testing": "src.core.config.TestingConfig",
}