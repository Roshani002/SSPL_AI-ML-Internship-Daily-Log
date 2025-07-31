import sqlite3
from models.users import User

class UserOperations:
    def __init__(self):
        self.connection = sqlite3.connect('library.db')
        self.cursor = self.connection.cursor()
        
    def adduser(self, user: User):
        try:
            self.cursor.execute("SELECT * FROM USERS WHERE user_id = ?", (user.id,))
            if self.cursor.fetchone():
                print(f"User with ID {user.id} already exists. Skipping insertion.")
                return
            
            userdetails = (
                user.id,
                user.name,
                user.email,
                user.phonenumber,
                user.address,
                user.membership_date 
            )   
            self.cursor.execute('INSERT INTO USERS (user_id, name, email, phonenumber, address, membership_date) VALUES  (?, ?, ?, ?, ?, ?)', userdetails)
            self.connection.commit()
            print(f"{user.name} is added successfully.")
        except sqlite3.Error as e:
            print(f"Error adding user: {e}")

    def display_allusers(self):
        try:
            self.cursor.execute('SELECT * FROM USERS')
            users = self.cursor.fetchall()
            print("\nAll Users:")
            print("ID | Name | Email | Phone | Address | Membership Date")
            for user in users:
                print(f"{user[0]} | {user[1]} | {user[2]} | {user[3]} | {user[4]} | {user[5]}")
        except sqlite3.Error as e:
            print(f"Error displaying users: {e}")