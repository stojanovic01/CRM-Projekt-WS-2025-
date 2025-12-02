import os
from flask import Flask, redirect, url_for, render_template, session
from dotenv import load_dotenv
from config import config
from extensions import db  # Deine globale SQLAlchemy-Instanz

# Blueprints importieren
from views.login import login_bp
from views.customers import customers_bp
from views.orders import orders_bp
from views.contacts import contacts_bp

# .env laden
load_dotenv()

# Flask App erzeugen
app = Flask(__name__, template_folder='templates')

# Konfiguration laden
env = os.getenv('FLASK_ENV', 'production')
app.config.from_object(config[env])

# Datenbank initialisieren
db.init_app(app)

# Blueprints registrieren
app.register_blueprint(login_bp)
app.register_blueprint(customers_bp)
app.register_blueprint(orders_bp)
app.register_blueprint(contacts_bp)

# Startseite -> direkt weiterleiten zur Login-Seite
@app.route('/')
def index():
    return redirect(url_for('login.login'))

# Route für die firstpage.html nach Login
@app.route('/firstpage')
def firstpage():
    if 'user_id' not in session:
        return redirect(url_for('login.login'))
    return render_template('firstpage.html')

# Tabellen erstellen (nur beim Start)
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'])
