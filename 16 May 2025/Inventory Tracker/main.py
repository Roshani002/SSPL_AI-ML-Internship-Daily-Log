import sqlite3
from datetime import datetime, timedelta
from models.products import Product
from models.warehouses import Warehouse
from models.inventory import Inventory
from models.transcations import Transcation
from operations.product_op import product_operations
from operations.warehouse_op import warehouse_operations
from operations.inventory_op import inventory_operations
from operations.transcation_op import transcation_operations

def initialize_database():
    try:
        conn = sqlite3.connect("inventory_tracker.db")
        cur = conn.cursor()

        sql_script = None
        with open ('schema.sql', 'r') as file:
            sql_script = file.read()

        statements = sql_script.strip().split(";")

        for stmt in statements:
            if stmt.strip():
                cur.execute(stmt)

        conn.commit()
        conn.close()
        print("Database initialized successfully")
    except Exception as e:
        print(f"Error initializing database: {e}")

def add_sample_data():

    # Registering Students
    product_ope = product_operations()
    warehouse_ope = warehouse_operations()
    transcations_ope = transcation_operations()
    inventory_ope = inventory_operations()

    # add products
    products = [
        Product("DeskChair", 10000.00, "OfficeFurniture"),
        Product("Laptop", 65000.00, "Electronics"),
        Product("Washing Machine", 30000.00, "Electronics")
    ]
    
    def add_product():
        print("\nProducts added:")
        for product in products:
            product_ope.add_product(product)

    def get_product():
        # get product by id
        print("\nProduct with ID 2 is:")
        print(product_ope.get_product_by_id(2))
    
    def display_products():
        # display all products
        all_products = product_ope.get_all_products()
        print("\nDisplaying all Products...")
        for product in all_products:
            print(product)

    def update_product():
        # update product
        update_pro = Product("DeskChair", 15000.00, "OfficeFurniture")
        product_ope.update_product(update_pro,1)

    add_product()
    get_product()
    update_product()
    display_products()


    # WAREHOUSE
    # Add warehouses
    warehouses = [
        Warehouse("Anjani", "Ahmedabad", "500 sq ft", 9988776655),
        Warehouse("Supriya", "Kutch", "2000 sq ft", 1122334455),
        Warehouse("Karnvir", "Mumbai", "3000 sq ft", 1234567890)
    ]
    
    def add_warehouse():
        print("\nWarehouses added:")
        for warehouse in warehouses:
            warehouse_ope.add_warehouse(warehouse)

    def get_warehouse():
        # get product by id
        print("\nWarehouse with ID 3 is:")
        print(warehouse_ope.get_warehouse_by_id(3))
    
    def display_warehouses():
        # display all products
        all_warehouses = warehouse_ope.get_all_warehouses()
        print("\nDisplaying all Warehouses...")
        for warehouse in all_warehouses:
            print(warehouse)

    def update_warehouse():
        # update product
        update_war = Warehouse("Anjani", "Ahmedabad", "1000 sq ft", 9988776655)
        warehouse_ope.update_warehouse(update_war,1)

    add_warehouse()
    get_warehouse()
    display_warehouses()
    update_warehouse()

    # TRANSCATION and INVENTORY
    transcations = [
        Transcation(1, 1, 100, "purchase", "2025-05-22"),
        Transcation(1, 1, 10, "sale", "2025-05-22"),
    ]
    
    def add_transcation():
        for transcation in transcations:
            transcations_ope.add_transcation(transcation)
    
    def getall_inventoy_transcation():
        items = inventory_ope.get_all_inventorys()
        print("\nDisplaying all Inventory:")
        for item in items:
            print(item)

        transcations = transcations_ope.get_all_transcations()
        print("\nDisplaying All Transcations")
        for transcation in transcations:
            print(transcation)

    add_transcation()
    getall_inventoy_transcation()

def main():
    initialize_database()
    
    add_sample_data()

if __name__ == "__main__":
    main()