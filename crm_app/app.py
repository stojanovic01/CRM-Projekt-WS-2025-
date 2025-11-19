# app.py
from flask import Flask, render_template, request, redirect, url_for, flash, session
import os
import hashlib
import re
from functools import wraps
from datetime import datetime, timedelta
from models import db, User, Customer, Order, Product, Conversation
from views.customers import customers_bp
from flask_migrate import Migrate

app = Flask(__name__)

# MySQL Datenbankverbindung
# Importiere Konfiguration aus db_config.py
try:
    from db_config import MYSQL_HOST, MYSQL_PORT, MYSQL_DATABASE, MYSQL_USER, MYSQL_PASSWORD
    has_port = True
except ImportError:
    # Fallback falls db_config.py nicht existiert
    MYSQL_HOST = 'localhost'
    MYSQL_PORT = 3306
    MYSQL_DATABASE = 'u243204db2'
    MYSQL_USER = 'u243204db2'
    MYSQL_PASSWORD = '01122024spSP.'
    has_port = False

# SQLAlchemy Connection String für MySQL mit pymysql
if has_port and MYSQL_PORT != 3306:
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}?charset=utf8mb4'
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DATABASE}?charset=utf8mb4'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'dev-secret-change-in-production'  # für flash messages

print(f"📊 Verbinde mit MySQL-Datenbank: {MYSQL_DATABASE} @ {MYSQL_HOST}")

db.init_app(app)
migrate = Migrate(app, db)

# Hilfsfunktionen für Formatierung
def format_currency(amount):
    """Formatiere Betrag im deutschen Format: 1.234,56 €"""
    if amount is None:
        return '0,00 €'
    return f"{amount:,.2f} €".replace(',', 'X').replace('.', ',').replace('X', '.')

def format_date(date_obj, with_time=False):
    """Formatiere Datum im deutschen Format: dd.mm.YYYY (HH:MM)"""
    if not date_obj:
        return 'N/A'
    if with_time:
        return date_obj.strftime('%d.%m.%Y %H:%M')
    return date_obj.strftime('%d.%m.%Y')

# Validierungsfunktionen
def validate_email(email):
    """Validiere E-Mail-Format"""
    if not email:
        return True  # E-Mail ist optional
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_phone(phone):
    """Validiere Telefonnummer (einfache Prüfung)"""
    if not phone:
        return True  # Telefon ist optional
    # Erlaubt: +, -, Leerzeichen, Zahlen, Klammern
    pattern = r'^[\d\s\+\-\(\)]+$'
    return re.match(pattern, phone) is not None and len(phone.replace(' ', '').replace('-', '').replace('+', '').replace('(', '').replace(')', '')) >= 6

# Template-Filter registrieren
@app.template_filter('currency')
def currency_filter(amount):
    return format_currency(amount)

@app.template_filter('date')
def date_filter(date_obj):
    return format_date(date_obj)

@app.template_filter('datetime')
def datetime_filter(date_obj):
    return format_date(date_obj, with_time=True)

def create_admin_user():
    """Erstelle Admin-User falls noch nicht vorhanden"""
    admin = User.query.filter_by(name='administrator').first()
    if not admin:
        # SHA256 Hash von "administrator"
        password_hash = hashlib.sha256('administrator'.encode()).hexdigest()
        admin = User(
            name='administrator',
            email='admin@crm.local',
            password_hash=password_hash,
            role='Admin'
        )
        db.session.add(admin)
        db.session.commit()
        print("Admin-User 'administrator' erstellt")

