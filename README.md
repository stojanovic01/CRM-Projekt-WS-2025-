# CRM-System – Informatik-Schulprojekt

Ein einfaches Customer Relationship Management System für Kundenverwaltung, Bestellungen und Kontakt-Tracking.

**Entwickelt mit:** Python 3.11 | Flask | SQLite

---

## 1) Plattform-Check

- **Zielplattform:** PythonAnywhere (https://www.pythonanywhere.com)
- **Datenbank getestet:** SQLite (lokal) / MySQL (optional auf PA)
- **Entscheidung & Begründung:** 
  - SQLite für lokale Entwicklung (keine externe DB nötig)
  - MySQL auf PythonAnywhere optional (PA bietet MySQL an)
  - Einfach, schnell, für Schulprojekt ausreichend

---

## 2) Voraussetzungen

**Tools:**
- FTP-Client oder Git für Code-Transfer
- Browser für PythonAnywhere Dashboard
- Terminal/PowerShell für lokale Entwicklung

**Zugangsdaten:**
- PythonAnywhere Account (kostenlos: https://www.pythonanywhere.com)
- Optional: MySQL Zugangsdaten (werden von PA bereitgestellt)

---

## 3) Schritt-für-Schritt Installation

### Schritt 1: Code hochladen

**Option A: Git (empfohlen)**
```bash
git clone https://github.com/stojanovic01/CRM-Projekt-WS-2025-.git
cd CRM-Projekt-WS-2025-
```

**Option B: Manueller Upload**
- Code-Dateien in `/home/USERNAME/mysite/` hochladen (FTP)
- Ordnerstruktur erhalten bleiben!

### Schritt 2: Abhängigkeiten installieren

```bash
# Virtuelle Umgebung
cd ~/mysite
python3 -m venv venv
source venv/bin/activate

# Dependencies
pip install -r requirements.txt
```

**Was wird installiert:**
- Flask (Web-Framework)
- SQLAlchemy (Datenbank-ORM)
- python-dotenv (Konfiguration)
- PyMySQL (für MySQL, optional)

### Schritt 3: .env erstellen

**Datei:** `CRM-Projekt-WS-2025-/.env`

```ini
FLASK_ENV=production
SECRET_KEY=sicher-generierter-zufallswert-hier
SQLALCHEMY_DATABASE_URI=sqlite:///instance/crm.db
DEBUG=False
TIMEZONE=Europe/Vienna
```

### Schritt 4: Datenbank anlegen/platzieren

**Lokal (SQLite):**
- Datei `crm_dump.sql` existiert bereits
- Auf PythonAnywhere: SQLite DB wird automatisch erstellt

**MySQL (optional auf PythonAnywhere):**
- DB-Name: `USERNAME_crm_db`
- Benutzer wird auf PA konfiguriert

### Schritt 5: Dump importieren

```bash
# SQLite (lokal)
sqlite3 crm_app/instance/crm.db < crm_dump.sql

# MySQL auf PythonAnywhere (über Console)
mysql -u USER -p -h mysql.pythonanywhere-services.com USERNAME_crm_db < crm_dump.sql
```

**Inhalt des Dumps:**
- 6 Tabellen (users, customers, orders, order_items, products, conversations)
- 5 Kunden + 7 Bestellungen + 5 Produkte + 5 Kontakte
- Admin-User: `admin` / `admin` (Passwort ändern!)

### Schritt 6: App starten / WSGI konfigurieren

**Lokal starten:**
```bash
cd crm_app
python app.py
# → http://localhost:5000
```

**Auf PythonAnywhere:**
1. **Web Tab** → Neue Web App erstellen
2. **Framework:** Python 3.11 + Flask
3. **WSGI-Datei bearbeiten:**
   - Pfad: `/var/www/USERNAME_pythonanywhere_com_wsgi.py`
   - Inhalt: Siehe `pythonanywhere_wsgi.py` im Projekt

```python
import sys, os
path = os.path.expanduser('~/mysite/crm_app')
sys.path.insert(0, path)
os.environ['FLASK_ENV'] = 'production'

from app import app as application
```

4. **Reload** → App startet
5. **URL:** `https://USERNAME.pythonanywhere.com`

---

## 4) Smoke-Tests

### Test 1: Website lädt
- Öffne `https://USERNAME.pythonanywhere.com` (lokal: http://localhost:5000)
- ✅ Startseite sichtbar?

### Test 2: Login funktioniert
- Benutzer: `admin`
- Passwort: `admin` (später ändern!)
- ✅ Nach Login: Dashboard sichtbar?

### Test 3: Kunden-Übersicht
- Menü → Customers
- ✅ 5 Kunden sichtbar?

### Test 4: Suchfunktion
- Suche nach "Max" (einer der Test-Kunden)
- ✅ Max Mustermann gefunden?

### Test 5: Kunden-Detail + Datumsfilter
- Kunde anklicken
- Rechts: Bestellungen & Umsatz
- Datumsfilter: "Last 3 Months"
- ✅ Bestellungen gefiltert angezeigt?

### Test 6: Bestellungen
- Menü → Orders
- ✅ 7 Bestellungen sichtbar?

### Test 7: Keine Fehler im Log
```bash
# PythonAnywhere Console
tail -50 /var/log/error.log
# → Sollte keine Python-Fehler enthalten
```

---

## 5) Troubleshooting

| Fehler | Ursache | Lösung |
|--------|--------|--------|
| **502 Bad Gateway** | WSGI-Fehler | WSGI-Datei prüfen, Pfade kontrollieren |
| **404 - not found** | Statische Dateien fehlen | Static Files in PA Dashboard konfigurieren |
| **No module 'app'** | Python-Pfad falsch | sys.path in WSGI anpassen |
| **sqlite: no such table** | Dump nicht importiert | `crm_dump.sql` importieren |
| **500 Internal Error** | Allgemeiner Fehler | Log prüfen (`/var/log/error.log`) |
| **Keine Datenbank-Verbindung** | `.env` fehlt/falsch | `.env` erstellen mit korrekter DB-URI |

### Häufige Fehler beim Debugging

**Fehler:** "ImportError: No module named 'flask'"
- **Grund:** Virtual Environment nicht aktiviert
- **Fix:** `source venv/bin/activate` vor pip-install

**Fehler:** "FileNotFoundError: instance/crm.db"
- **Grund:** Datenbank-Datei existiert nicht
- **Fix:** `crm_dump.sql` importieren oder `touch crm_app/instance/crm.db`

**Fehler:** "500 Error beim Login"
- **Grund:** Benutzer nicht im Dump enthalten
- **Fix:** Dump neu importieren mit `crm_dump.sql`

### Logs überprüfen

**PythonAnywhere:**
```bash
# Error Log
tail -100 /var/log/error.log

# Access Log
tail -100 /var/log/access.log
```

**Lokal:**
- Konsole zeigt Fehler beim Starten
- Flask Debug-Mode: `DEBUG=True` in `.env`

---

## 📁 Projektstruktur (Übersicht)

```
CRM-Projekt-WS-2025-/
├── crm_app/
│   ├── app.py              # Flask-Hauptanwendung
│   ├── models.py           # Datenbank-Modelle
│   ├── config.py           # Konfiguration
│   ├── views/              # Routes & Business-Logik
│   ├── templates/          # HTML-Vorlagen (12 Dateien)
│   ├── static/             # CSS & Bilder
│   └── instance/crm.db     # SQLite Datenbank
├── requirements.txt        # Python-Dependencies
├── pythonanywhere_wsgi.py  # WSGI für PythonAnywhere
├── .env.example            # Konfigurationsvorlage
├── runtime.txt             # Python-Version
├── crm_dump.sql            # Testdaten-Dump
└── README.md               # Diese Datei
```

---

## ✨ Funktionen im Überblick

- **Kundenverwaltung** – Kontaktdaten, Umsatz-Berechnung
- **Bestellungsverwaltung** – Bestellungen mit Positionen
- **Produktkatalog** – Produkt-Verwaltung
- **Kontakt-Tracking** – Telefon, E-Mail, Meeting, Chat
- **Suche & Filter** – Nach Kunden, Datum, Status
- **Benutzer-Rollen** – Admin, Lehrer, Schüler

---

**Fragen?** Siehe `DEPLOYMENT_QUICK_START.md` für erweiterte Anleitung.
