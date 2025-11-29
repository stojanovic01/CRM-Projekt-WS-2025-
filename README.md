# 📊 CRM-Anwendung – Kundenverwaltungssystem

Ein professionelles Kundenmanagementsystem für die Verwaltung von Kunden, Bestellungen, Produkten und Kundenkontakten. Entwickelt mit **Python/Flask** und **MySQL**.

---

## 🎯 Features

✅ **Kundenverwaltung** – Vollständige Kundendatenbank mit Kontaktdaten  
✅ **Bestellungsverwaltung** – Erstellen, bearbeiten und Status verfolgen  
✅ **Produktkatalog** – Verwaltung von Produkten mit SKU und Preisen  
✅ **Gesprächsverlauf** – Dokumentation von Kundeninteraktionen  
✅ **Benutzerrollen** – Admin und Schüler/Lehrer Rollen  
✅ **Datenbankdump** – Fertige Beispieldaten zum Importieren  

---

## 📋 Plattform & Technologie

| Komponente | Details |
|-----------|---------|
| **Plattform** | PythonAnywhere (pythonanywhere.com) |
| **Sprache** | Python 3.8+ |
| **Framework** | Flask 3.0+ |
| **Datenbank** | MySQL 5.7+ |
| **ORM** | SQLAlchemy 2.0+ |

---

## 📂 Projektstruktur

```
CRM-Projekt-WS-2025-/
├── crm_app/
│   ├── app.py                    # Hauptanwendung
│   ├── models.py                 # Datenbankmodelle
│   ├── db_config.py              # Lokale DB-Konfiguration
│   ├── requirements.txt           # Python-Abhängigkeiten
│   ├── .env.example              # Konfigurationsvorlage
│   │
│   ├── views/                    # Flask-Views
│   │   ├── customers.py
│   │   ├── orders.py
│   │   ├── contacts.py
│   │   └── login.py
│   │
│   ├── templates/                # HTML-Templates
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── mainview.html
│   │   ├── customers.html
│   │   ├── customer_detail.html
│   │   ├── orders.html
│   │   ├── products.html
│   │   ├── conversations.html
│   │   ├── contacts.html
│   │   └── users.html
│   │
│   ├── static/                   # CSS/Assets
│   │   └── style.css
│   │
│   └── instance/                 # Runtime-Daten (nicht versioniert)
│       └── crm_app.db            # SQLite Datenbank (lokal)
│
├── crm_dump.sql                  # Datenbank-Dump mit Beispieldaten
├── INSTALLATION.md               # ⭐ Installation & Migration
├── README.md                     # Diese Datei
└── .git/                         # Git-Versionskontrolle
```

---

## 🚀 Quick Start

### Für lokale Entwicklung

```bash
# 1. Abhängigkeiten installieren
cd crm_app
pip install -r requirements.txt

# 2. App starten
python app.py

# 3. Im Browser öffnen
# http://localhost:5000
# Login: administrator / administrator
```

### Für PythonAnywhere Deployment

**Siehe:** [INSTALLATION.md](INSTALLATION.md) ← **START HIER!**

Die Datei enthält eine vollständige Schritt-für-Schritt-Anleitung mit:
- ✅ PythonAnywhere Account-Setup
- ✅ MySQL Datenbank-Konfiguration
- ✅ Code-Upload und WSGI-Konfiguration
- ✅ Datenbank-Migrationen mit Beispieldaten
- ✅ Smoke-Tests zur Validierung
- ✅ Troubleshooting für häufige Probleme

---

## 🔑 Standard-Anmeldedaten

Nach Installation mit Dump verfügbar:

| Feld | Wert |
|------|------|
| **Benutzer** | `administrator` |
| **Passwort** | `administrator` |
| **Rolle** | Admin |

⚠️ **Nach dem Login Passwort ändern!**

---

## 📦 Dateien zur Verteilung

### Erforderlich

- ✅ `crm_app/` – Komplette Anwendung
- ✅ `crm_dump.sql` – Datenbank-Dump mit Schema & Beispieldaten
- ✅ `INSTALLATION.md` – Anleitung für Deployment
- ✅ `requirements.txt` – Python-Abhängigkeiten
- ✅ `.env.example` – Konfigurationsvorlage

### Optional

- 📄 `.git/` – Git-Repository (für Versionskontrolle)
- 📄 `instance/` – Lokale Daten (nicht notwendig auf Server)

---

## 🗄️ Datenbank

### Schema

Die Anwendung verwendet folgende Tabellen:

- **users** – Benutzeraccounts (Administrator, Schüler, Lehrer)
- **customers** – Kundendaten
- **products** – Produktkatalog
- **orders** – Bestellungen
- **order_items** – Bestellpositionen
- **conversations** – Kundengespräche

### Dump-Import

Die Datei `crm_dump.sql` enthält:
- ✅ Vollständiges Schema mit Foreign Keys
- ✅ Admin-Benutzer (administrator/administrator)
- ✅ 5 Beispiel-Kunden
- ✅ 5 Beispiel-Produkte
- ✅ 7 Beispiel-Bestellungen mit Positionen
- ✅ 8 Beispiel-Gespräche

