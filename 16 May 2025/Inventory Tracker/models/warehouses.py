class Warehouse:
    def __init__(self, w_name, w_location, capacity, contact_no):
        self.w_name = w_name
        self.w_location = w_location
        self.capacity = capacity
        self.contact_no = contact_no

    def __str__(self):
        return f"Warehouse Name = {self.w_name} | Location = {self.w_location} | Capacity = {self.capacity} | Contact_no = {self.contact_no}"    

        
