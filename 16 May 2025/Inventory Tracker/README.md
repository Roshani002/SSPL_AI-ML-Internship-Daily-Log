# Task 2: Inventory Tracker
- Create classes for products and warehouses; use a database to store inventory data; implement CRUD operations via Python.

## Features

- **Product Management:** Add, list, and delete products.
- **Warehouse Management:** Define warehouses with locations, capacities, and contact details.
- **Inventory Control:** Maintain stock levels across warehouses, update quantities, and view current inventory.
- **Transaction Logging:** Record stock movements (in and out) with timestamps and review your history.

## How to run
1. **Create Virtual environment**
   
2. **Inspect the database and Run main file**
   - The SQLite database file `inventory_tracker.db` will be created in the project root.
   - If you'd like to start fresh, delete `inventory_tracker.db` and rerun `main.py`.

## Project Structure

```
Inventory_Tracker_/
├── main.py
├── schema.sql
├── inventory_tracker.db
├── models/
│   ├── inventory.py
│   ├── products.py
│   ├── transcations.py
│   └── warehouses.py
└── operations/
    ├── inventory_op.py
    ├── product_op.py
    ├── transcation_op.py
    └── warehouse_op.py
```

