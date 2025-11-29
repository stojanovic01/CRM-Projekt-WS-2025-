# 📖 CRM auf PythonAnywhere - Deployment-Anleitung für Anfänger

**Version:** 1.0  
**Zielplattform:** PythonAnywhere (pythonanywhere.com)  
**Dauer:** ca. 30-45 Minuten  
**Schwierigkeit:** Anfänger

---

## 📋 Was Sie brauchen

✅ PythonAnywhere Account (kostenlos oder bezahlt)  
✅ Dieses Git-Repository / Projekt-Ordner  
✅ Text-Editor (Notepad reicht!)  
✅ Browser  

---

## 🚀 SCHRITT 1-10: Das vollständige Deployment

### SCHRITT 1: PythonAnywhere Web App erstellen

1. Login auf https://www.pythonanywhere.com
2. Dashboard → **"Web"** → **"Add a new web app"**
3. Wählen Sie **Flask** und **Python 3.11**
4. Projektname: `crm` (URL wird: `<USERNAME>-crm.pythonanywhere.com`)
5. "Next" & "Finish"

**Status:** ✅ Web App ist erstellt

---

### SCHRITT 2: Code hochladen

**Option A - Mit Git (empfohlen):**
```bash
# Bash Console auf PythonAnywhere öffnen:
# Dashboard → Consoles → Bash

cd /home/<USERNAME>
git clone https://github.com/YOUR_REPO.git mysite
cd mysite
```

**Option B - Datei-Manager:**
- Dashboard → Files → Upload alle Ordner/Dateien
- Struktur: `/home/<USERNAME>/mysite/crm_app/`, `pythonanywhere_wsgi.py`, etc.

**Status:** ✅ Code liegt in `/home/<USERNAME>/mysite/`

---

### SCHRITT 3: Virtuelle Umgebung & Dependencies

**Bash Console (fortgesetzt):**
```bash
cd /home/<USERNAME>/mysite

# 1. venv erstellen
python3.11 -m venv venv

# 2. Aktivieren
source venv/bin/activate

# 3. Dependencies
pip install -r requirements.txt
```

**Erwartete Ausgabe:** `Successfully installed Flask-3.0.0 ...`

**Status:** ✅ Dependencies installiert

---

### SCHRITT 4: .env Konfiguration

```bash
# .env aus Template kopieren
cp .env.example .env

# Bearbeiten
nano .env
```

**Inhalt setzen:**
```ini
FLASK_ENV=production
SECRET_KEY=<NEUER_ZUFALLSWERT>
SQLALCHEMY_DATABASE_URI=sqlite:///app.db
DEBUG=False
```

**Secret Key generieren (in Bash):**
```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```

Speichern: `Ctrl+O` → Enter → `Ctrl+X`

**Status:** ✅ .env konfiguriert

---

### SCHRITT 5: Datenbank importieren

```bash
cd /home/<USERNAME>/mysite/crm_app/instance
sqlite3 crm.db < ../../crm_dump.sql

# Überprüfen:
sqlite3 crm.db "SELECT COUNT(*) FROM customers;"
# Sollte: 5 zeigen
```

**Status:** ✅ Datenbank mit Testdaten importiert

---

### SCHRITT 6: WSGI-Datei konfigurieren

Im Dashboard:
```
Web → [Your web app] → WSGI configuration file
```

Edit: `/var/www/<USERNAME>_pythonanywhere_com_wsgi.py`

**Einfügung am Anfang:**
```python
import sys
import os
from pathlib import Path

# Pfade
project = '/home/<USERNAME>/mysite'
sys.path.insert(0, f'{project}/crm_app')
os.chdir(f'{project}/crm_app')

# .env laden
if Path('/home/<USERNAME>/mysite/.env').exists():
    from dotenv import load_dotenv
    load_dotenv('/home/<USERNAME>/mysite/.env')

if not os.environ.get('FLASK_ENV'):
    os.environ['FLASK_ENV'] = 'production'

from app import app as application
```

**Speichern** und **"Reload"** klicken!

**Status:** ✅ WSGI konfiguriert

---

### SCHRITT 7-10: TESTEN

#### SCHRITT 7: Startseite testen
```
https://<USERNAME>-crm.pythonanywhere.com/
```
❓ Lädt die Seite ohne Fehler?  
✅ = Weiter zu Schritt 8

---

#### SCHRITT 8: Daten überprüfen
```
https://<USERNAME>-crm.pythonanywhere.com/customers
```
❓ Zeigt "5 customers"?  
❓ Sehen Sie Max Mustermann, Anna Schmidt, etc.?  
✅ = Weiter zu Schritt 9

---

#### SCHRITT 9: Kunden-Detail testen
```
Klick auf "Max Mustermann"
```
❓ Zeigt E-Mail: max@example.com?  
❓ Zeigt Umsatz: z.B. €3,199.95?  
✅ = Weiter zu Schritt 10

---

#### SCHRITT 10: Suchfunktion testen
```
Suchfeld: "Anna"
Ergebnis: Anna Schmidt sollte erscheinen
```
❓ Funktioniert die Suche?  
✅ = **Deployment erfolgreich!**

---

## 🐛 Häufige Probleme

### ❌ "502 Bad Gateway"
**Lösung:** WSGI-Datei überprüfen
```bash
# Logs ansehen:
tail -50 /var/log/access.log
```

### ❌ Keine Daten in /customers
**Lösung:** Dump-Import überprüfen
```bash
sqlite3 /home/<USERNAME>/mysite/crm_app/instance/crm.db ".tables"
# Sollte: customers, orders, products, users, conversations zeigen
```

### ❌ "ERROR 500"
**Lösung:**
1. SECRET_KEY in .env überprüfen (nicht "change-me-...")
2. WSGI-Pfade überprüfen (USERNAME korrekt?)
3. Reload durchführen

---

## ✅ Checkliste Deployment abgeschlossen?

```
[ ] PythonAnywhere Web App "crm" erstellt
[ ] Code in /home/USERNAME/mysite/ hochgeladen  
[ ] venv erstellt und Dependencies installiert
[ ] .env mit SECRET_KEY erstellt
[ ] crm_dump.sql importiert (5 customers)
[ ] WSGI-Datei angepasst
[ ] Startseite lädt (https://<USERNAME>-crm.pythonanywhere.com/)
[ ] /customers zeigt 5 Kunden
[ ] Kunden-Detail funktioniert
[ ] Suchfunktion funktioniert
```

Wenn alles gehakt: ✅ **Deployment erfolgreich!**

---

## 🧪 Smoke-Tests (optional)

```bash
# SSH Console
cd /home/<USERNAME>/mysite
source venv/bin/activate
python crm_app/scripts/smoke_tests.py
```

**Erwartet:** 27/27 Tests bestanden

---

## 📞 Support

Fragen zur Anleitung?
1. Logs überprüfen: `tail -100 /var/log/access.log`
2. PythonAnywhere Help: https://help.pythonanywhere.com/
3. Stellen Sie sicher, dass USERNAME überall korrekt ist

---

**🎉 Fertig! Ihr CRM läuft auf PythonAnywhere!**
