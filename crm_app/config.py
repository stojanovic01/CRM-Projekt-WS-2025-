import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Basis-Konfiguration"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-change-in-production')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TIMEZONE = os.getenv('TIMEZONE', 'Europe/Vienna')
    DEBUG = os.getenv('DEBUG', 'False') == 'True'
    JSON_SORT_KEYS = False

    # Produktionsdatenbank auf PythonAnywhere
    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_HOST = os.getenv('DB_HOST')
    DB_NAME = os.getenv('DB_NAME')

    if DB_USER and DB_PASSWORD and DB_HOST and DB_NAME:
        SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    else:
        raise RuntimeError("MySQL-Konfigurationsvariablen nicht gesetzt!")

class ProductionConfig(Config):
    """Produktions-Konfiguration"""
    DEBUG = False
    TESTING = False

class TestingConfig(Config):
    """Test-Konfiguration (in-memory SQLite)"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

# Config Dictionary
config = {
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': ProductionConfig
}

def get_config():
    """Gibt die aktuelle Konfiguration zurück"""
    env = os.getenv('FLASK_ENV', 'production')
    return config.get(env, config['default'])
