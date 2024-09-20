from os import environ

class Config(object):
    TESTING = False

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = environ.get("DATABASE_URL")

class DevelopmentConfig(Config):
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