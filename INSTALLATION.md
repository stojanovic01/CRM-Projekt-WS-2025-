# 📖 CRM-Anwendung - Installations- & Migrationsanleitung für PythonAnywhere

## 1) Plattform-Check ✅

| Aspekt | Status |
|--------|--------|
| **Zielplattform** | PythonAnywhere (pythonanywhere.com) |
| **Programmiersprache** | Python 3 (Flask) |
| **Datenbank** | MySQL (PythonAnywhere Standard) |
| **Betrieb** | Cloud-Hosting, automatische WSGI |

**Entscheidung:** PythonAnywhere wurde gewählt, da es:
- Einfache MySQL-Verwaltung via Dashboard bietet
- Automatische WSGI-Konfiguration ermöglicht
- Kostenlos für kleine Anwendungen läuft
- Keine SSH/FTP-Komplexität erfordert

---

## 2) Voraussetzungen

### Erforderliche Accounts & Tools

- ✅ **PythonAnywhere Account** - https://www.pythonanywhere.com
  - Kostenlos oder bezahlt (Ab $5/Monat für MySQL)
  - Account-Name: Wird benötigt für `<username>.pythonanywhere.com`

- ✅ **Lokale Vorbereitung**
  - Python 3.8+ installiert
  - Git (optional, für Versionskontrolle)
  - Texteditor oder IDE

### Benutzer-Zugangsdaten

Die folgenden Informationen werden der Lehrperson separat bereitgestellt:

```
PythonAnywhere Login:
  Benutzer: [WIRD SEPARAT BEREITGESTELLT]
  Passwort: [WIRD SEPARAT BEREITGESTELLT]

MySQL Datenbank:
  Host: [USERNAME].mysql.pythonanywhere-services.com
  Datenbank: [USERNAME]$crm_db
  Benutzer: [USERNAME]
  Passwort: [WIRD SEPARAT BEREITGESTELLT]

Website URL:
  https://[USERNAME].pythonanywhere.com
```

---

## 3) Schritt-für-Schritt Installation

### Schritt 1: PythonAnywhere Account erstellen / einloggen

1. Öffnen Sie: https://www.pythonanywhere.com
2. Klicken Sie **"Start running Python online"** (kostenlos)
3. Oder **Login** falls Sie bereits einen Account haben
4. Bestätigen Sie die Email

**Screenshot-Moment:** PythonAnywhere Dashboard nach Login

---

### Schritt 2: MySQL Datenbank erstellen

1. Im PythonAnywhere Dashboard: **Databases** (links)
2. Klicken Sie **"Create a new database"**
3. Geben Sie einen Namen ein: z.B. `crm_db`
4. Klicken Sie **"Create"**
5. Speichern Sie die Zugangsdaten:
   - **Host:** `[USERNAME].mysql.pythonanywhere-services.com`
   - **Benutzer:** `[USERNAME]`
   - **Datenbank:** `[USERNAME]$crm_db`
   - **Passwort:** Wird nach Erstellung angezeigt

**Screenshot-Moment:** Datenbank erfolgreich erstellt mit Zugangsdaten

---

### Schritt 3: Code hochladen (via Git oder ZIP)

#### Option A: Via Git (empfohlen)

1. Im PythonAnywhere Dashboard: **Consoles** → **New console** → **Bash**
2. Führen Sie aus:
   ```bash
   cd ~
   git clone https://github.com/BENUTZERNAME/CRM-Projekt-WS-2025-.git
   cd CRM-Projekt-WS-2025-/crm_app
   ```

#### Option B: Via ZIP Upload

1. Laden Sie den Code lokal als ZIP herunter
2. Im PythonAnywhere: **Files** → Upload ZIP
3. Extrahieren Sie den ZIP in Ihr Home-Verzeichnis
4. Navigieren Sie zum Ordner: `CRM-Projekt-WS-2025-/crm_app`

**Screenshot-Moment:** Code erfolgreich hochgeladen

---

### Schritt 4: Virtual Environment einrichten

1. Im Dashboard: **Consoles** → **New console** → **Bash**
2. Führen Sie aus:
   ```bash
   cd ~/CRM-Projekt-WS-2025-/crm_app
   mkvirtualenv --python=/usr/bin/python3.10 crm_env
   ```
