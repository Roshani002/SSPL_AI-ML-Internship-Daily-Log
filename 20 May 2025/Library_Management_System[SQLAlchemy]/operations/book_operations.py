from sqlalchemy.orm import Session
from models.books import Book
from models.users import User

class BookOperations:

    def __init__(self, session: Session):
        self.session = session
        
    def addbook(self, book: Book):
        try:
            self.session.begin()
            existing_book = self.session.query(Book).filter(
                Book.book_name == book.book_name,
                Book.author == book.author
            ).first()
            if existing_book:
                print(f"{book.book_name} by {book.author} book already exists. Skipping insertion.")
                return

            self.session.add(book)
            self.session.commit()
            print(f"{book.book_name} added successfully.")
        except Exception as e:
            self.session.rollback()
            print(f"Error adding book: {e}")
        finally:
            self.session.close()

    def get_book_by_id(self, book_id):
        try:
            self.session.begin()
            get_book = self.session.query(Book).filter(Book.book_id == book_id).one()
            self.session.commit()
            if get_book:
                print("\nBook by Selected ID:")
                print(f"ID = {get_book.book_id} | Name = {get_book.book_name} | Author = {get_book.author} | Genre = {get_book.genre} | Published Year = {get_book.published_year} | Available = {get_book.available}")
            else:
                print("Book not found")
        except Exception as e:
            self.session.rollback()
            print(f"Error getting book: {e}")
        finally:
            self.session.close()

    def return_book(self, book_id, book_name, user_id):
        try:
            self.session.begin()
            
            bookname = self.session.query(Book).filter(Book.book_name == book_name).one()
            userid = self.session.query(User).filter(User.user_id == user_id).one()
            update_book = self.session.query(Book).filter(Book.book_id == book_id).update({'available': Book.available + 1})
            self.session.commit()
            if update_book:
                print(f"{bookname.book_name} returned successfully by User {userid.user_id}")
        except Exception as e:
            self.session.rollback()
            print(f"Error returning book: {e}")
        finally:
            self.session.close()
    
    def display_allbooks(self):
        try:
            self.session.begin()
            result = self.session.query(Book).all()
            print("\nDisplaying all Books:")
            for r in result:
                print(f"ID = {r.book_id} | Name = {r.book_name} | Author = {r.author} | Genre = {r.genre} | Published Year = {r.published_year} | Available = {r.available}")
        except Exception as e:
            self.session.rollback()
            print(f"Error displaying books: {e}")
        finally:
            self.session.close()
     
    


        