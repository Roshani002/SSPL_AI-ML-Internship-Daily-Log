/*
Objective:
 Use an e-commerce database schema to generate business insights with SQL queries.
Dataset Schema:
customers (customer_id, name, email, created_at)
orders (order_id, customer_id, total_amount, order_date)
order_items (order_item_id, order_id, product_id, quantity, price)
products (product_id, name, category, price)

Tasks:
1. List the top 10 customers by total spend.
2. Generate a report of daily revenue and order count for the last 30 days.
3. Identify most sold products in the last 3 weeks.
4. Calculate the conversion rate (orders/site visits) if given a site_visits table.
5. Show total revenue broken down by product category.
*/
use Ecommerce;
show tables;

SELECT * FROM CUSTOMERS;
SELECT * FROM ORDERS;
SELECT * FROM PRODUCTS;
SELECT * FROM ORDER_ITEMS;
SELECT * FROM SITE_VISITS;

-- 1.list top 10 customres by total spend
SELECT c.customer_id, c.customer_name, o.order_id, max(o.total_amount) as max_total_spend, dense_rank() over(order by total_amount desc) as dense_rank_number
FROM CUSTOMERS AS c
INNER JOIN ORDERS AS o
ON c.customer_id = o.customer_id
group by order_id
limit 10;

-- 2. Generate a report of daily revenue and order count for the last 30 days.
select count(order_id) as total_order_per_day, sum(total_amount) as revenue, order_date 
from orders 
where order_date > date_sub(curdate(), interval 90 day)
group by order_date
order by order_date;

-- 3. Identify most sold products in the last 3 weeks.
SELECT 
    p.product_id,
    p.product_name,
    SUM(oi.quantity) AS total_quantity_sold
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
JOIN products p ON oi.product_id = p.product_id
WHERE o.order_date BETWEEN '2025-03-13' AND '2025-03-19'
GROUP BY p.product_id, p.product_name
ORDER BY total_quantity_sold DESC;

-- 4.Calculate the conversion rate (orders/site visits) if given a site_visits table.
SELECT count(distinct o.order_id)*1 / count(distinct sv.visit_id) as conversation_rate
from site_visits as sv
left join orders as o
on o.customer_id = sv.customer_id and o.order_Date = sv.visited_at;

-- 5. Show total revenue broken down by product category.
select count(oi.order_id) as no_of_orders, sum(oi.quantity*oi.price) as revenue, p.category
from order_items as oi
inner join products as p
on oi.product_id = p.product_id
group by p.category
order by p.category;