3. Das Virtual Environment wird automatisch aktiviert

---

### Schritt 5: Abhängigkeiten installieren

In der **Bash Console** (env sollte aktiv sein):

```bash
pip install -r requirements.txt
```

**Erwartete Ausgabe:**
```
Successfully installed Flask-3.0.0 Flask-SQLAlchemy-3.1.1 ... [weitere Pakete]
```

**Screenshot-Moment:** Erfolgreiches Installation aller Pakete

---

### Schritt 6: .env Datei erstellen

1. In PythonAnywhere: **Files** → Öffnen Sie `crm_app/`
2. Erstellen Sie neue Datei: `.env`
3. Kopieren Sie diesen Inhalt und passen Sie an:

```env
# Flask-Einstellungen
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=your-secret-key-change-this-to-something-random

# Datenbank - Ihre MySQL-Zugangsdaten von Schritt 2
SQLALCHEMY_DATABASE_URI=mysql+pymysql://[USERNAME]:[PASSWORD]@[HOST]/[USERNAME]$crm_db?charset=utf8mb4

# Beispiel (ersetzen Sie CHANGE_ME durch echte Werte):
# SQLALCHEMY_DATABASE_URI=mysql+pymysql://john:mypassword@john.mysql.pythonanywhere-services.com/john$crm_db?charset=utf8mb4

# Zeitzone
TIMEZONE=Europe/Vienna

# Sicherheit
SQLALCHEMY_TRACK_MODIFICATIONS=False
```

**Wichtig:** Speichern Sie die `.env` Datei!

---

### Schritt 7: Datenbank-Tabellen erstellen

In der **Bash Console**:

```bash
cd ~/CRM-Projekt-WS-2025-/crm_app
source ~/.virtualenvs/crm_env/bin/activate
python << EOF
from app import app, db
with app.app_context():
    db.create_all()
    print("✓ Tabellen erfolgreich erstellt!")
EOF
```

**Screenshot-Moment:** Bestätigung "Tabellen erfolgreich erstellt!"

---

### Schritt 8: Datenbank-Dump importieren (Beispieldaten)

#### Methode A: Via Web-Console (einfach)

1. Im PythonAnywhere: **Databases** → Ihre Datenbank
2. Klicken Sie **"Open in Adminer"** (oder phpMyAdmin falls vorhanden)
3. Wählen Sie: **Import**
4. Laden Sie die Datei hoch: `crm_dump.sql` (aus dem Projekt)
5. Klicken Sie **"Execute"**

**Screenshot-Moment:** Erfolgreiches Import mit Daten

#### Methode B: Via MySQL CLI (für Fortgeschrittene)

In der **Bash Console**:

```bash
cd ~/CRM-Projekt-WS-2025-
mysql -u [USERNAME] -p[PASSWORD] -h [USERNAME].mysql.pythonanywhere-services.com [USERNAME]\$crm_db < crm_dump.sql
```

Geben Sie Ihr Passwort ein wenn gefordert.

---

### Schritt 9: WSGI-Datei erstellen (für PythonAnywhere)

1. Im Dashboard: **Web** → **Add a new web app**
2. Wählen Sie **Manual configuration** → **Python 3.10**
3. Im WSGI-Datei-Editor, ersetzen Sie den Inhalt durch:

```python
import sys
import os

path = os.path.expanduser('~/CRM-Projekt-WS-2025-/crm_app')
if path not in sys.path:
    sys.path.insert(0, path)

os.environ['VIRTUAL_ENV'] = os.path.expanduser('~/.virtualenvs/crm_env')
os.environ.setdefault('FLASK_ENV', 'production')

# Lade .env Variablen
from dotenv import load_dotenv
load_dotenv(os.path.join(path, '.env'))

from app import app as application
```

4. Klicken Sie **"Save"**

**Screenshot-Moment:** WSGI-Datei erfolgreich gespeichert

---

### Schritt 10: Web-App neu laden

1. Im Dashboard: **Web** → Ihre Web-App
2. Klicken Sie **"Reload [USERNAME].pythonanywhere.com"** (grüner Button)
3. Warten Sie 10-30 Sekunden

