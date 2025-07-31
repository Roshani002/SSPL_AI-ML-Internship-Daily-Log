class Inventory:
    def __init__(self, p_id, w_id, quantity, last_updated):
        self.p_id = p_id
        self.w_id = w_id
        self.quantity = quantity
        self.last_updated = last_updated

    def __str__(self):
        return f"Product ID = {self.p_id} | Warehouse ID = {self.w_id} | Quantity = {self.quantity} | Last Updated = 54{self.last_updated}"    

        
        
