import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app
from models import Customer, Order, Conversation, db
from flask import render_template
from sqlalchemy import func

with app.app_context():
    # pick first customer with id
    customer = Customer.query.order_by(Customer.id).first()
    if not customer:
        print('no customer')
        raise SystemExit(0)
    # replicate logic from customer_detail
    start = None
    end = None
    orders_query = Order.query.filter_by(customer_id=customer.id)
    recent_orders = orders_query.order_by(Order.order_date.desc()).limit(10).all()
    # totals
    total_revenue = float( (db.session.query(func.coalesce(func.sum(Order.total_amount), 0)).filter(Order.customer_id == customer.id).scalar()) ) if True else 0.0
    revenue_last_year = 0.0
    conversations_list = Conversation.query.filter_by(customer_id=customer.id).order_by(Conversation.conversation_time.desc()).limit(10).all()
    last_conversation = Conversation.query.filter_by(customer_id=customer.id).order_by(Conversation.conversation_time.desc()).first()
    # render template inside a request context so url_for() works
    with app.test_request_context(f'/customers/{customer.id}'):
        html = render_template('customer_detail.html',
                           customer=customer,
                           recent_orders=recent_orders,
                           conversations_list=conversations_list,
                           total_revenue=total_revenue,
                           revenue_last_year=revenue_last_year,
                           last_conversation=last_conversation,
                           start=start,
                           end=end)
    print('rendered length:', len(html))
