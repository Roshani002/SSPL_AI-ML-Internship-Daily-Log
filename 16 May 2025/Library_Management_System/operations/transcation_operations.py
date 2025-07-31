import sqlite3
from models.transcations import Transcations
from models.users import User
from datetime import datetime, timedelta

class TranscationOperations:
    def __init__(self):
        self.connection = sqlite3.connect('library.db')
        self.cursor = self.connection.cursor()
        
    def addtranscation(self, user_id : int, book_id : int):
        try:
            self.cursor.execute("SELECT name FROM USERS WHERE user_id = ?", (user_id,))
            user_name = self.cursor.fetchone()[0]
            self.cursor.execute("SELECT book_name FROM BOOKS WHERE book_id = ?", (book_id,))
            book_name = self.cursor.fetchone()[0]

            issue_date = datetime.now().strftime("%Y-%m-%d")
            due_date = (datetime.now() + timedelta(days=20)).strftime("%Y-%m-%d")
            fineamount = 0

            # Check if book is available
            self.cursor.execute("SELECT available FROM BOOKS WHERE book_id = ?", (book_id,))
            available = self.cursor.fetchone()[0]
            
            if available <= 0:
                print("Book not available for borrowing")
                return

            # Add transaction
            self.cursor.execute(
                "INSERT INTO TRANSCATIONS (user_id, book_id, issue_date, due_date, fineamount) VALUES (?, ?, ?, ?, ?)",
                (user_id, book_id, issue_date, due_date, fineamount)
            )
            
            # Update book availability
            self.cursor.execute("UPDATE BOOKS SET available = available - 1 WHERE book_id = ?", (book_id,))
            self.connection.commit()
            print(f"{user_name} borrowed '{book_name}'")
        except sqlite3.Error as e:
            print(f"Error adding transaction: {e}")

    def check_overdue_books(self):
        try:
            current_date = datetime.now().strftime("%Y-%m-%d")
            self.cursor.execute("""
                SELECT t.transaction_id, b.book_name, u.name, t.due_date 
                FROM TRANSCATIONS t
                JOIN BOOKS b ON t.book_id = b.book_id
                JOIN USERS u ON t.user_id = u.user_id
                WHERE t.return_date IS NULL AND t.due_date < ?
            """, (current_date,))
            
            overdue_books = self.cursor.fetchall()
            
            if overdue_books:
                print("\nOverdue Books:")
                print("Transaction ID | Book Name | User Name | Due Date")
                for book in overdue_books:
                    print(f"{book[0]} | {book[1]} | {book[2]} | {book[3]}")
            else:
                print("No overdue books found")
                
            return overdue_books
        except sqlite3.Error as e:
            print(f"Error checking overdue books: {e}")
            return []
        
    


        
        
        
        
        


