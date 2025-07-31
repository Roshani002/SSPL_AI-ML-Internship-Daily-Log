from sqlalchemy.orm import Session
from sqlalchemy import select, and_
from models.transcations import Transcation
from models.users import User
from models.books import Book
from datetime import datetime, timedelta

class TranscationOperations:

    def __init__(self, session: Session):
        self.session = session
        
    def addtranscation(self, user_id, book_id, issue_date):
        try:
            self.session.begin()
            user = self.session.query(User).filter_by(user_id=user_id).first()
            book = self.session.query(Book).filter_by(book_id=book_id).first()

            if not user or not book:
                print("Invalid user or book ID")
                return

            if book.available <= 0:
                print("Book not available for borrowing")
                return

            due_date = issue_date + timedelta(days=20)
            
            # Create new transaction
            new_transcation = Transcation(
                user_id=user.user_id,
                book_id=book.book_id,
                issue_date=issue_date,
                due_date=due_date
            )
            self.session.add(new_transcation)
            self.session.flush()
            # Update book availability
            book.available -= 1
            if book.available < 1:
                raise ValueError
            self.session.commit()
            print(f"\n{user.name} borrowed '{book.book_name}' on date {issue_date}")

        except Exception as e:
            self.session.rollback()
            print(f"Error adding transaction: {e}")
        finally:
            self.session.close()

    def check_overdue_books(self):
        try:
            self.session.begin()
            current_date = datetime.now().date()

            overdue_books = (
                self.session.query(
                    Transcation.transcation_id,
                    Book.book_name,
                    User.name,
                    Transcation.due_date).join(Book, Transcation.book_id == Book.book_id).join(User, Transcation.user_id == User.user_id).filter(Transcation.due_date < Transcation.return_date).all()
            )
            if overdue_books:
                print("\nOverdue Books:")
                print("Transaction ID | Book Name | User Name | Due Date")
                for transcation_id, book_name, user_name, due_date in overdue_books:
                    print(f"Transcation ID = {transcation_id} | Book Name = {book_name} | User Name = {user_name} | Due Date = {due_date}")
            else:
                print("No overdue books found")
            return overdue_books

        except Exception as e:
            print(f"Error checking overdue books: {e}")
            return []
        finally:
            self.session.close()


        
        
        
        
        


