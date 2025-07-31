/* Dataset Schema:
customers (customer_id, name, email, created_at)
orders (order_id, customer_id, total_amount, order_date)
order_items (order_item_id, order_id, product_id, quantity, price)
products (product_id, name, category, price)
*/

-- database created
CREATE DATABASE ECommerce;

-- use database
use Ecommerce;

-- create tables
CREATE TABLE CUSTOMERS (
	customer_id int primary key auto_increment,
    customer_name varchar(200),
    email varchar(200),
    created_at timestamp
);

CREATE TABLE ORDERS (
	order_id int primary key auto_increment,
    customer_id int,
    total_amount decimal(10,2),
    order_date date,
    foreign key (customer_id) references customers (customer_id)
);

CREATE TABLE PRODUCTS (
	product_id int primary key auto_increment,
    product_name varchar(200),
    category varchar(200),
    price decimal(10,2)
);

CREATE TABLE ORDER_ITEMS (
	order_item_id int primary key auto_increment,
    order_id int,
    product_id int,
    quantity int,
    price decimal(10,2),
    
    foreign key (order_id) references orders (order_id),
    foreign key (product_id) references products (product_id)
);

CREATE TABLE SITE_VISITS (
	visit_id int primary key auto_increment,
    customer_id int,
    visited_at date,
    visit_source varchar(100),
    foreign key (customer_id) references customers (customer_id)
);

-- show all tables 
show tables;

-- insert data
INSERT INTO CUSTOMERS (customer_name, email, created_at) VALUES
('Riya Sharma', 'riya.sharma@example.com', '2024-11-25 10:15:00'),
('Amit Verma', 'amit.verma@example.com', '2024-12-10 09:40:00'),
('Neha Singh', 'neha.singh@example.com', '2025-01-05 12:30:00'),
('Vikram Mehta', 'vikram.mehta@example.com', '2025-01-18 14:05:00'),
('Tanya Roy', 'tanya.roy@example.com', '2025-01-20 11:22:00'),
('Rohan Desai', 'rohan.desai@example.com', '2025-02-01 15:45:00'),
('Sneha Patel', 'sneha.patel@example.com', '2025-02-10 16:30:00'),
('Anil Kapoor', 'anil.kapoor@example.com', '2025-02-12 10:10:00'),
('Meera Nair', 'meera.nair@example.com', '2025-02-14 13:00:00'),
('Manish Agarwal', 'manish.agarwal@example.com', '2025-02-15 14:30:00'),
('Divya Joshi', 'divya.joshi@example.com', '2025-02-20 17:00:00'),
('Karan Malhotra', 'karan.malhotra@example.com', '2025-02-25 08:45:00'),
('Alok Reddy', 'alok.reddy@example.com', '2025-03-01 09:15:00'),
('Priya Menon', 'priya.menon@example.com', '2025-03-05 11:40:00'),
('Sunil Chauhan', 'sunil.chauhan@example.com', '2025-03-15 12:50:00');
SELECT * FROM CUSTOMERS;

INSERT INTO PRODUCTS (product_name, category, price) VALUES
('Wireless Mouse', 'Electronics', 799.00),
('Bluetooth Headphones', 'Electronics', 1999.00),
('T-shirt - Black', 'Apparel', 499.00),
('Jeans - Blue', 'Apparel', 1299.00),
('Yoga Mat', 'Fitness', 899.00),
('Dumbbells (2kg)', 'Fitness', 699.00),
('LED Desk Lamp', 'Home & Living', 999.00),
('Water Bottle - 1L', 'Home & Living', 299.00),
('Sneakers - White', 'Footwear', 1999.00),
('Running Shoes', 'Footwear', 2499.00);
SELECT * FROM PRODUCTS;

INSERT INTO ORDERS (customer_id, total_amount, order_date) VALUES
(1, 2798.00, '2025-03-20'),
(2, 1798.00, '2025-03-19'),
(3, 3298.00, '2025-03-18'),
(4, 2499.00, '2025-03-17'),
(5, 899.00, '2025-03-15'),
(6, 2298.00, '2025-03-14'),
(7, 699.00, '2025-03-14'),
(8, 499.00, '2025-03-13'),
(9, 2998.00, '2025-03-13'),
(10, 1999.00, '2025-03-12'),
(11, 3298.00, '2025-03-10'),
(12, 2798.00, '2025-03-09'),
(13, 899.00, '2025-03-08'),
(14, 499.00, '2025-03-07'),
(15, 999.00, '2025-03-06');
SELECT * FROM ORDERS;

INSERT INTO ORDER_ITEMS (order_id, product_id, quantity, price) VALUES
(1, 1, 1, 799.00),
(1, 2, 1, 1999.00),
(2, 3, 2, 499.00),
(2, 4, 1, 1299.00),
(3, 10, 1, 2499.00),
(3, 8, 1, 299.00),
(3, 6, 1, 499.00),
(4, 9, 1, 1999.00),
(4, 1, 1, 499.00),
(5, 5, 1, 899.00),
(6, 2, 1, 1999.00),
(6, 1, 1, 299.00),
(7, 6, 1, 699.00),
(8, 3, 1, 499.00),
(9, 4, 2, 1299.00),
(9, 8, 1, 399.00),
(10, 10, 1, 1999.00),
(11, 7, 2, 999.00),
(11, 1, 1, 799.00),
(12, 2, 1, 1999.00),
(12, 8, 1, 299.00),
(13, 5, 1, 899.00),
(14, 3, 1, 499.00),
(15, 7, 1, 999.00);
SELECT * FROM ORDER_ITEMS;

INSERT INTO site_visits (visit_id, customer_id, visited_at, visit_source) VALUES
(1, 1, '2025-03-20', 'Google Ads'),
(2, NULL, '2025-03-20', 'Organic'),
(3, 2, '2025-03-19', 'Email Campaign'),
(4, NULL, '2025-03-19', 'Facebook Ads'),
(5, 3, '2025-03-18', 'Referral'),
(6, 4, '2025-03-17', 'Direct'),
(7, NULL, '2025-03-17', 'Google Ads'),
(8, 5, '2025-03-15', 'Email Campaign'),
(9, NULL, '2025-03-14', 'Organic'),
(10, 6, '2025-03-14', 'Referral'),
(11, 7, '2025-03-14', 'Organic'),
(12, 8, '2025-03-13', 'Direct'),
(13, 9, '2025-03-13', 'Google Ads'),
(14, 10, '2025-03-12', 'Email Campaign'),
(15, 11, '2025-03-10', 'Referral'),
(16, 12, '2025-03-09', 'Organic'),
(17, 13, '2025-03-08', 'Facebook Ads'),
(18, 14, '2025-03-07', 'Direct'),
(19, 15, '2025-03-06', 'Google Ads'),
(20, NULL, '2025-03-06', 'Organic');
SELECT * FROM site_visits;

