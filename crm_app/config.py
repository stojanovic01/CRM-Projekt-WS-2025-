"""
Zentralisierte Konfigurationsdatei für CRM
Diese Datei wird von app.py importiert
Liest Datenbankdaten aus include.php
"""

import os
from dotenv import load_dotenv
from php_config_parser import get_db_connection_string, get_db_config_dict

# Lade Umgebungsvariablen
load_dotenv()

class Config:
    """Basis-Konfiguration"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-change-in-production')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False

class DevelopmentConfig(Config):
    """Lokale Entwicklung - liest aus include.php"""
    DEBUG = True
    
    # Liest Datenbankverbindung aus include.php (LOCAL Umgebung)
    try:
        SQLALCHEMY_DATABASE_URI = get_db_connection_string(environment='local', driver='mysql+pymysql')
    except Exception as e:
        print(f"⚠️  Warnung: Konnte include.php nicht laden: {e}")
        print("Fallback auf lokale SQLite-Datenbank...")
        SQLALCHEMY_DATABASE_URI = 'sqlite:///crm_dev.db'

class ProductionConfig(Config):
    """PythonAnywhere Production - liest aus include.php"""
    DEBUG = False
    
    # Liest Datenbankverbindung aus include.php (PRODUCTION Umgebung)
    try:
        SQLALCHEMY_DATABASE_URI = get_db_connection_string(environment='production', driver='mysql+pymysql')
    except Exception as e:
        print(f"❌ Fehler: Konnte include.php nicht laden für Production: {e}")
        raise

# Wähle Config basierend auf Umgebung
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

def get_config():
    """Gibt die passende Konfiguration zurück"""
    env = os.getenv('FLASK_ENV', 'development')
    return config.get(env, config['default'])
