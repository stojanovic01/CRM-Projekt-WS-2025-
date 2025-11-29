"""
Testet die MySQL-Verbindung
"""
import pymysql
import sys

# Konfiguration
try:
    from db_config import MYSQL_HOST, MYSQL_PORT, MYSQL_DATABASE, MYSQL_USER, MYSQL_PASSWORD
except ImportError:
    MYSQL_HOST = 'localhost'
    MYSQL_PORT = 3306
    MYSQL_DATABASE = 'u243204db2'
    MYSQL_USER = 'u243204db2'
    MYSQL_PASSWORD = '01122024spSP.'

print("=" * 60)
print("MySQL-Verbindungstest")
print("=" * 60)
print(f"Host:     {MYSQL_HOST}")
print(f"Port:     {MYSQL_PORT}")
print(f"Datenbank: {MYSQL_DATABASE}")
print(f"Benutzer:  {MYSQL_USER}")
print("=" * 60)

try:
    print("\n🔄 Versuche Verbindung herzustellen...")
    connection = pymysql.connect(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DATABASE,
        charset='utf8mb4'
    )
    
    print("✅ Verbindung erfolgreich!")
    
    # Zeige MySQL-Version
    cursor = connection.cursor()
    cursor.execute("SELECT VERSION()")
    version = cursor.fetchone()
    print(f"✅ MySQL-Version: {version[0]}")
    
    # Zeige vorhandene Tabellen
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    if tables:
        print(f"✅ Vorhandene Tabellen ({len(tables)}):")
        for table in tables:
            print(f"   - {table[0]}")
    else:
        print("ℹ️  Keine Tabellen vorhanden (Datenbank ist leer)")
    
    cursor.close()
    connection.close()
    
    print("\n" + "=" * 60)
    print("✅ Verbindungstest erfolgreich!")
    print("=" * 60)
    print("\nSie können jetzt init_mysql_db.py ausführen, um die Tabellen zu erstellen.")
    
except pymysql.err.OperationalError as e:
    print(f"\n❌ Verbindungsfehler: {e}")
    print("\n💡 Mögliche Lösungen:")
    print("   1. Stellen Sie sicher, dass MySQL läuft")
    print("      - Bei XAMPP: Starten Sie XAMPP Control Panel → MySQL starten")
    print("      - Bei MAMP: Starten Sie MAMP → MySQL starten")
    print("   2. Überprüfen Sie die Zugangsdaten in db_config.py")
    print("   3. Überprüfen Sie, ob die Datenbank existiert")
    print("   4. Bei Remote-Server: Prüfen Sie Firewall/Port-Freigabe")
    sys.exit(1)
    
except Exception as e:
    print(f"\n❌ Unerwarteter Fehler: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
