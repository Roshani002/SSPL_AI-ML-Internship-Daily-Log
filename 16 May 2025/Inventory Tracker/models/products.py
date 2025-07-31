class Product:
    def __init__(self, p_name, price, category):
        self.p_name = p_name
        self.price = price
        self.category = category

    def __str__(self):
        return f"Product Name = {self.p_name} | Price = {self.price} | Category = {self.category}"    
