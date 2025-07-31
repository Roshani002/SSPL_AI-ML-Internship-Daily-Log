CREATE TABLE IF NOT EXISTS BOOKS  (
	book_id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_name varchar(500),
    author varchar(500),
    published_year int,
    genre varchar(500),
    available int
);


CREATE TABLE IF NOT EXISTS USERS (
    user_id int PRIMARY KEY,
    name varchar(500),
    email varchar(200),
    phonenumber int,
    address varchar(1000),
    membership_date date
);


CREATE TABLE IF NOT EXISTS TRANSCATIONS (
	transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id int,
    book_id int,
    issue_date date,
    due_date date,
    return_date date,
    fineamount DECIMAL (10,2),
    
    FOREIGN KEY (user_id) REFERENCES USERS (user_id),
    FOREIGN KEY (book_id) REFERENCES BOOKS (book_id)
);


