# Deployment-Anleitung für Easyname Webhosting

## 📋 Übersicht
Diese Anleitung beschreibt, wie Sie die CRM-Anwendung auf Ihrem Easyname-Webhosting-Server deployen.

## 🔑 Zugangsdaten

**FTP-Zugang:**
- Host: `e157104-ftp.services.easyname.eu`
- Benutzername: `243204ftp1`
- Passwort: `01122024spSP.`
- Port: `21`

**MySQL-Datenbank:**
- Host: `localhost` (auf dem Server selbst)
- Datenbank: `u243204db2`
- Benutzername: `u243204db2`
- Passwort: `01122024spSP.`

## 📦 Dateien zum Hochladen

### 1. Haupt-Verzeichnis `crm_app/`

**Dateien hochladen:**
```
crm_app/
├── app.py                      ✓ Hauptanwendung
├── models.py                   ✓ Datenbankmodelle
├── db_config.py                ✓ MySQL-Konfiguration
├── init_mysql_db.py            ✓ Initialisierungsskript
│
├── static/
│   └── style.css               ✓ Stylesheet
│
├── templates/
│   ├── base.html               ✓ Basis-Template
│   ├── index.html              ✓ Login-Seite
│   ├── mainview.html           ✓ Dashboard
│   ├── customers.html          ✓ Kundenliste
│   ├── customer_detail.html    ✓ Kundendetails
│   ├── orders.html             ✓ Bestellungen
│   ├── order_items.html        ✓ Bestellpositionen
│   ├── products.html           ✓ Produkte
│   ├── conversations.html      ✓ Kontakte
│   ├── contacts.html           ✓ Kontaktansicht
│   └── users.html              ✓ Benutzerverwaltung
│
└── views/
    ├── customers.py            ✓ Kunden-Views
    ├── orders.py               ✓ Bestellungen-Views
    ├── contacts.py             ✓ Kontakte-Views
    └── login.py                ✓ Login-Logik
```

### 2. NICHT hochladen (lokal bleiben):
```
❌ __pycache__/                 (Python Cache)
❌ instance/                    (SQLite-Datenbank, nicht benötigt)
❌ migrations/                  (Flask-Migrate, evtl. nicht kompatibel)
❌ scripts/                     (Test-Skripte, nur für Entwicklung)
❌ .git/                        (Git-Verzeichnis)
❌ bishergemacht.txt            (Notizen)
```

### 3. Zusätzliche Dateien (falls benötigt):
```
✓ requirements.txt              (falls vorhanden, für pip install)
```

## 🚀 Deployment-Schritte

### Schritt 1: FTP-Upload mit FileZilla

1. **FileZilla öffnen** und Verbindung herstellen:
   - Host: `e157104-ftp.services.easyname.eu`
   - Benutzername: `243204ftp1`
   - Passwort: `01122024spSP.`
   - Port: `21`

2. **Verzeichnisstruktur auf dem Server:**
   - Navigieren Sie zum Web-Root (meist `/httpdocs/` oder `/public_html/`)
   - Erstellen Sie dort einen Ordner: `crm_app/`

3. **Dateien hochladen (WICHTIG - neue Dateien hinzugefügt!):**
   ```
   crm_app/
   ├── .htaccess                    ✓ NEU! Server-Konfiguration
   ├── passenger_wsgi.py            ✓ NEU! WSGI-Einstiegspunkt
   ├── index.cgi                    ✓ NEU! CGI-Alternative
   ├── requirements.txt             ✓ NEU! Python-Abhängigkeiten
   ├── app.py                       ✓ Hauptanwendung (aktualisiert!)
   ├── models.py                    ✓ Datenbankmodelle
   ├── db_config.py                 ✓ MySQL-Konfiguration
   ├── init_mysql_db.py             ✓ Initialisierungsskript
   │
   ├── static/
   │   └── style.css                ✓ Stylesheet
   │
   ├── templates/
   │   └── *.html                   ✓ Alle 11 HTML-Dateien
   │
   └── views/
       └── *.py                     ✓ Alle 4 Python-Dateien
   ```

