from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Index, ForeignKey, Numeric, DateTime, Integer, String, Text
from sqlalchemy import Enum as SAEnum  # wichtig: kein MySQL-ENUM

db = SQLAlchemy()

class Customer(db.Model):
    __tablename__ = "customers"
    id = db.Column(Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(String(100), nullable=False)
    last_name = db.Column(String(100), nullable=False)
    email = db.Column(String(255), unique=True)
    phone = db.Column(String(50))
    created_at = db.Column(DateTime, default=datetime.utcnow, nullable=False)

    orders = db.relationship("Order", back_populates="customer", cascade="all, delete-orphan")
    conversations = db.relationship("Conversation", back_populates="customer", cascade="all, delete-orphan")

class Order(db.Model):
    __tablename__ = "orders"
    id = db.Column(Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(Integer, ForeignKey("customers.id", ondelete="CASCADE"), nullable=False)
    order_date = db.Column(DateTime, nullable=False)
    status = db.Column(
        SAEnum("Offen", "Bezahlt", "Storniert", name="order_status", native_enum=False, create_constraint=True, validate_strings=True),
        nullable=False,
        default="Offen",
    )
    total_amount = db.Column(Numeric(10, 2), nullable=False)

    customer = db.relationship("Customer", back_populates="orders")
    items = db.relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")

    __table_args__ = (
        Index("idx_orders_date", "order_date"),
        Index("idx_orders_customer_date", "customer_id", "order_date"),
    )

class OrderItem(db.Model):
    __tablename__ = "order_items"
    id = db.Column(Integer, primary_key=True, autoincrement=True)
    order_id = db.Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    product_id = db.Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = db.Column(Integer, nullable=False)
    unit_price = db.Column(Numeric(10, 2), nullable=False)

    order = db.relationship("Order", back_populates="items")
    product = db.relationship("Product", back_populates="items")

class Product(db.Model):
    __tablename__ = "products"
    id = db.Column(Integer, primary_key=True, autoincrement=True)
    sku = db.Column(String(100), unique=True)
    name = db.Column(String(255), nullable=False)
    base_price = db.Column(Numeric(10, 2), nullable=False)

    items = db.relationship("OrderItem", back_populates="product")

class Conversation(db.Model):
    __tablename__ = "conversations"
    id = db.Column(Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(Integer, ForeignKey("customers.id", ondelete="CASCADE"), nullable=False)
    user_id = db.Column(Integer, ForeignKey("users.id"))
    channel = db.Column(
        SAEnum("Telefon", "E-Mail", "Meeting", "Chat", name="conversation_channel", native_enum=False, create_constraint=True, validate_strings=True),
        nullable=False,
    )
    subject = db.Column(String(255))
    notes = db.Column(Text)
    conversation_time = db.Column(DateTime, nullable=False)

    customer = db.relationship("Customer", back_populates="conversations")
    user = db.relationship("User", back_populates="conversations")

    __table_args__ = (
        Index("idx_conversations_time", "conversation_time"),
        Index("idx_conversations_customer_time", "customer_id", "conversation_time"),
    )

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(Integer, primary_key=True, autoincrement=True)
    name = db.Column(String(100), nullable=False)
    email = db.Column(String(255), unique=True)
    password_hash = db.Column(String(255))
    role = db.Column(
        SAEnum("Schüler", "Lehrer", "Admin", name="user_role", native_enum=False, create_constraint=True, validate_strings=True),
        nullable=True,
        default="Schüler",
    )

    conversations = db.relationship("Conversation", back_populates="user")