**Screenshot-Moment:** "Reload completed. Web app is live."

---

### Schritt 11: App testen

Öffnen Sie im Browser:
```
https://[USERNAME].pythonanywhere.com
```

Sie sollten sehen:
- ✅ Login-Seite lädt
- ✅ CSS/Styling ist sichtbar
- ✅ Keine Fehler in der Konsole (F12)

**Screenshot-Moment:** CRM-App lädt erfolgreich

---

## 4) Smoke-Tests (Validierung)

Nach erfolgreicher Installation führen Sie diese Tests durch:

### Test 1: Anmeldung

1. Öffnen Sie: `https://[USERNAME].pythonanywhere.com`
2. Benutzer: `administrator`
3. Passwort: `administrator`
4. **Ergebnis:** Sie sehen das Dashboard

✅ **PASS** - Authentifizierung funktioniert

---

### Test 2: Kunden-Übersicht

1. Klicken Sie im Menu: **Kunden**
2. Sie sollten 5 Beispiel-Kunden sehen:
   - Max Mustermann
   - Anna Beispiel
   - Peter Schmidt
   - Sarah Weber
   - Thomas Fischer

✅ **PASS** - Datenbank hat Beispieldaten

---

### Test 3: Kunden-Detail & Filter

1. Klicken Sie auf einen Kunden (z.B. "Max Mustermann")
2. Sie sehen:
   - Kundendetails (Email, Telefon)
   - Bestellungen (mind. 2)
   - Umsatz gesamt (z.B. 1.329,98 €)
   - Umsatz letztes Jahr (falls Daten)
3. Scroll unten zu "Letzte Bestellungen" - sollten 2-3 Bestellungen sichtbar sein
4. Scroll weiter zu "Letzte Kontakte" - sollten 2 Gespräche sichtbar sein

✅ **PASS** - Kundendetails & Beziehungen arbeiten

---

### Test 4: Bestellungen-Suche

1. Klicken Sie: **Bestellungen**
2. Sie sehen eine Liste mit ~7 Bestellungen
3. Klicken Sie auf eine Bestellung - sehen Sie Details & Positionen?

✅ **PASS** - Bestellungsdata wird angezeigt

---

### Test 5: Produkte

1. Klicken Sie: **Produkte**
2. Sie sehen 5 Beispiel-Produkte:
   - Laptop Pro (1299.99 €)
   - USB-C Kabel (29.99 €)
   - Monitor 27" (399.99 €)
   - etc.

✅ **PASS** - Produktdaten vorhanden

---

### Test 6: Logs überprüfen

1. Im PythonAnywhere Dashboard: **Web** → **Log files**
2. Überprüfen Sie die **error.log** auf Fehler
   - Sollte leer oder nur Warnungen sein
   - Keine roten Errors

✅ **PASS** - Keine kritischen Fehler

---

## 5) Troubleshooting

### Problem: "No module named 'app'"

**Ursache:** Virtual Environment nicht aktiviert oder Pfad falsch

**Lösung:**
```bash
source ~/.virtualenvs/crm_env/bin/activate
cd ~/CRM-Projekt-WS-2025-/crm_app
python -c "from app import app; print('OK')"
```

---

### Problem: "Can't connect to MySQL server"

**Ursache:** Datenbank-Zugangsdaten in `.env` falsch

**Lösung:**
1. Überprüfen Sie in `.env`:
   - Host ist korrekt (z.B. `john.mysql.pythonanywhere-services.com`)
   - Datenbank ist korrekt (z.B. `john$crm_db`)
   - Passwort stimmt
2. Testen Sie die Verbindung:
   ```bash
   mysql -u [USERNAME] -p -h [HOST] [DATABASE]
   ```

---

### Problem: "500 Internal Server Error"

**Ursache:** Python-Fehler in der App

**Lösung:**
1. Überprüfen Sie in PythonAnywhere: **Web** → **error.log**
2. Suchen Sie nach roten Fehlern
3. Häufig: Fehlende imports, falsche `.env`-Werte
4. Korrigieren Sie und klicken Sie **"Reload"**

---

### Problem: "403 Forbidden" oder "404 Not Found"

