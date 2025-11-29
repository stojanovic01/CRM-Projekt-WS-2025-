from flask import Blueprint, render_template, request, session, redirect, url_for
from crm_app.models import db, Order, Customer
from datetime import datetime

orders_bp = Blueprint('orders', __name__, url_prefix='/orders')

@orders_bp.route('/')
def list_orders():
    if 'user_id' not in session:
        return redirect(url_for('login.login'))
    
    # Filter nach Status
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

@orders_bp.route('/<int:order_id>')
def order_detail(order_id):
    if 'user_id' not in session:
        return redirect(url_for('login.login'))
    
    order = Order.query.get_or_404(order_id)
    
    return render_template('order_detail.html', order=order)

@orders_bp.route('/add', methods=['GET', 'POST'])
def add_order():
    if 'user_id' not in session:
        return redirect(url_for('login.login'))
    
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