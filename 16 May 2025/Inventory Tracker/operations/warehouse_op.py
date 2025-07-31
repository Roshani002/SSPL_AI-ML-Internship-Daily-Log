from models.warehouses import Warehouse
from typing import List
import sqlite3 

class warehouse_operations:
    def __init__(self):
        self.connection = sqlite3.connect('inventory_tracker.db')
        self.cursor = self.connection.cursor()

    def add_warehouse(self, warehouse: Warehouse):
        try:
            warehousedetails = (
                warehouse.w_name,
                warehouse.w_location,
                warehouse.capacity,
                warehouse.contact_no
            )
            self.cursor.execute(f"""
            INSERT INTO WAREHOUSES (w_name, w_location, capacity, contact_no) VALUES (?, ?, ?, ?);
            """, warehousedetails)
            self.connection.commit()
            print(f"{warehouse.w_name} Warehoouse added Successfully.")
        except sqlite3.Error as e:
            print(f"Error When adding warehouse data: {e}")

    def get_warehouse_by_id(self, w_id: int):
        try:
            query = f"""
            SELECT w_id, w_name, w_location, capacity, contact_no
            FROM warehouses
            WHERE w_id = ?;
            """
            records = self.cursor.execute(query, (w_id,)).fetchall()
            self.connection.commit()
            warehouse: Warehouse = None
            for row in records:
                warehouse = Warehouse(
                    w_name=row[1],
                    w_location=row[2],
                    capacity=row[3],
                    contact_no=row[4]
                )
            return warehouse
        except sqlite3.Error as e:
            print(f"Error fetching warehouse: {e}")
            return None
        
    def get_all_warehouses(self):
        try:
            query = """
            SELECT w_id, w_name, w_location, capacity, contact_no
            FROM WAREHOUSES;
            """
            records = self.cursor.execute(query).fetchall()
            self.connection.commit()
            warehouses : List[Warehouse] = []
            for row in records:
                warehouses.append(
                    Warehouse(
                        # w_id=row[0],
                        w_name=row[1],
                        w_location=row[2],
                        capacity=row[3],
                        contact_no=row[4]
                    )
                )
            return warehouses
        except sqlite3.Error as e:
            print(f"Error displaying warehouses: {e}")

    def update_warehouse(self, warehouse: Warehouse, w_id: int):
        try:
            query = """
            UPDATE WAREHOUSES
            SET capacity = ?
            WHERE w_id = ?;
            """
            self.cursor.execute(query, (warehouse.capacity, w_id))
            self.connection.commit()
            print(f"\nWarehouse with ID {w_id} updated successfully.")
        except sqlite3.Error as e:
            print(f"Error Updating warehouse: {e}")
    
    def delete_warehouse(self, w_id: int):
        try:
            query = """
            DELETE FROM WAREHOUSES
            WHERE w_id = ?;
            """
            self.cursor.execute(query, (w_id,))
            self.connection.commit()
            print(f"Warehouse with ID {w_id} deleted successfully.")
        except sqlite3.Error as e:
            print(f"Error when Deleting warehouse: {e}")

            