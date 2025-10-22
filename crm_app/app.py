# app.py
from flask import Flask, render_template
from models import db
from views.customers import customers_bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///crm.db'
db.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/customers')
def customers():
    return render_template('customers.html')

@app.route('/contacts')
def contacts():
    return render_template('contacts.html')

@app.route('/orders')
def orders():
    return render_template('orders.html')

@app.route('/order_items')
def order_items():
    return render_template('order_items.html')

@app.route('/products')
def products():
    return render_template('products.html')

@app.route('/users')
def users():
    return render_template('users.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # erstellt Tabellen automatisch
    app.run(debug=True)

app.register_blueprint(customers_bp)
