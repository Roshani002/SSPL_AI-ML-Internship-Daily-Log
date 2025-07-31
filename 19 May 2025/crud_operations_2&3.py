from sqlalchemy import create_engine, select, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

engine = create_engine('sqlite:///user.db')
connection = engine.connect()

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    contact_no = Column(Integer)

    def __repr__(self):
        return "<USer(first_name = '{}', last_name = '{}', email = '{}', contact_no = '{}')>".format(
            self.first_name, self.last_name, self.email, self.contact_no
        )
    
session = Session(engine)
def add_all_records():
    Base.metadata.create_all(engine)
# for adding multiple entries
    with Session(engine) as session:
        user_1 = User(
            first_name = "Roshani",
            last_name = "Patel",
            email = "roshanipatel123@gmail.com",
            contact_no = 9638116008
        )
        user_2 = User(
            first_name = "Yash",
            last_name = "Jogi",
            email = "yashj23@gmail.com",
            contact_no = 9765234578
        )
        user_3 = User(
            first_name = "Vishwa",
            last_name = "Patel",
            email = "vishwap0013@gmail.com",
            contact_no = 9635214569
        )
        
        session.add_all([user_1, user_2, user_3])
        session.commit()
        print("\nRecords addded successfully.")
        
        # To interact with databse you must create and use a session
        # Session = sessionmaker(bind=engine)
        # session = Session()

        # for add single entry
        # user_1 = User(first_name = 'Roshani', last_name = 'Patel', email = 'roshanip123@gmail.com', contact_no = 9638116008)
        # session.add(user_1)
        # session.commit()
        # # query
        # user = session.query(User).filter_by(first_name = 'Roshani').first()
        # print(user)

def select_record():
    # for create a new select object OR Simple SELECT
    stmt = select(User).where(User.last_name.in_(["Patel"]))
    print("\nSelected Users whose last_name is Patel:")
    for user in session.scalars(stmt):
        print(user)

    query = select(User).where(User.contact_no.endswith(78))
    print("\nSelected User whose contact no ends with digits 78:")
    for quer in session.scalars(query):
        print(quer)


def update_record():
    # for update
    stmts = select(User).where(User.first_name == "Yash")
    Yash = session.scalars(stmts).one()

    Yash.first_name = "Krisha"
    Yash.last_name = "Gadhiya"
    Yash.email = "krisha9876@gmail.com"
    if Yash.email:
        session.commit()
        print("\nRecord Updated.")
    else:
        print("\nRecord not updated")

def delete_record():
    # for delete
    user_to_delete = session.get(User,3)
    if user_to_delete:
        session.delete(user_to_delete)
        session.commit()
        print("\nUser deleted successfully.")    
    else:
        print("\nUSer not found.")

add_all_records()
select_record()
# update_record()
# delete_record()
    
    