# from sqlalchemy.orm import Session
from create_db import DatabaseManager
from models.books import Book
from models.users import User
from operations.book_operations import BookOperations
from operations.user_operations import UserOperations
from operations.transcation_operations import TranscationOperations
from datetime import date

def initialize_database():
    db = DatabaseManager()
    db.setup_database()
    return db.get_session()

def main():
    session = initialize_database()

    # BOOK operations
    bope = BookOperations(session)
    book1 = Book(
        book_name = "Verity", 
        author = "Colleen Hoover", 
        published_year = 2018, 
        genre = "thriller", 
        available = 7)
    book2 = Book(
        book_name = "It ends with us", 
        author = "Colleen Hoover", 
        published_year = 2016, 
        genre = "romance", 
        available = 10)
    book3 = Book(
        book_name = "Atomic Habits", 
        author = "James Clear", 
        published_year = 2018, 
        genre = "Self-development", 
        available = 7)
    bope.addbook(book1)
    bope.addbook(book2)
    bope.addbook(book3)
    bope.get_book_by_id(2)
    bope.display_allbooks()


    # USER Operations
    uope = UserOperations(session)
    user1 = User(
        user_id = 101,
        name = "Roshani", 
        email = "roshani123@gmail.com",
        phonenumber = 9638116008,
        address = "Ahmedabad, Gujarat",
        membership_date = date(2025,4,28))
    user2 = User(
        user_id = 102,
        name = "Kavita", 
        email = "kavita3333@gmail.com",
        phonenumber = 9824486250,
        address = "Nikol, Gujarat",
        membership_date = date(2025,3,17))
    uope.adduser(user1)
    uope.adduser(user2)
    uope.display_allusers()
    
    # TRANSCATION Operations
    tope = TranscationOperations(session)
    tope.addtranscation(102,1,date(2025,4,30))
    tope.addtranscation(101,2,date(2025,4,15))
    tope.check_overdue_books()

    # Return a book
    bope.return_book(1, 'Verity', 102)
    

if __name__ == "__main__":
    main()