**Ursache:** WSGI-Konfiguration falsch

**Lösung:**
1. Überprüfen Sie die WSGI-Datei (Schritt 9)
2. Der Path muss auf `crm_app/` zeigen
3. Speichern und **Reload** durchführen

---

### Problem: CSS/Bilder laden nicht

**Ursache:** Static Files nicht konfiguriert

**Lösung:**
1. Im PythonAnywhere: **Web** → **Static files**
2. Fügen Sie hinzu:
   - URL: `/static/`
   - Directory: `/home/[USERNAME]/CRM-Projekt-WS-2025-/crm_app/static/`
3. Klicken Sie **"Save"** und **"Reload"**

---

## 6) Datenbank-Management

### Datenbank-Dump aktualisieren (nach Änderungen)

Falls Sie neue Daten in der Datenbank eingefügt haben und einen neuen Dump möchten:

1. In PythonAnywhere Bash:
   ```bash
   mysqldump -u [USERNAME] -p -h [USERNAME].mysql.pythonanywhere-services.com [USERNAME]\$crm_db > crm_dump_new.sql
   ```
2. Speichern Sie die Datei als `crm_dump_new.sql`

---

### Datenbank zurücksetzen

Falls Sie alle Daten löschen und vom Dump neu starten möchten:

**Via Adminer/phpMyAdmin:**
1. **Databases** → Ihre DB
2. Wählen Sie **"Drop database"**
3. Erstellen Sie neue leere Datenbank
4. Importieren Sie `crm_dump.sql` erneut

---

## 7) Sicherheit (für Produktion)

⚠️ **Wichtig:** Diese App ist für Schulung gedacht. Für echten Produktivbetrieb:

1. **SECRET_KEY ändern**
   - Generieren Sie einen zufälligen String
   - `python -c "import secrets; print(secrets.token_hex(32))"`
   - Tragen Sie den in `.env` ein

2. **Admin-Passwort ändern**
   - Nach dem Login zu "Benutzer" → Admin-Konto
   - Passwort ändern

3. **HTTPS**
   - PythonAnywhere bietet kostenloses Let's Encrypt SSL
   - Dashboard: **Web** → **SSL certificates** → Aktivieren

4. **DEBUG ausschalten**
   - In `.env`: `FLASK_DEBUG=False`

5. **Regelmäßige Backups**
   - Wöchentlich `crm_dump.sql` exportieren
   - In separatem Speicher ablegen

---

## 8) Weitere Ressourcen

- **PythonAnywhere Docs:** https://help.pythonanywhere.com
- **Flask Docs:** https://flask.palletsprojects.com
- **SQLAlchemy Docs:** https://docs.sqlalchemy.org
- **MySQL CLI:** https://dev.mysql.com/doc/mysql-shell/8.0/en/

---

## ✅ Checkliste - Installation abgeschlossen?

- [ ] PythonAnywhere Account erstellt
- [ ] MySQL Datenbank erstellt (Zugangsdaten gespeichert)
- [ ] Code hochgeladen (via Git oder ZIP)
- [ ] Virtual Environment erstellt
- [ ] Abhängigkeiten installiert (`pip install -r requirements.txt`)
- [ ] `.env` Datei mit korrekten Zugangsdaten erstellt
- [ ] Datenbank-Tabellen erstellt
- [ ] Dump importiert (Beispieldaten)
- [ ] WSGI-Datei konfiguriert
- [ ] Web-App neu geladen
- [ ] App im Browser erreichbar (`https://[USERNAME].pythonanywhere.com`)
- [ ] Alle 6 Smoke-Tests bestanden
- [ ] Keine Fehler in den Logs

---

## 📞 Support & Fragen

Bei Problemen:
1. Überprüfen Sie die **error.log** in PythonAnywhere
2. Lesen Sie das **Troubleshooting** oben
3. Kontaktieren Sie die Lehrperson mit:
   - Fehlermeldung (exact text)
   - Screenshot der error.log
   - Welcher Schritt schlägt fehl?

---

**Version:** 1.0  
**Datum:** November 2025  
**Zielgruppe:** Lehrperson & Studierende  
**Plattform:** PythonAnywhere
