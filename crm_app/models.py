from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    email = db.Column(db.String(120))
    city = db.Column(db.String(50))

    orders = db.relationship('Order', backref='customer', lazy=True)
    contacts = db.relationship('Contact', backref='customer', lazy=True)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    date = db.Column(db.Date)
    amount = db.Column(db.Float)

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    date = db.Column(db.Date)
    type = db.Column(db.String(50))  # z.B. Email, Anruf, Meeting
    notes = db.Column(db.Text)
