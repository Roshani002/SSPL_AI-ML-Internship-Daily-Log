from models.grades import Grade
import sqlite3 

class grade_operations:
    def __init__(self):
        self.connection = sqlite3.connect('student_management.db')
        self.cursor = self.connection.cursor()

    def add_grade(self, grade: Grade):
        try:
            gradedetails = (
                grade.student_id,
                grade.course_id,
                grade.grade,
                grade.remarks
            )
            self.cursor.execute("INSERT INTO GRADES (student_id, course_id, grade, remarks) VALUES (?, ?, ?, ?)", gradedetails)
            self.connection.commit()
        except sqlite3.Error as e:
            print(f"Error adding grade: {e}")

    def display_grades(self):
        self.cursor.execute('SELECT * FROM GRADES')
        grades = self.cursor.fetchall()
        self.connection.commit()
        print("Grades added:")
        for grade in grades:
            student_id, course_id, grade, remarks = grade
            print(f"{student_id} | {course_id} | {grade} | {remarks}")







        