Import auf PythonAnywhere: Siehe [INSTALLATION.md → Schritt 8](INSTALLATION.md#schritt-8-datenbank-dump-importieren-beispieldaten)

---

## 🔐 Sicherheit

⚠️ **Diese App ist für Schulung/Demonstrationszwecke.**

Für Produktion notwendig:
1. `SECRET_KEY` in `.env` ändern (sicher generieren)
2. Admin-Passwort ändern
3. HTTPS aktivieren (PythonAnywhere: kostenlos mit Let's Encrypt)
4. Regelmäßige Datenbank-Backups
5. Input-Validierung überprüfen
6. CORS und CSRF-Protection konfigurieren

---

## 📖 Dokumentation

| Datei | Inhalt |
|-------|--------|
| **[INSTALLATION.md](INSTALLATION.md)** | 🌟 Schritt-für-Schritt Anleitung für PythonAnywhere |
| **[crm_dump.sql](crm_dump.sql)** | Datenbank-Schema & Beispieldaten |
| **[.env.example](crm_app/.env.example)** | Konfigurationsvorlage |

---

## 🛠️ Technische Details

### Flask-Konfiguration

```python
# Datenbankverbindung aus .env
SQLALCHEMY_DATABASE_URI=mysql+pymysql://user:pass@host/database?charset=utf8mb4

# Oder lokal SQLite
SQLALCHEMY_DATABASE_URI=sqlite:///app.db
```

### WSGI für PythonAnywhere

```python
import sys, os
path = os.path.expanduser('~/CRM-Projekt-WS-2025-/crm_app')
sys.path.insert(0, path)
os.environ.setdefault('FLASK_ENV', 'production')

from app import app as application
```

### Abhängigkeiten

Siehe `crm_app/requirements.txt`:
- Flask 3.0.0
- Flask-SQLAlchemy 3.1.1
- SQLAlchemy 2.0.23
- PyMySQL 1.1.2
- python-dotenv 1.0.0
- gunicorn 21.2.0

---

## 🧪 Tests

### Smoke-Tests (nach Installation)

1. **Anmeldung** – Login mit `administrator/administrator`
2. **Kunden-Übersicht** – 5 Beispiel-Kunden sichtbar
3. **Kundendetails** – Bestellungen & Gespräche angezeigt
4. **Bestellungen** – 7 Bestellungen mit Positionen
5. **Produkte** – 5 Beispiel-Produkte sichtbar
6. **Logs** – Keine Fehler in `error.log`

Details: [INSTALLATION.md → Smoke-Tests](INSTALLATION.md#4-smoke-tests-validierung)

---

## 🐛 Troubleshooting

### Häufige Probleme

**"Can't connect to MySQL server"**
- Überprüfen Sie `.env` – Zugangsdaten korrekt?
- Testen Sie die Verbindung: `mysql -u USER -p -h HOST DATABASE`

**"No module named 'app'"**
- Virtual Environment aktiviert? `source ~/.virtualenvs/crm_env/bin/activate`
- Pfad korrekt in WSGI-Datei?

**"500 Internal Server Error"**
- Siehe `error.log` in PythonAnywhere Dashboard
- Häufig: Fehlende `.env` oder falsche Datenbank-URI

**"CSS lädt nicht"**
- Static Files konfiguriert? Dashboard: **Web** → **Static files**
- URL: `/static/` → Directory: `/home/.../crm_app/static/`

Vollständiges Troubleshooting: [INSTALLATION.md → Troubleshooting](INSTALLATION.md#5-troubleshooting)

---

## 📞 Support & Ressourcen

- **PythonAnywhere Dokumentation:** https://help.pythonanywhere.com
- **Flask Dokumentation:** https://flask.palletsprojects.com
- **SQLAlchemy Dokumentation:** https://docs.sqlalchemy.org
- **MySQL Dokumentation:** https://dev.mysql.com

---

## 📄 Lizenz & Hinweise

**CRM-Anwendung**  
Schulprojekt – Frei verwendbar für Bildungszwecke  
© 2025

Technologie:
- Backend: Python 3 + Flask
- ORM: SQLAlchemy
- Datenbank: MySQL
- Hosting: PythonAnywhere
- Frontend: Jinja2 Templates + Bootstrap (via CDN)

---

## ✅ Checkliste für Benutzer

Für erfolgreiche Installation:

- [ ] PythonAnywhere Account erstellt
- [ ] MySQL Datenbank angelegt
- [ ] Code hochgeladen
- [ ] `requirements.txt` installiert
- [ ] `.env` erstellt mit korrekten Werten
- [ ] WSGI-Datei konfiguriert
- [ ] Datenbank-Dump importiert
- [ ] App neu geladen ("Reload")
- [ ] Website erreichbar unter `https://[USERNAME].pythonanywhere.com`
- [ ] Login funktioniert
- [ ] Alle Smoke-Tests erfolgreich

---

## 🎉 Nächste Schritte

1. **Installation:** Folgen Sie [INSTALLATION.md](INSTALLATION.md)
2. **Testen:** Durchlaufen Sie die Smoke-Tests
3. **Anpassen:** Passen Sie `.env` und Datenbankwerte an
4. **Verwenden:** Kunden & Bestellungen verwalten!

---

**Version:** 1.0  
**Letztes Update:** November 2025  
**Plattform:** PythonAnywhere  
**Sprache:** Python 3 + Flask