def create_sample_data():
    """Erstelle realistische Testdaten für Kunden, Produkte und Bestellungen"""
    # Prüfe ob bereits Daten vorhanden sind
    if Customer.query.count() > 0:
        return
    
    # Österreichische/Deutsche Unternehmen mit Ansprechpartnern (erweitert auf 15 Kunden)
    contacts_data = [
        {"first_name": "Maria", "last_name": "Schmidt", "email": "m.schmidt@tgm.ac.at", "phone": "+43 1 33126-102"},
        {"first_name": "Thomas", "last_name": "Müller", "email": "t.mueller@siemens.com", "phone": "+43 1 71707-234"},
        {"first_name": "Sarah", "last_name": "Weber", "email": "s.weber@bmw.at", "phone": "+43 1 25125-567"},
        {"first_name": "Michael", "last_name": "Fischer", "email": "m.fischer@erstegroup.com", "phone": "+43 1 53100-890"},
        {"first_name": "Andrea", "last_name": "Wagner", "email": "a.wagner@basf.at", "phone": "+43 1 71175-123"},
        {"first_name": "Robert", "last_name": "Bauer", "email": "r.bauer@microsoft.at", "phone": "+43 1 61616-456"},
        {"first_name": "Julia", "last_name": "Hofmann", "email": "j.hofmann@sap.com", "phone": "+43 1 28818-789"},
        {"first_name": "Christian", "last_name": "Steiner", "email": "c.steiner@redbull.com", "phone": "+43 662 6582-012"},
        {"first_name": "Lisa", "last_name": "Mayer", "email": "l.mayer@bosch.at", "phone": "+43 1 79730-345"},
        {"first_name": "Klaus", "last_name": "Berger", "email": "k.berger@telekom.at", "phone": "+43 1 79585-678"},
        {"first_name": "Anna", "last_name": "Huber", "email": "a.huber@porsche.at", "phone": "+43 1 91104-901"},
        {"first_name": "Stefan", "last_name": "Gruber", "email": "s.gruber@voest.at", "phone": "+43 732 6585-234"},
        {"first_name": "Petra", "last_name": "Pichler", "email": "p.pichler@ams.at", "phone": "+43 3842 200-567"},
        {"first_name": "Markus", "last_name": "Eder", "email": "m.eder@andritz.com", "phone": "+43 316 6902-890"},
        {"first_name": "Sophie", "last_name": "Lang", "email": "s.lang@frequentis.com", "phone": "+43 1 81150-123"}
    ]
    
    # Produkte erstellen (ohne description Feld)
    products_data = [
        {"sku": "SW-PREM-2025", "name": "Software Lizenz Premium", "price": 2499.99},
        {"sku": "HW-MAINT-365", "name": "Hardware Wartungspaket", "price": 8999.99},
        {"sku": "CLD-BUS-1TB", "name": "Cloud Storage Business", "price": 199.99},
        {"sku": "SEC-ENT-SUI", "name": "Security Suite Enterprise", "price": 4999.99},
        {"sku": "TRN-WS-2DAY", "name": "Training Workshop", "price": 1299.99}
    ]
    
    # Produkte in DB speichern
    products = []
    for prod_data in products_data:
        product = Product(
            sku=prod_data["sku"],
            name=prod_data["name"],
            base_price=prod_data["price"]
        )
        db.session.add(product)
        products.append(product)
    
    # Kunden erstellen (mit first_name/last_name)
    customers = []
    for i, contact in enumerate(contacts_data):
        customer = Customer(
            first_name=contact["first_name"],
            last_name=contact["last_name"],
            email=contact["email"],
            phone=contact["phone"],
            created_at=datetime.now() - timedelta(days=i*15)  # Gestaffelte Erstellungsdaten
        )
        db.session.add(customer)
        customers.append(customer)
    
    db.session.commit()  # Erst committen damit IDs verfügbar sind
    
    # Bestellungen erstellen (mit korrekten Status-Werten) - erhöht auf 60 Bestellungen
    import random
    order_statuses = ['Offen', 'Bezahlt', 'Storniert']  # Diese Werte sind im Model definiert
    
    for i in range(60):  # 60 Bestellungen (für ≥50 Kriterium)
        customer = random.choice(customers)
        
        # Realistische Bestelldaten der letzten 120 Tage
        order_date = datetime.now() - timedelta(days=random.randint(0, 120))
        
        order = Order(
            customer_id=customer.id,
            order_date=order_date,
            status=random.choice(order_statuses),
            total_amount=round(random.uniform(500, 15000), 2)
        )
        db.session.add(order)
    
    db.session.commit()
    
    # Erstelle auch einige Kontakte zu den Kunden
    admin_user = User.query.filter_by(name='administrator').first()
    if admin_user and len(customers) > 0:
        import random
        channels = ['Telefon', 'E-Mail', 'Meeting', 'Chat']
        contact_subjects = [
            'Erstkontakt - Interesse an unseren Lösungen',
            'Nachfrage zu Produktdetails',
            'Vertragsverhandlung',
            'Support-Anfrage',
            'Follow-up nach Meeting',
            'Terminvereinbarung',
            'Beschwerdebearbeitung',
            'Angebotsnachfrage'
        ]
        
        sample_notes = [
            'Kunde zeigt großes Interesse an unserer Premium-Lösung. Nächster Schritt: Detailliertes Angebot erstellen.',
            'Technische Fragen zur Integration geklärt. Kunde benötigt noch Bedenkzeit.',
            'Sehr positives Gespräch. Kunde möchte Testphase vereinbaren.',
            'Support-Case erfolgreich gelöst. Kunde ist zufrieden mit der schnellen Bearbeitung.',
            'Preisverhandlung läuft gut. Kompromiss bei Lizenzanzahl gefunden.',
            'Terminvereinbarung für nächste Woche. Präsentation vorbereiten.',
            'Beschwerde bezüglich Lieferverzug. Entschädigungsmaßnahmen besprochen.',
            'Kunde interessiert sich für Zusatzmodule. Cross-selling Potenzial vorhanden.'
        ]
        
        for i in range(60):  # 60 Konversationen (für ≥50 Kriterium)
            customer = random.choice(customers)
            contact_time = datetime.now() - timedelta(days=random.randint(0, 120), hours=random.randint(0, 23))

            conversation = Conversation(
                customer_id=customer.id,
                user_id=admin_user.id,
                channel=random.choice(channels),
                subject=random.choice(contact_subjects),
                notes=random.choice(sample_notes),
                conversation_time=contact_time
            )
            db.session.add(conversation)
    
    db.session.commit()
    print("Testdaten erfolgreich erstellt: 15 Kunden, 5 Produkte, 60 Bestellungen, 60 Kontakte")

