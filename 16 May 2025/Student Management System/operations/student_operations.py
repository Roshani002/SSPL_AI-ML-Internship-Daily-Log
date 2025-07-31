from models.students import Student
import sqlite3 

class student_operations:
    def __init__(self):
        self.connection = sqlite3.connect('student_management.db')
        self.cursor = self.connection.cursor()

    def register_student(self, student: Student):
        try:
            studentdetails = (
                student.first_name,
                student.last_name,
                student.dob,
                student.gender,
                student.email,
                student.phone_number
            )
            self.cursor.execute("INSERT INTO STUDENTS (first_name, last_name, dob, gender, email, phone_number) VALUES (?, ?, ?, ?, ?, ?)", studentdetails)
            self.connection.commit()
            print(f"{student.first_name} {student.last_name} registered Successfully.")
        except sqlite3.IntegrityError as e:
            print(f"Registration failed: {e}")
        except sqlite3.Error as e:
            print(f"Error registering student: {e}")

    def display_students(self):
        students = self.cursor.execute('SELECT * FROM STUDENTS').fetchall()
        self.connection.commit()
        print("Students Registered:")
        for student in students:
            student_id, first_name, last_name, dob, gender, email, phone_number = student
            print(f"{student_id} | {first_name} | {last_name} | {dob} | {gender} | {email} | {phone_number}")

    def query_performance(self):
        # apply join query
        self.cursor.execute(""" 
        SELECT 
            s.student_id, 
            s.first_name, 
            s.last_name, 
            c.course_name, 
            c.credits 
        FROM 
            STUDENTS s
        INNER JOIN GRADES g ON s.student_id = g.student_id
        INNER JOIN COURSES c ON g.course_id = c.course_id
        WHERE 
            g.remarks = 'Excellent';
        """)
        students1 = self.cursor.fetchall()
        self.connection.commit()
        print("Students who got grade A++:")
        for student in students1:
            student_id, first_name, last_name, course_name, credits = student
            print(f"{student_id} | {first_name} | {last_name} | {course_name} | {credits}")

        query_2 = self.cursor.execute("""
        SELECT 
            S.first_name, 
            S.last_name, 
            S.email, 
            S.phone_number, 
            C.course_name, 
            C.course_code, 
            G.grade
        FROM 
            STUDENTS AS S
        INNER JOIN COURSES AS C ON S.student_id = G.student_id
        INNER JOIN GRADES AS G ON G.course_id = C.course_id;
        """)
        students2 = query_2.fetchall()
        self.connection.commit()
        print("Grades for each student across courses:")
        for student in students2:
            first_name, last_name, email, phone_number, course_name, course_code, grade = student
            print(f"{first_name} | {last_name} | {email} | {phone_number} | {course_name} | {course_code} | {grade}")



