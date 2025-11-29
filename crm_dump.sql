-- CRM-Anwendung - Datenbank-Dump
-- Schema und Beispieldaten
-- Für Import auf PythonAnywhere MySQL

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";

-- ============================================================================
-- TABELLEN-STRUKTUR
-- ============================================================================

DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `name` varchar(100) NOT NULL,
  `email` varchar(255) UNIQUE,
  `password_hash` varchar(255),
  `role` enum('Schüler','Lehrer','Admin') DEFAULT 'Schüler',
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

DROP TABLE IF EXISTS `customers`;
CREATE TABLE `customers` (
  `id` int NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `first_name` varchar(100) NOT NULL,
  `last_name` varchar(100) NOT NULL,
  `email` varchar(255) UNIQUE,
  `phone` varchar(50),
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  UNIQUE KEY `email` (`email`),
  INDEX `idx_customers_name` (`first_name`, `last_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

DROP TABLE IF EXISTS `products`;
CREATE TABLE `products` (
  `id` int NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `sku` varchar(100) UNIQUE,
  `name` varchar(255) NOT NULL,
  `base_price` decimal(10, 2) NOT NULL,
  INDEX `idx_products_name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

DROP TABLE IF EXISTS `orders`;
CREATE TABLE `orders` (
  `id` int NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `customer_id` int NOT NULL,
  `order_date` datetime NOT NULL,
  `status` enum('Offen','Bezahlt','Storniert') NOT NULL DEFAULT 'Offen',
  `total_amount` decimal(10, 2) NOT NULL,
  KEY `fk_orders_customer` (`customer_id`),
  CONSTRAINT `fk_orders_customer` FOREIGN KEY (`customer_id`) REFERENCES `customers` (`id`) ON DELETE CASCADE,
  INDEX `idx_orders_date` (`order_date`),
  INDEX `idx_orders_customer_date` (`customer_id`, `order_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

DROP TABLE IF EXISTS `order_items`;
CREATE TABLE `order_items` (
  `id` int NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `order_id` int NOT NULL,
  `product_id` int NOT NULL,
  `quantity` int NOT NULL,
  `unit_price` decimal(10, 2) NOT NULL,
  KEY `fk_order_items_order` (`order_id`),
  KEY `fk_order_items_product` (`product_id`),
  CONSTRAINT `fk_order_items_order` FOREIGN KEY (`order_id`) REFERENCES `orders` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_order_items_product` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

DROP TABLE IF EXISTS `conversations`;
CREATE TABLE `conversations` (
  `id` int NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `customer_id` int NOT NULL,
  `user_id` int,
  `channel` enum('Telefon','E-Mail','Meeting','Chat') NOT NULL,
  `subject` varchar(255),
  `notes` text,
  `conversation_time` datetime NOT NULL,
  KEY `fk_conversations_customer` (`customer_id`),
  KEY `fk_conversations_user` (`user_id`),
  CONSTRAINT `fk_conversations_customer` FOREIGN KEY (`customer_id`) REFERENCES `customers` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_conversations_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE SET NULL,
  INDEX `idx_conversations_time` (`conversation_time`),
  INDEX `idx_conversations_customer_time` (`customer_id`, `conversation_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- BEISPIELDATEN
-- ============================================================================

-- Admin-Benutzer (Passwort: administrator)
INSERT INTO `users` (`name`, `email`, `password_hash`, `role`) VALUES
('administrator', 'admin@crm.local', '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918', 'Admin');

-- Beispiel-Produkte
INSERT INTO `products` (`sku`, `name`, `base_price`) VALUES
('SKU001', 'Laptop Pro', 1299.99),
('SKU002', 'USB-C Kabel', 29.99),
('SKU003', 'Monitor 27"', 399.99),
('SKU004', 'Wireless Mouse', 79.99),
('SKU005', 'Tastatur Mechanisch', 149.99);

-- Beispiel-Kunden
INSERT INTO `customers` (`first_name`, `last_name`, `email`, `phone`, `created_at`) VALUES
('Max', 'Mustermann', 'max.mustermann@example.com', '+43 699 1234567', '2025-01-15 10:30:00'),
('Anna', 'Beispiel', 'anna.beispiel@example.com', '+43 699 2345678', '2025-01-20 14:15:00'),
('Peter', 'Schmidt', 'peter.schmidt@example.com', '+43 699 3456789', '2025-02-05 09:45:00'),
('Sarah', 'Weber', 'sarah.weber@example.com', '+43 699 4567890', '2025-02-10 11:20:00'),
('Thomas', 'Fischer', 'thomas.fischer@example.com', '+43 699 5678901', '2025-02-15 13:00:00');

-- Beispiel-Bestellungen
INSERT INTO `orders` (`customer_id`, `order_date`, `status`, `total_amount`) VALUES
(1, '2025-03-01 10:00:00', 'Bezahlt', 1329.98),
(1, '2025-04-15 11:30:00', 'Offen', 449.98),
(2, '2025-03-10 09:00:00', 'Bezahlt', 1479.97),
(2, '2025-04-20 14:20:00', 'Bezahlt', 299.96),
(3, '2025-03-20 13:45:00', 'Offen', 1399.98),
(4, '2025-04-01 10:15:00', 'Bezahlt', 79.99),
(5, '2025-04-10 15:30:00', 'Bezahlt', 1429.97);

-- Bestellpositionen
INSERT INTO `order_items` (`order_id`, `product_id`, `quantity`, `unit_price`) VALUES
(1, 1, 1, 1299.99),
(1, 2, 1, 29.99),
(2, 3, 1, 399.99),
(2, 4, 1, 49.99),
(3, 1, 1, 1299.99),
(3, 2, 1, 29.99),
(3, 5, 1, 149.99),
(4, 4, 1, 79.99),
(4, 2, 1, 29.99),
(4, 2, 1, 29.99),
(5, 1, 1, 1299.99),
(5, 4, 1, 99.99),
(6, 4, 1, 79.99),
(7, 1, 1, 1299.99),
(7, 2, 1, 29.99),
(7, 5, 1, 99.99);

-- Beispiel-Gespräche
INSERT INTO `conversations` (`customer_id`, `user_id`, `channel`, `subject`, `notes`, `conversation_time`) VALUES
(1, 1, 'Telefon', 'Produkt-Anfrage', 'Kunde interessiert sich für Laptops und Zubehör', '2025-03-01 09:30:00'),
(1, 1, 'E-Mail', 'Rechnung-Frage', 'Frage zur Rechnungsnummer', '2025-03-05 14:00:00'),
(2, 1, 'Meeting', 'Großbestellung', 'Diskussion über Mengenrabatt', '2025-03-09 10:00:00'),
(2, 1, 'Chat', 'Versand-Status', 'Kunde verfolgt Bestellstatus', '2025-03-11 16:45:00'),
(3, 1, 'Telefon', 'Technischer Support', 'Hilfe bei der Konfiguration', '2025-03-19 11:00:00'),
(3, 1, 'E-Mail', 'Follow-up', 'Bestätigung der Lösung', '2025-03-22 09:15:00'),
(4, 1, 'Meeting', 'Jahresplanung', 'Planung für nächstes Geschäftsjahr', '2025-04-01 13:00:00'),
(5, 1, 'Telefon', 'Neue Anfrage', 'Kunde möchte Angebot', '2025-04-09 10:30:00');

COMMIT;
