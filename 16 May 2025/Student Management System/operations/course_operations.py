from models.courses import Course
import sqlite3 

class course_operations:
    def __init__(self):
        self.connection = sqlite3.connect('student_management.db')
        self.cursor = self.connection.cursor()

    def add_course(self, course: Course):
        try:
            coursedetails = (
                course.course_name,
                course.course_code,
                course.credits,
            )
            self.cursor.execute("INSERT INTO COURSES (course_name, course_code, credits) VALUES (?, ?, ?)", coursedetails)
            self.connection.commit()
            print(f"{course.course_name} added Successfully.")
        except sqlite3.IntegrityError as e:
            print(f"Error adding Course: {e}")
        except sqlite3.Error as e:
            print(f"Error adding course: {e}")


    def display_courses(self):
        courses = self.cursor.execute('SELECT * FROM COURSES').fetchall()
        self.connection.commit()
        print("Courses added:")
        print("Course ID | Course Name | Course Code | Credits")
        for course in courses:
            course_id, course_name, course_code, credits = course
            print(f"{course_id} | {course_name} | {course_code} | {credits}")






        