4. **Dateirechte setzen (WICHTIG!):**
   - Nach dem Upload in FileZilla:
   - Rechtsklick auf `passenger_wsgi.py` → Dateiberechtigungen → `755` (oder `rwxr-xr-x`)
   - Rechtsklick auf `index.cgi` → Dateiberechtigungen → `755` (oder `rwxr-xr-x`)
   - Rechtsklick auf `.htaccess` → Dateiberechtigungen → `644` (oder `rw-r--r--`)

### Schritt 2: Python-Abhängigkeiten installieren

**Per SSH auf dem Server** (falls SSH-Zugang vorhanden):
```bash
cd /pfad/zu/crm_app
pip3 install --user -r requirements.txt
```

**Falls kein SSH-Zugang:**
- Kontaktieren Sie Easyname Support
- Fragen Sie, wie Sie Python-Pakete installieren können
- Alternative: Fragen Sie nach vorinstallierten Paketen

### Schritt 3: Datenbank wird automatisch initialisiert

Die Anwendung erstellt beim **ersten Aufruf** automatisch:
- Alle Datenbank-Tabellen
- Admin-User (administrator/administrator)
- Beispieldaten (15 Kunden, 60 Bestellungen, 60 Kontakte)

**Keine manuellen Schritte nötig!**

## ⚠️ Wichtige Hinweise

### 1. Python-Version
- Easyname verwendet wahrscheinlich **Python 3.8+**
- Überprüfen Sie die verfügbare Version: `python3 --version`

### 2. App-Modus ändern
In `app.py` die letzte Zeile ändern:
```python
# Für Produktion (auf dem Server):
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
```

### 3. Secret Key
Ändern Sie in `app.py` den Secret Key zu einem sicheren Wert:
```python
app.config['SECRET_KEY'] = 'ERSETZEN_SIE_DIES_MIT_ZUFÄLLIGEM_STRING'
```

### 4. Datenbankzugriff
- MySQL ist nur von **innerhalb des Servers** erreichbar
- Von Ihrem lokalen PC aus können Sie NICHT auf die Datenbank zugreifen
- Verwenden Sie **phpMyAdmin** für Datenbank-Management

### 5. Erste Anmeldung
Nach dem Deployment:
1. Rufen Sie die App auf (z.B. `https://ihre-domain.eu/crm_app/`)
2. Die App erstellt automatisch einen Admin-User
3. Login: `administrator` / `administrator`
4. **Ändern Sie sofort das Passwort!**

## 🔍 Troubleshooting

### Problem: "500 Internal Server Error"
**Lösung:** 
- Überprüfen Sie die Server-Logs (meist in `/logs/error.log`)
- Stellen Sie sicher, dass alle Python-Module installiert sind
- Überprüfen Sie Dateiberechtigungen (755 für Ordner, 644 für Dateien)

### Problem: "Can't connect to MySQL server"
**Lösung:**
- `db_config.py` muss `MYSQL_HOST = 'localhost'` verwenden
- Überprüfen Sie in phpMyAdmin, ob die Datenbank existiert

### Problem: App startet nicht
**Lösung:**
- Überprüfen Sie, ob `passenger_wsgi.py` oder `.htaccess` korrekt konfiguriert ist
- Kontaktieren Sie Easyname Support für Python/Flask-Hosting-Details

## 📞 Support

Bei Problemen mit dem Hosting:
- **Easyname Support:** https://www.easyname.com/de/support
- Fragen Sie speziell nach: "Wie hoste ich eine Flask/Python-Anwendung?"

---

## ✅ Checkliste für Deployment

- [ ] FileZilla mit FTP-Zugangsdaten verbunden
- [ ] Alle Dateien aus `crm_app/` hochgeladen (außer `__pycache__`, `instance/`, `migrations/`)
- [ ] Ordnerstruktur korrekt (`static/`, `templates/`, `views/`)
- [ ] Python-Abhängigkeiten auf dem Server installiert
- [ ] Datenbank über `init_mysql_db.py` oder beim ersten Start initialisiert
- [ ] `.htaccess` oder `passenger_wsgi.py` erstellt (je nach Server-Konfiguration)
- [ ] `app.py` auf `debug=False` gesetzt
- [ ] Secret Key in `app.py` geändert
- [ ] App im Browser aufgerufen und getestet
- [ ] Mit `administrator`/`administrator` eingeloggt
- [ ] Admin-Passwort geändert

**Viel Erfolg mit dem Deployment! 🚀**
