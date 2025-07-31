import sqlite3
from models.books import Book
from models.users import User

class BookOperations:
    def __init__(self):
        self.connection = sqlite3.connect('library.db')
        self.cursor = self.connection.cursor()
        
    def addbook(self, book: Book):
        try:
            self.cursor.execute("SELECT * FROM BOOKS WHERE book_name = ? AND author = ? ", (book.name, book.author))
            if self.cursor.fetchone():
                print(f"{book.name} by {book.author} book already exists. Skipping insertion.")
                return
            
            bookdetails = (
                book.name,
                book.author,
                book.published_year,
                book.genre,
                book.available
            )
            self.cursor.execute('INSERT INTO BOOKS (book_name, author, published_year, genre, available) VALUES  (?, ?, ?, ?, ?)', bookdetails)
            self.connection.commit()
            print(f"{book.name} added successfully.")
        except sqlite3.Error as e:
            print(f"Error adding book: {e}")

    def get_book_by_id(self, book_id = int):
        try:
            self.cursor.execute("SELECT * FROM BOOKS WHERE book_id = ?", (book_id,))
            book = self.cursor.fetchone()
            if book:
                print(f"Book found: {book}")
                return book
            else:
                print("Book not found")
                return None
        except sqlite3.Error as e:
            print(f"Error fetching book: {e}")
            return None
        
    def return_book(self, book_id: int, user_id: int):
        try:
            # Get book and user details
            self.cursor.execute("SELECT book_name FROM BOOKS WHERE book_id = ?", (book_id,))
            book_name = self.cursor.fetchone()[0]
            
            self.cursor.execute("SELECT name FROM USERS WHERE user_id = ?", (user_id,))
            user_name = self.cursor.fetchone()[0]

            # Update book availability
            self.cursor.execute("UPDATE BOOKS SET available = available + 1 WHERE book_id = ?", (book_id,))
            self.connection.commit()
            print(f"'{book_name}' returned successfully by {user_name}")
        except sqlite3.Error as e:
            print(f"Error returning book: {e}")

    def display_allbooks(self):
        try:
            self.cursor.execute('SELECT * FROM BOOKS')
            books = self.cursor.fetchall()
            print("\nAll Books:")
            print("ID | Name | Author | Year | Genre | Available")
            for book in books:
                print(f"{book[0]} | {book[1]} | {book[2]} | {book[3]} | {book[4]} | {book[5]}")
        except sqlite3.Error as e:
            print(f"Error displaying books: {e}")
            
    


        