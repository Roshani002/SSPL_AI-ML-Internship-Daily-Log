# Task 1: Library Management System  
- Use OOP to model books, users, and transactions; store data in a database; write SQL queries for reports.

## Features

- **Book Management:** Add, list, return books.
- **User Management:** Register users and view user list.
- **Transaction Handling:** Issue books, check overdue returns, and log borrowing details.

## How to run
1. **Create Virtual environment**

2. **Inspect the database and Run main file**
   - The SQLite database file `library.db` will be created in the project root.
   - If needed, delete `library.db` and rerun `main.py` to reset.

## Project Structure

```
├── main.py
├── schema.sql
├── library.db
├── models/
│   ├── books.py
│   ├── transcations.py
│   └── users.py
├── operations/
│   ├── book_operations.py
│   ├── transcation_operations.py
│   └── user_operations.py
└── pyenv/
```


