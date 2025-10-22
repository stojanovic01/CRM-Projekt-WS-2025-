from flask import Blueprint, render_template
from models import Customer, Order, Contact, Product, OrderItem

customers_bp = Blueprint('customers', __name__) 

@customers_bp.route('/customers')
def list_customers():
    customers = Customer.query.all()
    return render_template('customers.html', customers=customers)

# @customers_bp.route('/customers/<int:customer_id>')
# def detail(customer_id):
#     customer = Customer.query.get_or_404(customer_id)
#     orders = Order.query.filter_by(customer_id=customer_id).all()
#     contacts = Contact.query.filter_by(customer_id=customer_id).all()
#     total_revenue = sum(o.amount for o in orders)
#     return render_template('customer_detail.html', customer=customer, orders=orders, contacts=contacts, total=total_revenue)
