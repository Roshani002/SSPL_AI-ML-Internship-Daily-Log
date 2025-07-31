from models.inventory import Inventory
from datetime import datetime
from typing import List
import sqlite3 

class inventory_operations:
    def __init__(self):
        self.connection = sqlite3.connect('inventory_tracker.db')
        self.cursor = self.connection.cursor()

    def add_inventory(self, inventory: Inventory):
        try:
            inventorydetails = (
                inventory.p_id,
                inventory.w_id,
                inventory.quantity,
                inventory.last_updated
            )
            self.cursor.execute(f"""
            INSERT INTO Inventory (p_id, w_id, quantity, last_updated) VALUES (?, ?, ?, ?);
            """, inventorydetails)
            self.connection.commit()
            print(f"Inventory with Product ID {inventory.p_id} and Warehouse ID {inventory.w_id} of {inventory.quantity} quantity added Successfully.")
        except sqlite3.Error as e:
            print(f"Error When adding inventory data: {e}")

    def get_inventory_by_id(self, w_id: int, p_id: int):
        try:
            query = """
            SELECT inventory_id, p_id, w_id, quantity, last_updated
            FROM INVENTORY 
            WHERE p_id = ? AND w_id = ?;
            """
            records = self.cursor.execute(query, (p_id, w_id)).fetchall()
            self.connection.commit()
            inventory: Inventory = None
            for row in records:
                inventory = Inventory(
                    # inventory_id=row[0],
                    p_id=row[1],
                    w_id=row[2],
                    quantity=row[3],
                    last_updated=row[4]
                )
            return inventory
        except sqlite3.Error as e:
            print(f"Error fetching inventory: {e}")
            return None
        
    def get_all_inventorys(self):
        try:
            query = """
            SELECT inventory_id, p_id, w_id, quantity, last_updated
            FROM INVENTORY;
            """
            records = self.cursor.execute(query).fetchall()
            self.connection.commit()
            inventory : List[Inventory] = []
            for row in records:
                inventory.append(
                    Inventory(
                        # inventory_id=row[0],
                        p_id=row[1],
                        w_id=row[2],
                        quantity=row[3],
                        last_updated=row[4]
                    )
                )
                return inventory       
        except sqlite3.Error as e:
            print(f"Error displaying inventory: {e}")

    def update_inventory(self, inventory: Inventory):
        try:
            query = """
            UPDATE INVENTORY
            SET quantity = ?, last_updated = CURRENT_TIMESTAMP
            WHERE p_id = ? AND w_id = ?;
            """
            self.cursor.execute(query, (inventory.quantity, inventory.p_id, inventory.w_id))
            self.connection.commit()
            print(f"Inventory updated successfully.")
        except sqlite3.Error as e:
            print(f"Error Updating inventory: {e}")
    
    def delete_inventory(self, inventory_id: int):
        try:
            query = """
            DELETE FROM INVENTORY
            WHERE inventory_id = ?
            """
            self.cursor.execute(query, (inventory_id,))
            self.connection.commit()
            print(f"Inventory with ID {inventory_id} deleted successfully.")
        except sqlite3.Error as e:
            print(f"Error when Deleting inventory: {e}")

            