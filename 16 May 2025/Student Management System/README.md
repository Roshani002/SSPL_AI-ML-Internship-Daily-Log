# Task 3: Student Management System  
- Model students, courses, and grades using OOP; store data in a database; query for student performance.

## Features

- **Student Registration:** Add and list students.
- **Course Management:** Add and display courses.
- **Grade Handling:** Assign grades, view performance, and run performance queries.

## How to run
1. **Create Virtual environment**

2. **Inspect the database and Run main file**
   - The SQLite database file `student_management.db` will be created in the project root.
   - If needed, delete `student_management.db` and rerun `main.py` to reset.

## Project Structure

```
Student_Management_System/
├── main.py
├── schema.sql
├── student_management.db
├── models/
│   ├── students.py
│   ├── courses.py
│   └── grades.py
└── operations/
    ├── student_operations.py
    ├── course_operations.py
    └── grade_operations.py
```
