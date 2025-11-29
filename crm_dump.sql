BEGIN TRANSACTION;
CREATE TABLE alembic_version (
	version_num VARCHAR(32) NOT NULL, 
	CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);
INSERT INTO "alembic_version" VALUES('2a9991bb71ef');
CREATE TABLE conversations (
	id INTEGER NOT NULL, 
	customer_id INTEGER NOT NULL, 
	user_id INTEGER, 
	channel VARCHAR(7) NOT NULL, 
	subject VARCHAR(255), 
	notes TEXT, 
	conversation_time DATETIME NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(customer_id) REFERENCES customers (id) ON DELETE CASCADE, 
	FOREIGN KEY(user_id) REFERENCES users (id), 
	CONSTRAINT conversation_channel CHECK (channel IN ('Telefon', 'E-Mail', 'Meeting', 'Chat'))
);
INSERT INTO "conversations" VALUES(1,1,2,'Telefon','Rechnungsanfrage','Kunde fragt nach Rechnung','2024-12-14 18:23:20.884682');
INSERT INTO "conversations" VALUES(2,2,1,'E-Mail','Lieferverzögerung','Kundenbeschwerde','2025-06-07 18:23:20.884682');
INSERT INTO "conversations" VALUES(3,3,2,'Meeting','Anforderungsanalyse','Besuch beim Kunden','2025-10-30 18:23:20.884682');
INSERT INTO "conversations" VALUES(4,4,3,'Chat','Technischer Support','Fragen zum Produkt','2025-11-27 18:23:20.884682');
INSERT INTO "conversations" VALUES(5,5,1,'E-Mail','Danksagung','Kunde bedankt sich','2025-11-29 18:23:20.884682');
CREATE TABLE customers (
	id INTEGER NOT NULL, 
	first_name VARCHAR(100) NOT NULL, 
	last_name VARCHAR(100) NOT NULL, 
	email VARCHAR(255), 
	phone VARCHAR(50), 
	created_at DATETIME NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (email)
);
INSERT INTO "customers" VALUES(1,'Max','Mustermann','max@example.com','+43 1 234 5678','2025-11-29 18:23:20.878923');
INSERT INTO "customers" VALUES(2,'Anna','Schmidt','anna@example.com','+43 2 345 6789','2025-11-29 18:23:20.878923');
INSERT INTO "customers" VALUES(3,'Peter','Wagner','peter@example.com','+43 3 456 7890','2025-11-29 18:23:20.878923');
INSERT INTO "customers" VALUES(4,'Sandra','Hofmann','sandra@example.com','+43 4 567 8901','2025-11-29 18:23:20.878923');
INSERT INTO "customers" VALUES(5,'Thomas','Brunner','thomas@example.com','+43 5 678 9012','2025-11-29 18:23:20.878923');
CREATE TABLE order_items (
	id INTEGER NOT NULL, 
	order_id INTEGER NOT NULL, 
	product_id INTEGER NOT NULL, 
	quantity INTEGER NOT NULL, 
	unit_price NUMERIC(10, 2) NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(order_id) REFERENCES orders (id) ON DELETE CASCADE, 
	FOREIGN KEY(product_id) REFERENCES products (id)
);
INSERT INTO "order_items" VALUES(1,1,1,1,899.99);
INSERT INTO "order_items" VALUES(2,1,2,1,349.99);
INSERT INTO "order_items" VALUES(3,2,2,1,349.99);
INSERT INTO "order_items" VALUES(4,2,5,1,19.99);
INSERT INTO "order_items" VALUES(5,3,1,1,899.99);
INSERT INTO "order_items" VALUES(6,3,4,1,49.99);
INSERT INTO "order_items" VALUES(7,4,1,1,899.99);
INSERT INTO "order_items" VALUES(8,4,2,1,349.99);
INSERT INTO "order_items" VALUES(9,4,3,1,79.99);
INSERT INTO "order_items" VALUES(10,5,3,2,79.99);
INSERT INTO "order_items" VALUES(11,5,4,1,49.99);
INSERT INTO "order_items" VALUES(12,6,1,2,899.99);
INSERT INTO "order_items" VALUES(13,6,5,1,19.99);
INSERT INTO "order_items" VALUES(14,7,5,5,19.99);
CREATE TABLE orders (
	id INTEGER NOT NULL, 
	customer_id INTEGER NOT NULL, 
	order_date DATETIME NOT NULL, 
	status VARCHAR(9) NOT NULL, 
	total_amount NUMERIC(10, 2) NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(customer_id) REFERENCES customers (id) ON DELETE CASCADE, 
	CONSTRAINT order_status CHECK (status IN ('Offen', 'Bezahlt', 'Storniert'))
);
INSERT INTO "orders" VALUES(1,1,'2024-10-30 18:23:20.884682','Bezahlt',1249.98);
INSERT INTO "orders" VALUES(2,2,'2024-12-09 18:23:20.884682','Bezahlt',429.98);
INSERT INTO "orders" VALUES(3,1,'2025-01-28 18:23:20.884682','Bezahlt',949.98);
INSERT INTO "orders" VALUES(4,3,'2025-06-02 18:23:20.884682','Bezahlt',1349.97);
INSERT INTO "orders" VALUES(5,4,'2025-10-30 18:23:20.884682','Offen',499.98);
INSERT INTO "orders" VALUES(6,5,'2025-11-24 18:23:20.884682','Bezahlt',2249.95);
INSERT INTO "orders" VALUES(7,2,'2025-11-29 18:23:20.884682','Offen',129.98);
CREATE TABLE products (
	id INTEGER NOT NULL, 
	sku VARCHAR(100), 
	name VARCHAR(255) NOT NULL, 
	base_price NUMERIC(10, 2) NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (sku)
);
INSERT INTO "products" VALUES(1,'PROD-001','Laptop',899.99);
INSERT INTO "products" VALUES(2,'PROD-002','Monitor 27"',349.99);
INSERT INTO "products" VALUES(3,'PROD-003','Tastatur',79.99);
INSERT INTO "products" VALUES(4,'PROD-004','Maus',49.99);
INSERT INTO "products" VALUES(5,'PROD-005','USB-C Kabel',19.99);
CREATE TABLE users (
	id INTEGER NOT NULL, 
	name VARCHAR(100) NOT NULL, 
	email VARCHAR(255), 
	password_hash VARCHAR(255), 
	role VARCHAR(7), 
	PRIMARY KEY (id), 
	UNIQUE (email), 
	CONSTRAINT user_role CHECK (role IN ('Schüler', 'Lehrer', 'Admin'))
);
INSERT INTO "users" VALUES(1,'Admin Benutzer','admin@crm.local','hashed','Admin');
INSERT INTO "users" VALUES(2,'Lehrer Test','teacher@school.local','hashed','Lehrer');
INSERT INTO "users" VALUES(3,'Schüler Test','student@school.local','hashed','Schüler');
CREATE INDEX idx_conversations_customer_time ON conversations (customer_id, conversation_time);
CREATE INDEX idx_conversations_time ON conversations (conversation_time);
CREATE INDEX idx_orders_customer_date ON orders (customer_id, order_date);
CREATE INDEX idx_orders_date ON orders (order_date);
COMMIT;
