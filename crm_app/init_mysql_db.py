"""
Initialisiert die MySQL-Datenbank und erstellt alle Tabellen
"""
import sys
import os

# Füge das aktuelle Verzeichnis zum Python-Path hinzu
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from models import Customer, Order, OrderItem, Product, Conversation, User

def init_database():
    """Erstelle alle Tabellen in der MySQL-Datenbank"""
    with app.app_context():
        print("Erstelle alle Tabellen in der MySQL-Datenbank...")
        
        # Lösche alle bestehenden Tabellen (Vorsicht!)
        print("Lösche alte Tabellen falls vorhanden...")
        db.drop_all()
        
        # Erstelle alle Tabellen neu
        print("Erstelle neue Tabellen...")
        db.create_all()
        
        print("✓ Datenbank erfolgreich initialisiert!")
        print(f"✓ Verbunden mit: {app.config['SQLALCHEMY_DATABASE_URI'].split('@')[1].split('?')[0]}")
        
        # Zeige erstellte Tabellen
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        print(f"✓ Erstellte Tabellen: {', '.join(tables)}")

if __name__ == '__main__':
    try:
        init_database()
    except Exception as e:
        print(f"❌ Fehler beim Initialisieren der Datenbank: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
