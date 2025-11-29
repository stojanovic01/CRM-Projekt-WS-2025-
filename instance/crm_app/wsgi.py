#!/usr/bin/env python3
"""
WSGI Entry Point für Gunicorn
Verwendung: gunicorn --config gunicorn_config.py wsgi:application
"""
import sys
import os

# Füge App-Verzeichnis zum Python-Path hinzu
sys.path.insert(0, os.path.dirname(__file__))

# Lade Umgebungsvariablen aus .env (optional)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # python-dotenv nicht installiert, verwende System-Umgebungsvariablen

# Importiere Flask-App
from app import app as application

# Initialisiere Datenbank beim Start
with application.app_context():
    from models import db, Customer
    from app import create_admin_user, create_sample_data
    
    try:
        db.create_all()
        print("✅ Datenbank-Tabellen erstellt/überprüft")
        
        create_admin_user()
        print("✅ Admin-User erstellt/überprüft")
        
        # Beispieldaten nur beim ersten Mal
        if Customer.query.count() == 0:
            create_sample_data()
            print("✅ Beispieldaten erstellt")
    except Exception as e:
        print(f"⚠️  Initialisierungsfehler: {e}")

if __name__ == "__main__":
    application.run()
