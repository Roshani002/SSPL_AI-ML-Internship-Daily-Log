from models.transcations import Transcation
from models.inventory import Inventory
from typing import List
from operations.inventory_op import inventory_operations
import sqlite3 

class transcation_operations:
    def __init__(self):
        self.connection = sqlite3.connect('inventory_tracker.db')
        self.cursor = self.connection.cursor()
        self.inventory_op = inventory_operations()

    def add_transcation(self, transcation: Transcation):
        try:
            transcationdetails = (
                transcation.p_id,
                transcation.w_id,
                transcation.quantity,
                transcation.transcation_type,
            )
            self.cursor.execute("""
            INSERT INTO TRANSCATIONS (p_id, w_id, quantity, transcation_type) VALUES (?, ?, ?, ?);
            """, transcationdetails)
            self.connection.commit()
            print(f"\nTranscation added Successfully.")

            inventory: Inventory = self.inventory_op.get_inventory_by_id(
                transcation.w_id,
                transcation.p_id
            )
            
            if inventory:
                if transcation.transcation_type.strip().lower() == 'purchase':
                    inventory.quantity += transcation.quantity
                elif transcation.transcation_type.strip().lower() == 'sale':
                    inventory.quantity -= transcation.quantity
                    if inventory.quantity < 0:
                        raise ValueError
                self.inventory_op.update_inventory(inventory)
                    
            else:
                # Create new inventory record if it doesn't exist and transaction is 'in'
                # print(f"Transaction type received: {transcation.transcation_type}")
                if transcation.transcation_type.strip().lower() == 'purchase':
                    new_inventory = Inventory(
                        p_id=transcation.p_id,
                        w_id=transcation.w_id,
                        quantity=transcation.quantity,
                        last_updated=transcation.transcation_date
                    )
                    self.inventory_op.add_inventory(new_inventory)
                else:
                    raise ValueError("Cannot perform transaction on non-existent inventory")
            self.connection.commit()
        except sqlite3.Error as e:
            self.connection.rollback()
            print(f"Error adding transcation: {e}")
            return None
        
    def get_transcation_by_id(self, transcation_id: int, w_id: int, p_id: int):
        try:
            query = """
            SELECT transaction_id, p_id, w_id, quantity, transaction_type, transaction_date
            FROM TRANSCATIONS
            WHERE transaction_id = ?
            """
            records = self.cursor.execute(query, (transcation_id)).fetchall()
            self.connection.commit()
            transcation: Transcation = None
            for row in records:
                transcation = Transcation(
                    transcation_id=row[0],
                    p_id=row[1],
                    w_id=row[2],
                    quantity=row[3],
                    transcation_type=[4],
                    transcation_date=[5]
                )
            return transcation
        except sqlite3.Error as e:
            print(f"Error fetching transcation: {e}")
            return None
        
    def get_transactions_by_product(self, p_id: int):
        try:
            query = """
            SELECT transcation_id, p_id, w_id, quantity, transcation_type, transcation_date
            FROM TRANSCATIONS
            WHERE p_id = ?
            ORDER BY transcation_date DESC;
            """
            records = self.cursor.execute(query, (p_id,)).fetchall()
            transcations = List[Transcation] = []
            self.connection.commit()
            
            for row in records:
                transcations.append(
                    Transcation(
                        transcation_id=row[0],
                        p_id=row[1],
                        w_id=row[2],
                        quantity=row[3],
                        transcation_type=row[4],
                        transcation_date=row[5]
                    )
                )
            return transcations        
        except Exception as e:
            print(f"Error displaying transcation: {e}")
        
    def get_all_transcations(self):
        try:
            query = """
            SELECT transcation_id, p_id, w_id, quantity, transcation_type, transcation_date
            FROM TRANSCATIONS;
            """
            records = self.cursor.execute(query).fetchall()
            self.connection.commit()
            transcations: List[Transcation] = []

            for row in records:
                transcations.append(
                  Transcation(
                    # transcation_id=row[0],
                    p_id=row[1],
                    w_id=row[2],
                    quantity=row[3],
                    transcation_type=row[4],
                    transcation_date=row[5]
                    )
                )
            return transcations          
        except sqlite3.Error as e:
            print(f"Error displaying transcation: {e}")

    