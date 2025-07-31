from sqlalchemy.orm import Session
from models.users import User
from datetime import date

class UserOperations:

    def __init__(self, session: Session):
        self.session = session
        
    def adduser(self, user: User):
        try:
            self.session.begin()
            existing_user = self.session.query(User).filter(User.user_id == user.user_id).first()
            if existing_user:
                print(f"\nUser with ID {user.user_id} already exists. Skipping insertion.")
                return
            self.session.add(user)
            self.session.commit()
            print(f"\n{user.name} is added successfully.")
        except Exception as e:
            print(f"Error adding user: {e}")
        finally:
            self.session.close()

    def display_allusers(self):
        try:
            self.session.begin()
            result = self.session.query(User).all()
            print("\nAll Users:")
            for r in result:
                print(f"ID = {r.user_id} | Name = {r.name} | Email = {r.email} | Phone = {r.phonenumber} | Address = {r.address} | Membership Date = {r.membership_date}")
        except Exception as e:
            self.session.rollback()
            print(f"Error displaying users: {e}")
        finally:
            self.session.close()