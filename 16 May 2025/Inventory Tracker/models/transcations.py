class Transcation:
    def __init__(self, p_id, w_id, quantity, transcation_type, transcation_date):
        self.p_id = p_id
        self.w_id = w_id
        self.quantity = quantity
        self.transcation_type = transcation_type
        self.transcation_date = transcation_date
        
    def __str__(self):
        return f"Product ID = {self.p_id} | Warehouse ID = {self.w_id} | Quantity = {self.quantity} | Transcation Type = {self.transcation_type} | Transcation Date = {self.transcation_date}"    

