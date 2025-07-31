CREATE TABLE IF NOT EXISTS STUDENTS (
    student_id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    dob date NOT NULL,
    gender TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    phone_number TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS COURSES (
    course_id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_name TEXT NOT NULL UNIQUE,
    course_code TEXT NOT NULL UNIQUE,
    credits int NOT NULL
);

CREATE TABLE IF NOT EXISTS GRADES (
    student_id int NOT NULL,
    course_id int NOT NULL,
    grade TEXT NOT NULL UNIQUE,
    remarks TEXT,

    FOREIGN KEY (student_id) REFERENCES STUDENTS(student_id),
    FOREIGN KEY (course_id) REFERENCES COURSES (course_id)
);



