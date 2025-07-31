import sqlite3
from models.students import Student
from models.courses import Course
from models.grades import Grade
from operations.student_operations import student_operations
from operations.course_operations import course_operations
from operations.grade_operations import grade_operations

def initialize_database():
    try:
        conn = sqlite3.connect("student_management.db")
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

    # Registering Students
    student = student_operations()
    student1 = Student("Roshani", "Patel", "2003-09-02", "Female", "roshanipatel123@gmail.com", 9638116008)
    student2 = Student("Aesha", "Soni", "2003-05-12", "Female", "soniaesha234@gmail.com", 7069560794)
    student3 = Student("Kajal", "Thakkar", "2005-10-06", "Female", "kajalt123@gmail.com", 8735925698)
    student4 = Student("Rajan", "Panchal", "2003-04-17", "Male", "rajanp1234@gmail.com",8347062609)
    student.register_student(student1)
    student.register_student(student2)
    student.register_student(student3)
    student.register_student(student4)
    student.display_students()

    # Add courses
    courses = course_operations()
    course1 = Course("Data Structures and Algorithms", "CS201", 7)
    course2 = Course("Computer Networks", "CS302", 8)
    course3 = Course("Object Oriented Programming", "CS501", 7)
    course4 = Course("Compiler Design", "CS212", 8)
    course5 = Course("Python for Machine Learning", "CS312", 9)
    courses.add_course(course1)
    courses.add_course(course2)
    courses.add_course(course3)
    courses.add_course(course4)
    courses.add_course(course5)
    courses.display_courses()

    # Add grades
    grades = grade_operations()
    grade1 = Grade(1, 1, "A+", "Excellent")
    grade2 = Grade(2, 4, "A", "Very Good")
    grade3 = Grade(3, 2, "B", "Good")
    grade4 = Grade(4, 5, "C", "Poor")
    grades.add_grade(grade1)
    grades.add_grade(grade2)
    grades.add_grade(grade3)
    grades.add_grade(grade4)
    grades.display_grades()

    student.query_performance()
if __name__ == "__main__":
    main()
