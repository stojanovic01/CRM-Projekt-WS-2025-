import os
from flask import Flask
from dotenv import load_dotenv
from crm_app.models import db, User, Customer, Order, Product, Conversation, OrderItem
from crm_app.config import config

# .env laden
load_dotenv()

# Flask App erstellen
app = Flask(__name__)

# Konfiguration laden
env = os.getenv('FLASK_ENV', 'production')
app.config.from_object(config[env])

# Datenbank initialisieren
db.init_app(app)

# Blueprints registrieren
from crm_app.views.login import login_bp
from crm_app.views.customers import customers_bp
from crm_app.views.orders import orders_bp
from crm_app.views.contacts import contacts_bp

app.register_blueprint(login_bp)
app.register_blueprint(customers_bp)
app.register_blueprint(orders_bp)
app.register_blueprint(contacts_bp)

# Startseite
@app.route('/')
def index():
    return 'CRM System läuft! Gehe zu /login'

# Tabellen erstellen
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=os.getenv('DEBUG', 'False') == 'True')