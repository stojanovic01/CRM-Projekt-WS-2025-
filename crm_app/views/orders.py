from flask import Blueprint, render_template, request, session, redirect, url_for
from datetime import datetime
from crm_app.models import db, Order

# Versuch, Modelle aus verschiedenen Pfaden zu importieren
try:
    from crm_app.models import db, Order, Customer
except ModuleNotFoundError:
    try:
        from ..models import db, Order, Customer
    except ModuleNotFoundError:
        try:
            from models import db, Order, Customer
        except ModuleNotFoundError:
            db = None
            Order = None
            Customer = None
            print("Warning: models konnten nicht importiert werden! Orders werden nicht funktionieren.")

orders_bp = Blueprint('orders', __name__, url_prefix='/orders')

@orders_bp.route('/')
def list_orders():
    if db is None or Order is None:
        return "Fehler: Datenbankmodelle nicht verfügbar", 500

    if 'user_id' not in session:
        return redirect(url_for('login.login'))

    try:
        status = request.args.get('status', '')
        date_from = request.args.get('date_from', '')
        date_to = request.args.get('date_to', '')

        query = Order.query

        if status:
            query = query.filter_by(status=status)

        if date_from:
            query = query.filter(Order.order_date >= datetime.fromisoformat(date_from))

        if date_to:
            query = query.filter(Order.order_date <= datetime.fromisoformat(date_to))

        orders = query.order_by(Order.order_date.desc()).all()

        return render_template(
            'orders.html',
            orders=orders,
            status=status,
            date_from=date_from,
            date_to=date_to
        )
    except Exception as e:
        print(f"list_orders Fehler: {e}")
        return "Interner Fehler beim Laden der Bestellungen", 500

@orders_bp.route('/<int:order_id>')
def order_detail(order_id):
    if db is None or Order is None:
        return "Fehler: Datenbankmodelle nicht verfügbar", 500

    if 'user_id' not in session:
        return redirect(url_for('login.login'))

    try:
        order = Order.query.get_or_404(order_id)
        return render_template('order_detail.html', order=order)
    except Exception as e:
        print(f"order_detail Fehler: {e}")
        return "Interner Fehler beim Laden der Bestellung", 500

@orders_bp.route('/add', methods=['GET', 'POST'])
def add_order():
    if db is None or Order is None or Customer is None:
        return "Fehler: Datenbankmodelle nicht verfügbar", 500

    if 'user_id' not in session:
        return redirect(url_for('login.login'))

    try:
        if request.method == 'POST':
            order = Order(
                customer_id=request.form.get('customer_id'),
                order_date=datetime.fromisoformat(request.form.get('order_date')),
                status=request.form.get('status', 'Offen'),
                total_amount=request.form.get('total_amount')
            )
            db.session.add(order)
            db.session.commit()
            return redirect(url_for('orders.list_orders'))

        customers = Customer.query.all()
        return render_template('order_form.html', customers=customers)
    except Exception as e:
        print(f"add_order Fehler: {e}")
        return "Interner Fehler beim Erstellen der Bestellung", 500
