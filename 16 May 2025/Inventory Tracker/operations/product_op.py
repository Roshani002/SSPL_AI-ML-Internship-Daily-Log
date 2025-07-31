from models.products import Product
from typing import List
import sqlite3 

class product_operations:
    def __init__(self):
        self.connection = sqlite3.connect('inventory_tracker.db')
        self.cursor = self.connection.cursor()

    def add_product(self, product: Product):
        try:
            productdetails = (
                product.p_name,
                product.price,
                product.category
            )
            self.cursor.execute("INSERT INTO PRODUCTS (p_name, price, category) VALUES (?, ?, ?)", productdetails)
            self.connection.commit()
            print(f"{product.p_name} added Successfully.")
        except sqlite3.Error as e:
            print(f"Error adding Product: {e}")

    def get_product_by_id(self, p_id: int):
        try:
            query = """
            SELECT p_id, p_name, price, category
            FROM PRODUCTS
            WHERE p_id = ?;
            """
            
            records = self.cursor.execute(query, (p_id,)).fetchall()
            self.connection.commit()
            product: Product = None
            for row in records:
                product = Product(
                    p_name = row[1],
                    price = row[2],
                    category = row[3]          
                )
            return product
        except sqlite3.Error as e:
            print(f"Error fetching product: {e}")
            return None
        
    def get_all_products(self):
        try:
            query = f"""
            SELECT p_id, p_name, price, category
            FROM PRODUCTS;
            """
            records = self.cursor.execute(query).fetchall()
            self.connection.commit()
            products: List[Product] = []
            for row in records:
                products.append(Product(
                    # p_id = row[0],
                    p_name = row[1],
                    price = row[2],
                    category = row[3]
                ))
            return products
        except sqlite3.Error as e:
            print(f"Error displaying Products: {e}")
            return []

    def update_product(self, product: Product, p_id: int):
        try:
            # self.cursor.execute(f"""
            # UPDATE PRODUCTS
            # SET p_name = {product.p_name}, price = {product.price}, category = {product.category}
            # WHERE p_id = {p_id};
            # """)
            query = """
            UPDATE PRODUCTS
            SET p_name = ?, price = ?, category = ?
            WHERE p_id = ?;
            """
            self.cursor.execute(query, (product.p_name, product.price, product.category, p_id))
            self.connection.commit()
            print(f"\nProduct with ID {p_id} updated successfully.")
        except sqlite3.Error as e:
            print(f"Error Updating Product: {e}")
    
    def delete_product(self, p_id: int):
        try:
            query = """
            DELETE FROM PRODUCTS
            WHERE p_id = ?;
            """
            self.cursor.execute(query, (p_id,))
            self.connection.commit()
            print(f"Product with ID {p_id} deleted successfully.")
        except sqlite3.Error as e:
            print(f"Error when Deleting Product: {e}")

            