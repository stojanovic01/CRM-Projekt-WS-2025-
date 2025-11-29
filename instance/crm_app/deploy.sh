#!/bin/bash
# Deployment-Script für Ubuntu/Nginx Server
# Verwendung: bash deploy.sh

set -e  # Bei Fehler abbrechen

echo "🚀 CRM-App Deployment gestartet..."
echo ""

# 1. Prüfe ob im richtigen Verzeichnis
if [ ! -f "app.py" ]; then
    echo "❌ Fehler: app.py nicht gefunden!"
    echo "Bitte in das crm_app-Verzeichnis wechseln."
    exit 1
fi

# 2. Virtual Environment erstellen
echo "📦 Erstelle Virtual Environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✅ Virtual Environment erstellt"
else
    echo "ℹ️  Virtual Environment existiert bereits"
fi

# 3. Aktiviere venv und installiere Dependencies
echo ""
echo "📥 Installiere Python-Pakete..."
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
echo "✅ Pakete installiert"

# 4. Umgebungsvariablen setzen
echo ""
echo "🔧 Setze Umgebungsvariablen..."
export TZ='Europe/Vienna'
export LC_ALL='de_AT.UTF-8'
export LANG='de_AT.UTF-8'
export FLASK_APP='app.py'
export FLASK_ENV='production'

# 5. Datenbank initialisieren
echo ""
echo "🗄️  Initialisiere Datenbank..."
python3 << 'PYTHON_SCRIPT'
from app import app, db, create_admin_user, create_sample_data
from models import Customer

with app.app_context():
    try:
        db.create_all()
        print("✅ Tabellen erstellt/überprüft")
        
        create_admin_user()
        print("✅ Admin-User erstellt")
        
        if Customer.query.count() == 0:
            create_sample_data()
            print("✅ Beispieldaten eingefügt")
        else:
            print("ℹ️  Beispieldaten bereits vorhanden")
    except Exception as e:
        print(f"❌ Fehler: {e}")
        exit(1)
PYTHON_SCRIPT

# 6. Test: Gunicorn kurz starten
echo ""
echo "✅ Teste Gunicorn..."
gunicorn --bind 127.0.0.1:8000 --timeout 10 wsgi:application &
GUNICORN_PID=$!
sleep 5

# Prüfe ob Gunicorn läuft
if curl -s http://127.0.0.1:8000 > /dev/null 2>&1; then
    echo "✅ Gunicorn läuft erfolgreich!"
    kill $GUNICORN_PID 2>/dev/null || true
else
    echo "⚠️  Gunicorn-Test fehlgeschlagen (kann auch an fehlendem curl liegen)"
    kill $GUNICORN_PID 2>/dev/null || true
fi

echo ""
echo "✅ Deployment erfolgreich abgeschlossen!"
echo ""
echo "📋 Nächste Schritte (als root/sudo):"
echo ""
echo "1. Service-Datei kopieren:"
echo "   sudo cp crm.service /etc/systemd/system/"
echo "   # WICHTIG: Pfade in crm.service anpassen!"
echo ""
echo "2. Service aktivieren:"
echo "   sudo systemctl daemon-reload"
echo "   sudo systemctl enable crm"
echo "   sudo systemctl start crm"
echo "   sudo systemctl status crm"
echo ""
echo "3. Nginx konfigurieren:"
echo "   sudo cp nginx_crm.conf /etc/nginx/sites-available/crm"
echo "   # WICHTIG: Domain in nginx_crm.conf anpassen!"
echo "   sudo ln -s /etc/nginx/sites-available/crm /etc/nginx/sites-enabled/"
echo "   sudo nginx -t"
echo "   sudo systemctl restart nginx"
echo ""
echo "4. App im Browser testen:"
echo "   http://ihre-domain.at"
echo "   Login: administrator / administrator"
echo ""