def login_required(f):
    """Decorator für geschützte Routen"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Bitte loggen Sie sich zuerst ein')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/', methods=['GET', 'POST'])
def index():
    # Wenn bereits eingeloggt, weiterleiten zum Dashboard
    if 'user_id' in session:
        return redirect(url_for('mainview'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        
        if not username or not password:
            flash('Benutzername und Passwort sind erforderlich')
            return render_template('index.html')
        
        # Hash das eingegebene Passwort
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        # Suche User in DB
        user = User.query.filter_by(name=username, password_hash=password_hash).first()
        
        if user:
            # Login erfolgreich - Session setzen
            session['user_id'] = user.id
            session['username'] = user.name
            flash('Erfolgreich angemeldet!')
            return redirect(url_for('mainview'))
        else:
            flash('Ungültiger Benutzername oder Passwort')
    
    return render_template('index.html')

@app.route('/logout')
@login_required
def logout():
    session.clear()
    flash('Sie wurden erfolgreich abgemeldet')
    return redirect(url_for('index'))

@app.route('/mainview')
@login_required
def mainview():
    from models import Customer, Order, Conversation
    from datetime import datetime
    from sqlalchemy import or_
    
    # Suchparameter und Paginierung
    customer_search = request.args.get('customer_search', '').strip()
    order_search = request.args.get('order_search', '').strip()
    customer_page = request.args.get('customer_page', 1, type=int)
    order_page = request.args.get('order_page', 1, type=int)
    per_page = 10
    
    # Kunden-Query mit Suche und Paginierung
    customers_query = Customer.query
    if customer_search:
        search_pattern = f"%{customer_search}%"
        customers_query = customers_query.filter(
            or_(
                Customer.first_name.ilike(search_pattern),
                Customer.last_name.ilike(search_pattern),
                Customer.email.ilike(search_pattern),
                Customer.phone.ilike(search_pattern)
            )
        )
    customers_pagination = customers_query.order_by(Customer.created_at.desc()).paginate(
        page=customer_page, per_page=per_page, error_out=False
    )
    
    # Bestellungen-Query mit Suche und Paginierung
    orders_query = Order.query.join(Customer)
    if order_search:
        search_pattern = f"%{order_search}%"
        orders_query = orders_query.filter(
            or_(
                Customer.first_name.ilike(search_pattern),
                Customer.last_name.ilike(search_pattern),
                Order.status.ilike(search_pattern)
            )
        )
    orders_pagination = orders_query.order_by(Order.order_date.desc()).paginate(
        page=order_page, per_page=per_page, error_out=False
    )
    
    current_date = datetime.now().strftime("%d.%m.%Y")
    username = session.get('username', 'Unbekannt')
    
    return render_template('mainview.html',
                         customers_pagination=customers_pagination,
                         orders_pagination=orders_pagination,
                         current_date=current_date,
                         username=username,
                         customer_search=customer_search,
                         order_search=order_search)

@app.route('/customers', methods=['GET', 'POST'])
@login_required
def customers():
    if request.method == 'POST':
        # Add or edit customer
        customer_id = request.form.get('customer_id')
        first_name = request.form.get('first_name', '').strip()
        last_name = request.form.get('last_name', '').strip()
        email = request.form.get('email', '').strip() or None
        phone = request.form.get('phone', '').strip() or None
        
        # Validierung
        if not first_name or not last_name:
            flash('❌ Vorname und Nachname sind erforderlich')
            return redirect(url_for('customers'))
        
        if len(first_name) > 100 or len(last_name) > 100:
            flash('❌ Name darf maximal 100 Zeichen lang sein')
            return redirect(url_for('customers'))
        
        if email and not validate_email(email):
            flash('❌ Ungültige E-Mail-Adresse')
            return redirect(url_for('customers'))
        
        if phone and not validate_phone(phone):
            flash('❌ Ungültige Telefonnummer (mindestens 6 Ziffern)')
            return redirect(url_for('customers'))
        
        try:
            if customer_id:  # Edit existing
                customer = Customer.query.get_or_404(customer_id)
                customer.first_name = first_name
                customer.last_name = last_name
                customer.email = email
                customer.phone = phone
                flash(f'✅ Kontakt "{first_name} {last_name}" wurde erfolgreich aktualisiert')
            else:  # Add new
                customer = Customer(
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    phone=phone
                )
                db.session.add(customer)
                flash(f'✅ Neuer Kontakt "{first_name} {last_name}" wurde erfolgreich hinzugefügt')
            
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            flash(f'❌ Fehler beim Speichern: {str(e)}')
        
        return redirect(url_for('customers'))
    
    # GET request - show all customers with pagination
    page = request.args.get('page', 1, type=int)
    per_page = 15
    search = request.args.get('search', '').strip()
    
    customers_query = Customer.query
    if search:
        from sqlalchemy import or_
        search_pattern = f"%{search}%"
        customers_query = customers_query.filter(
            or_(
                Customer.first_name.ilike(search_pattern),
                Customer.last_name.ilike(search_pattern),
                Customer.email.ilike(search_pattern),
                Customer.phone.ilike(search_pattern)
            )
        )
    
    customers_pagination = customers_query.order_by(Customer.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return render_template('customers.html', 
                         customers_pagination=customers_pagination,
                         search=search)


@app.route('/customers/<int:customer_id>')
@login_required
def customer_detail(customer_id):
    from datetime import datetime, timedelta
    from sqlalchemy import func

    customer = Customer.query.get_or_404(customer_id)

    # Date range filter for KPIs and order list (optional)
    start_str = request.args.get('start')
    end_str = request.args.get('end')
    start_dt = None
    end_dt = None
    try:
        if start_str:
            start_dt = datetime.fromisoformat(start_str)
        if end_str:
            # parse end date and set to end of day
            end_dt = datetime.fromisoformat(end_str)
            end_dt = end_dt + timedelta(hours=23, minutes=59, seconds=59)
    except Exception:
        start_dt = None
        end_dt = None

    # Orders for this customer (apply date filter if present)
    orders_query = Order.query.filter_by(customer_id=customer.id)
    if start_dt:
        orders_query = orders_query.filter(Order.order_date >= start_dt)
    if end_dt:
        orders_query = orders_query.filter(Order.order_date <= end_dt)
    recent_orders = orders_query.order_by(Order.order_date.desc()).limit(10).all()

    # KPIs: total revenue (all time or in date range) and revenue last calendar year
    total_query = db.session.query(func.coalesce(func.sum(Order.total_amount), 0)).filter(Order.customer_id == customer.id)
    if start_dt:
        total_query = total_query.filter(Order.order_date >= start_dt)
    if end_dt:
        total_query = total_query.filter(Order.order_date <= end_dt)
    total_revenue = float(total_query.scalar() or 0)

    # Revenue for last calendar year
    now = datetime.now()
    last_year_start = datetime(now.year - 1, 1, 1)
    last_year_end = datetime(now.year - 1, 12, 31, 23, 59, 59)
    last_year_query = db.session.query(func.coalesce(func.sum(Order.total_amount), 0)).filter(Order.customer_id == customer.id, Order.order_date >= last_year_start, Order.order_date <= last_year_end)
    revenue_last_year = float(last_year_query.scalar() or 0)

    # Last conversations (timeline, newest first)
    conversations_list = Conversation.query.filter_by(customer_id=customer.id).order_by(Conversation.conversation_time.desc()).limit(10).all()

    # Last conversation summary (for header)
    last_conversation = Conversation.query.filter_by(customer_id=customer.id).order_by(Conversation.conversation_time.desc()).first()

    return render_template('customer_detail.html',
                           customer=customer,
                           recent_orders=recent_orders,
                           conversations_list=conversations_list,
                           total_revenue=total_revenue,
                           revenue_last_year=revenue_last_year,
                           last_conversation=last_conversation,
                           start=start_str,
                           end=end_str)

@app.route('/customers/delete/<int:customer_id>')
@login_required
def delete_customer(customer_id):
    try:
        customer = Customer.query.get_or_404(customer_id)
        name = f"{customer.first_name} {customer.last_name}"
        db.session.delete(customer)
        db.session.commit()
        flash(f'Kontakt "{name}" wurde erfolgreich gelöscht')
    except Exception as e:
        db.session.rollback()
        flash(f'Fehler beim Löschen: {str(e)}')
    
    return redirect(url_for('customers'))

@app.route('/conversations', methods=['GET', 'POST'])
@login_required
def conversations():
    if request.method == 'POST':
        # Add or edit contact
        conversation_id = request.form.get('contact_id')
        customer_id = request.form.get('customer_id')
        channel = request.form.get('channel')
        subject = request.form.get('subject', '').strip() or None
        notes = request.form.get('notes', '').strip()
        contact_time_str = request.form.get('contact_time')
        
        # Validierung
        if not customer_id or not channel or not notes or not contact_time_str:
            flash('❌ Kunde, Kanal, Notizen und Konversationszeit sind erforderlich')
            return redirect(url_for('conversations'))
        
        if len(notes) < 10:
            flash('❌ Notizen müssen mindestens 10 Zeichen lang sein')
            return redirect(url_for('conversations'))
        
        if subject and len(subject) > 255:
            flash('❌ Betreff darf maximal 255 Zeichen lang sein')
            return redirect(url_for('conversations'))

        try:
            # Parse contact time
            contact_time = datetime.fromisoformat(contact_time_str.replace('T', ' '))

            # Get current user ID
            current_user = User.query.filter_by(name=session.get('username')).first()
            user_id = current_user.id if current_user else None

            if conversation_id:  # Edit existing
                conversation = Conversation.query.get_or_404(conversation_id)
                conversation.customer_id = customer_id
                conversation.channel = channel
                conversation.subject = subject
                conversation.notes = notes
                conversation.conversation_time = contact_time
                flash('✅ Konversation wurde erfolgreich aktualisiert')
            else:  # Add new
                conversation = Conversation(
                    customer_id=customer_id,
                    user_id=user_id,
                    channel=channel,
                    subject=subject,
                    notes=notes,
                    conversation_time=contact_time
                )
                db.session.add(conversation)
                flash('✅ Neue Konversation wurde erfolgreich dokumentiert')

            db.session.commit()
        except Exception as e:
            db.session.rollback()
            flash(f'❌ Fehler beim Speichern: {str(e)}')

        return redirect(url_for('conversations'))
    
    # GET request - show all contacts with pagination
    import json
    page = request.args.get('page', 1, type=int)
    per_page = 15

    # Optionaler Filter per Kanal (channel), Suche (q) und Sortierung (order)
    selected_channel = request.args.get('channel', None)
    search_q = request.args.get('q', None)
    order = request.args.get('order', 'desc')  # 'desc' (default) oder 'asc'

    # Basisquery
    query = Conversation.query
    # apply channel filter
    if selected_channel:
        query = query.filter_by(channel=selected_channel)

    # apply full-text-ish search across customer name, subject, notes and channel
    if search_q:
        # Use cast to string for enum column before doing ilike to avoid SQLAlchemy Enum
        # lookup/validation errors when the parameter contains wildcard patterns.
        from sqlalchemy import or_, cast, String
        q_like = f"%{search_q}%"
        # join Customer to allow searching by name
        query = query.join(Customer).filter(
            or_(
                Customer.first_name.ilike(q_like),
                Customer.last_name.ilike(q_like),
                Conversation.subject.ilike(q_like),
                Conversation.notes.ilike(q_like),
                cast(Conversation.channel, String).ilike(q_like),
            )
        )

    # Sortierung nach Kontaktzeit (default: neueste zuerst)
    if order == 'asc':
        query = query.order_by(Conversation.conversation_time.asc())
    else:
        query = query.order_by(Conversation.conversation_time.desc())
    
    # Paginierung
    conversations_pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    customers_list = Customer.query.order_by(Customer.first_name, Customer.last_name).all()

    # Liste vorhandener Kanäle für das Filter-Dropdown (aus DB)
    channels_raw = db.session.query(Conversation.channel).distinct().all()
    channels_list = [c[0] for c in channels_raw if c[0]]

    # Prepare JSON data for JavaScript
    contacts_json = []
    for contact in conversations_pagination.items:
        contacts_json.append({
            'id': contact.id,
            'customer_id': contact.customer_id,
            'customer_name': f"{contact.customer.first_name} {contact.customer.last_name}" if contact.customer else None,
            'channel': contact.channel,
            'subject': contact.subject,
            'notes': contact.notes,
            'conversation_time': contact.conversation_time.isoformat() if contact.conversation_time else None,
            'conversation_time_formatted': contact.conversation_time.strftime('%d.%m.%Y %H:%M') if contact.conversation_time else None
        })
    
    return render_template('conversations.html', 
                         conversations_pagination=conversations_pagination,
                         customers=customers_list,
                         contacts_json=json.dumps(contacts_json),
                         channels=channels_list,
                         selected_channel=selected_channel,
                         current_order=order,
                         search_q=search_q)

@app.route('/conversations/delete/<int:contact_id>')
@login_required
def delete_contact(contact_id):
    try:
        conversation = Conversation.query.get_or_404(contact_id)
        subject = conversation.subject or 'Konversation'
        db.session.delete(conversation)
        db.session.commit()
        flash(f'Konversation "{subject}" wurde erfolgreich gelöscht')
    except Exception as e:
        db.session.rollback()
        flash(f'Fehler beim Löschen: {str(e)}')
    
    return redirect(url_for('conversations'))


@app.route('/orders/create', methods=['POST'])
@login_required
def create_order():
    """Minimal endpoint to create a placeholder order for a customer.
    This lets the customer-detail page create a lightweight order and return to the detail view.
    """
    try:
        customer_id = request.form.get('customer_id')
        if not customer_id:
            flash('Kunde ist erforderlich')
            return redirect(request.referrer or url_for('customers'))

        # create a minimal order record
        order = Order(
            customer_id=int(customer_id),
            order_date=datetime.now(),
            status='Offen',
            total_amount=0.0
        )
        db.session.add(order)
        db.session.commit()
        flash('Neue Bestellung (Platzhalter) wurde erstellt')
    except Exception as e:
        db.session.rollback()
        flash(f'Fehler beim Erstellen der Bestellung: {e}')

    # redirect back to customer detail
    return redirect(request.referrer or url_for('customers'))

# Entfernte Routen: orders, order_items, products, users
# Die App fokussiert sich jetzt nur auf Kontakte und Kundenkonversationen

app.register_blueprint(customers_bp)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # erstellt Tabellen automatisch
        create_admin_user()  # erstelle Admin-User
        create_sample_data()  # erstelle Testdaten
    app.run(debug=True)
