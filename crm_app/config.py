import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Basis-Konfiguration"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-change-in-production')
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI', 'sqlite:///crm.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TIMEZONE = os.getenv('TIMEZONE', 'Europe/Vienna')
    DEBUG = os.getenv('DEBUG', 'False') == 'True'
    JSON_SORT_KEYS = False

class DevelopmentConfig(Config):
    """Entwicklungs-Konfiguration"""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """Produktions-Konfiguration"""
    DEBUG = False
    TESTING = False

class TestingConfig(Config):
    """Test-Konfiguration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

# Config Dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': ProductionConfig
}

def get_config():
    """Gibt die aktuelle Konfiguration zurück"""
    env = os.getenv('FLASK_ENV', 'production')
    return config.get(env, config['default'])