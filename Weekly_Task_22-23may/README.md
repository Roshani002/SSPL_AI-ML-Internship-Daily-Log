# TASKS
## 🔶 Python Task: Data Pipeline Development
Build a Python module that fetches data from a public API, processes it (cleaning, normalizing and filtering), and stores results in a CSV/JSON and a local SQLite DB using SQLAlchemy. Includes logging, error handling, and modular code.

## 🔷 SQL Task: E-Commerce Reporting Dashboard
Write SQL queries on an e-commerce schema to generate insights.
1. List the top 10 customers by total spend.
2. Generate a report of daily revenue and order count for the last 30 days.
3. Identify most sold products in the last 3 months.
4. Calculate the conversion rate (orders/site visits) if given a site_visits table.
5. Show total revenue broken down by product category.


## 🔶 Python Task: Mini Data Ingestion Pipeline (News API)

- Ingested articles from BBC News using `requests`
- Cleaned and normalized data using custom transformation logic
- Validated and structured with SQLAlchemy ORM
- Stored output to `news.db` SQLite DB and `news` table
- Modular code using functions and OOP in `main_pipeline.py`

## 🔷 SQL Task: E-Commerce BI Queries

- Designed MySQL schema (customers, orders, products, etc.)
- Wrote SQL queries to extract:
  - Top customers by spend
  - Daily revenue and order count
  - Most sold products in last 3 weeks
  - Conversion rate from site visits
  - Revenue by product category

---

## Project Structure

```
Data Pipeline Development/
├── main_pipeline.py
├── fetch_transform_data.py
├── load_data.py
├── news_table.py
├── database/
│   └── news.db

E-Commerce_Reporting_Dashboard_SQL
├── task_sql_queries.sql
├── e-commerce_database.sql

```

