from extensions import db  # Importiert die globale Instanz
from datetime import datetime
from sqlalchemy import Index, ForeignKey, Numeric, DateTime, Integer, String, Text, Enum as SAEnum

# ============================================
# 1. USER MODEL
# ============================================
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(Integer, primary_key=True, autoincrement=True)
    name = db.Column(String(100), nullable=False)
    email = db.Column(String(255), unique=True)
    password_hash = db.Column(String(255))  # Einfaches Klartextpasswort
    role = db.Column(SAEnum('Schüler', 'Lehrer', 'Admin', name='role_enum'), default='Schüler')
    
    conversations = db.relationship("Conversation", back_populates="user")

    def __repr__(self):
        return f'<User {self.name}>'
    
# ============================================
# 2. CUSTOMER MODEL
# ============================================
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

    __table_args__ = (
        Index('idx_customers_name', 'first_name', 'last_name'),
    )

    def __repr__(self):
        return f'<Customer {self.first_name} {self.last_name}>'


# ============================================
# 3. PRODUCT MODEL
# ============================================
class Product(db.Model):
    __tablename__ = "products"
    id = db.Column(Integer, primary_key=True, autoincrement=True)
    sku = db.Column(String(100), unique=True)
    name = db.Column(String(255), nullable=False)
    base_price = db.Column(Numeric(10, 2), nullable=False)

    order_items = db.relationship("OrderItem", back_populates="product")

    def __repr__(self):
        return f'<Product {self.name}>'


# ============================================
# 4. ORDER MODEL
# ============================================
class Order(db.Model):
    __tablename__ = "orders"
    id = db.Column(Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(Integer, ForeignKey("customers.id", ondelete="CASCADE"), nullable=False)
    order_date = db.Column(DateTime, nullable=False)
    status = db.Column(SAEnum('Offen', 'Bezahlt', 'Storniert', name='status_enum'), default='Offen', nullable=False)
    total_amount = db.Column(Numeric(10, 2), nullable=False)

    customer = db.relationship("Customer", back_populates="orders")
    items = db.relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")

    __table_args__ = (
        Index('idx_orders_date', 'order_date'),
        Index('idx_orders_customer_date', 'customer_id', 'order_date'),
    )

    def __repr__(self):
        return f'<Order {self.id}>'


# ============================================
# 5. ORDER_ITEM MODEL
# ============================================
class OrderItem(db.Model):
    __tablename__ = "order_items"
    id = db.Column(Integer, primary_key=True, autoincrement=True)
    order_id = db.Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    product_id = db.Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = db.Column(Integer, nullable=False)
    unit_price = db.Column(Numeric(10, 2), nullable=False)

    order = db.relationship("Order", back_populates="items")
    product = db.relationship("Product", back_populates="order_items")

    def __repr__(self):
        return f'<OrderItem {self.id}>'


# ============================================
# 6. CONVERSATION MODEL
# ============================================
class Conversation(db.Model):
    __tablename__ = "conversations"
    id = db.Column(Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(Integer, ForeignKey("customers.id", ondelete="CASCADE"), nullable=False)
    user_id = db.Column(Integer, ForeignKey("users.id"))
    channel = db.Column(SAEnum('Telefon', 'E-Mail', 'Meeting', 'Chat', name='channel_enum'), nullable=False)
    subject = db.Column(String(255))
    notes = db.Column(Text)
    conversation_time = db.Column(DateTime, nullable=False)

    customer = db.relationship("Customer", back_populates="conversations")
    user = db.relationship("User", back_populates="conversations")

    __table_args__ = (
        Index('idx_conversations_time', 'conversation_time'),
        Index('idx_conversations_customer_time', 'customer_id', 'conversation_time'),
    )

    def __repr__(self):
        return f'<Conversation {self.id}>'