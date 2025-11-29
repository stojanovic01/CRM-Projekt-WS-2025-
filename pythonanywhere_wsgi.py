"""
WSGI-Konfiguration für PythonAnywhere
Diese Datei wird von PythonAnywhere als Entry-Point verwendet
"""

import sys
import os
from pathlib import Path

# ============================================
# Pfade konfigurieren
# ============================================
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / 'crm_app'))
sys.path.insert(0, str(project_root))

# Wechsel in Projekt-Verzeichnis
os.chdir(str(project_root / 'crm_app'))

# ============================================
# Umgebungsvariablen laden
# ============================================
if not os.environ.get('FLASK_ENV'):
    os.environ['FLASK_ENV'] = 'production'

# Lade .env wenn vorhanden
if Path('.env').exists():
    from dotenv import load_dotenv
    load_dotenv()

# ============================================
# Flask App importieren
# ============================================
from app import app as application

# ============================================
# Error Handling für WSGI
# ============================================
if __name__ == '__main__':
    print("⚠️  Diese Datei sollte nicht direkt ausgeführt werden!")
    print("   Sie wird von PythonAnywhere als WSGI Entry-Point verwendet.")
    print("   Verwenden Sie für lokale Tests: python crm_app/app.py")
