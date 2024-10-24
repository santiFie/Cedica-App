from os import environ
from datetime import timedelta

class Config(object):
    TESTING = False
    SECRET_KEY = "my_secret_key"
    SESSION_TYPE = "filesystem"
    SESSION_PERMANENT = False
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=60)

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

class DevelopmentConfig(Config):
    MINIO_SERVER = "localhost:9000"
    MINIO_ACCESS_KEY = "0yNExytlaQ2opQLb19vp"
    MINIO_SECRET_KEY = "AaVEC9YEuvJ56Yag943XT6Vex7VaQXyhhH6Qh5G5"
    MINIO_SECURE = False
    DEBUG = True
    DB_USER = "grupo43"
    DB_PASSWORD = "1234"
    DB_HOST = "localhost"
    DB_PORT = "5432"
    DB_NAME = "grupo43"
    SQLALCHEMY_DATABASE_URI = (
         f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

class TestingConfig(Config):
    TESTING = True

config = {
    "production": "src.core.config.ProductionConfig",
    "development": "src.core.config.DevelopmentConfig",
    "testing": "src.core.config.TestingConfig",
}