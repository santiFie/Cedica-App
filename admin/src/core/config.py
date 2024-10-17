from os import environ

class Config(object):
    TESTING = False
    SECRET_KEY = "my_secret_key"
    SESSION_TYPE = "filesystem"

class ProductionConfig(Config):
    MINIO_SERVER = environ.get("MINIO_SERVER")
    MINIO_ACCESS_KEY = environ.get("MINIO_ACCESS_KEY")
    MINIO_SECRET_KEY = environ.get("MINIO_SECRET_KEY")
    MINIO_SECURE = True
    SQLALCHEMY_DATABASE_URI = environ.get("DATABASE_URL")

class DevelopmentConfig(Config):
    MINIO_SERVER = "localhost:9000"
    MINIO_ACCESS_KEY = "G7hmAEJq91tXcpJ7HsRs"
    MINIO_SECRET_KEY = "hRmdv0rd2YMV1RMa6mGDqJO9MR2pv5TdlQocgEoV"
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