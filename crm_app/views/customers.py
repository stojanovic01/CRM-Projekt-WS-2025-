from flask import Blueprint, render_template, request, session, redirect, url_for
from datetime import datetime
from crm_app.models import db, Customer, Order

customers_bp = Blueprint('customers', __name__, url_prefix='/customers')

@customers_bp.route('/')
def list_customers():
    if db is None or Customer is None:
        return "Fehler: Datenbankmodelle nicht verfügbar", 500

    if 'user_id' not in session:
        return redirect(url_for('login.login'))

    try:
        search = request.args.get('search', '')

        if search:
            customers = Customer.query.filter(
                (Customer.first_name.ilike(f'%{search}%')) |
                (Customer.last_name.ilike(f'%{search}%')) |
                (Customer.email.ilike(f'%{search}%'))
            ).all()
        else:
            customers = Customer.query.all()

        return render_template('customers.html', customers=customers, search=search)
    except Exception as e:
        print(f"list_customers Fehler: {e}")
        return "Interner Fehler beim Laden der Kunden", 500

@customers_bp.route('/<int:customer_id>')
def customer_detail(customer_id):
    if db is None or Customer is None:
        return "Fehler: Datenbankmodelle nicht verfügbar", 500

    if 'user_id' not in session:
        return redirect(url_for('login.login'))

    try:
        customer = Customer.query.get_or_404(customer_id)
        orders = getattr(customer, 'orders', [])

        total_revenue = sum(float(order.total_amount) for order in orders)
        last_year_revenue = sum(
            float(order.total_amount) for order in orders
            if order.order_date.year == datetime.now().year - 1
        )

        last_orders = sorted(orders, key=lambda x: x.order_date, reverse=True)[:5]
        last_conversations = sorted(
            getattr(customer, 'conversations', []),
            key=lambda x: x.conversation_time,
            reverse=True
        )[:5]

        return render_template(
            'customer_detail.html',
            customer=customer,
            orders=orders,
            total_revenue=total_revenue,
            last_year_revenue=last_year_revenue,
            last_orders=last_orders,
            last_conversations=last_conversations
        )
    except Exception as e:
        print(f"customer_detail Fehler: {e}")
        return "Interner Fehler beim Laden des Kunden", 500

@customers_bp.route('/add', methods=['GET', 'POST'])
def add_customer():
    if db is None or Customer is None:
        return "Fehler: Datenbankmodelle nicht verfügbar", 500

    if 'user_id' not in session:
        return redirect(url_for('login.login'))

    try:
        if request.method == 'POST':
            customer = Customer(
                first_name=request.form.get('first_name'),
                last_name=request.form.get('last_name'),
                email=request.form.get('email'),
                phone=request.form.get('phone')
            )
            db.session.add(customer)
            db.session.commit()
            return redirect(url_for('customers.list_customers'))

        return render_template('customer_form.html')
    except Exception as e:
        print(f"add_customer Fehler: {e}")
        return "Interner Fehler beim Erstellen des Kunden", 500
