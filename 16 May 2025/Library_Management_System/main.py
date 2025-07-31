import sqlite3
from models.books import Book
from models.users import User
from models.transcations import Transcations
from operations.book_operations import BookOperations
from operations.user_operations import UserOperations
from operations.transcation_operations import TranscationOperations

def initialize_database():
    try:
        conn = sqlite3.connect("library.db")
        cur = conn.cursor()

        sql_script = None
        with open ('schema.sql', 'r') as file:
            sql_script = file.read()

        statements = sql_script.strip().split(";")

        for stmt in statements:
            if stmt.strip():
                cur.execute(stmt)

        conn.commit()
        conn.close()
        print("Database initialized successfully")
    except Exception as e:
        print(f"Error initializing database: {e}")

def main():
    initialize_database()

    # Book operations
    boperation = BookOperations()
    book1 = Book("Verity", "Colleen Hoover", 2018, "thriller", 7)
    book2 = Book("It ends with us", "Collen Hoover", 2016, "romance", 10)
    book3 = Book("You belong with me", "Suchi Batra", 2021, "romance", 5)
    book4 = Book("Atomic Habits","James Clear", 2018, "Self-development", 7)
    boperation.addbook(book1)
    boperation.addbook(book2)
    boperation.addbook(book3)
    boperation.addbook(book4)
    boperation.display_allbooks()

    # user operations
    uopertion = UserOperations()
    user1 = User(102, "Roshani", "roshani123@gmail.com", 9638116008, "Ahmedabad, Gujarat", "2025-01-23")
    user2 = User(202, "Kavita", "kavi1234@gmail.com", 9988776655, "Surat, Gujarat", "2025-04-17")
    uopertion.adduser(user1)
    uopertion.adduser(user2)
    uopertion.display_allusers()

    # Transcation operations
    toperation = TranscationOperations()
    toperation.addtranscation(202,1)
    toperation.check_overdue_books()

    # Return a book
    boperation.return_book(1, 202)
    boperation.display_allbooks()

if __name__ == "__main__":
    main()