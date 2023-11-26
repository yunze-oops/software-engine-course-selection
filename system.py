import sqlite3

class CourseSelectionSystem:
    def __init__(self, db_file="course_selection.db"):
        self.connection = sqlite3.connect(db_file)
        self.create_tables()

    def create_tables(self):
        with self.connection:
            cursor = self.connection.cursor()
            # Create Students table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS students (
                    student_id TEXT PRIMARY KEY,
                    name TEXT,
                    password TEXT
                )
            """)
            # Create Courses table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS courses (
                    course_id INTEGER PRIMARY KEY,
                    name TEXT,
                    num_students INTEGER DEFAULT 0
                )
            """)
            # Create SelectedCourses table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS selected_courses (
                    student_id TEXT,
                    course_id INTEGER,
                    FOREIGN KEY (student_id) REFERENCES students(student_id),
                    FOREIGN KEY (course_id) REFERENCES courses(course_id),
                    PRIMARY KEY (student_id, course_id)
                )
            """)

    def create_student_account(self, student_id, student_name, password):
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute("INSERT INTO students VALUES (?, ?, ?)", (student_id, student_name, password))

    def student_login(self, student_id, password):
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM students WHERE student_id = ? AND password = ?", (student_id, password))
            return cursor.fetchone() is not None

    def student_select_course(self, student_id):
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute("""
                SELECT course_id, name
                FROM courses
                WHERE course_id NOT IN (
                    SELECT course_id
                    FROM selected_courses
                    WHERE student_id = ?
                )
            """, (student_id,))
            available_courses = cursor.fetchall()
            for course in available_courses:
                print(f"CourseID: {course[0]}, Course Name: {course[1]}")

            selected_course_id = input("Enter the CourseID you want to select: ")
            cursor.execute("INSERT INTO selected_courses VALUES (?, ?)", (student_id, selected_course_id))
            cursor.execute("UPDATE courses SET num_students = num_students + 1 WHERE course_id = ?", (selected_course_id,))
            print("Course selected successfully!")

    def student_delete_course(self, student_id):
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute("""
                SELECT selected_courses.course_id, name
                FROM selected_courses
                JOIN courses ON selected_courses.course_id = courses.course_id
                WHERE student_id = ?
            """, (student_id,))
            selected_courses = cursor.fetchall()
            for course in selected_courses:
                print(f"CourseID: {course[0]}, Course Name: {course[1]}")

            deleted_course_id = input("Enter the CourseID you want to delete: ")
            cursor.execute("DELETE FROM selected_courses WHERE student_id = ? AND course_id = ?", (student_id, deleted_course_id))
            cursor.execute("UPDATE courses SET num_students = num_students - 1 WHERE course_id = ?", (deleted_course_id,))
            print("Course deleted successfully!")

    def student_check_courses(self, student_id):
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute("""
                SELECT selected_courses.course_id, name
                FROM selected_courses
                JOIN courses ON selected_courses.course_id = courses.course_id
                WHERE student_id = ?
            """, (student_id,))
            selected_courses = cursor.fetchall()
            print("Your selected courses:")
            for course in selected_courses:
                print(f"CourseID: {course[0]}, Course Name: {course[1]}")

    def admin_login(self, username, password):
        return username == "admin" and password == "admin"

    def admin_check_all_students(self):
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM students")
            all_students = cursor.fetchall()
            print("All students:")
            for student in all_students:
                print(f"StudentID: {student[0]}, Student Name: {student[1]}")

    def admin_check_all_courses(self):
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM courses")
            all_courses = cursor.fetchall()
            print("All courses:")
            for course in all_courses:
                print(f"CourseID: {course[0]}, Course Name: {course[1]}, Number of Students: {course[2]}")

    def admin_add_course(self, course_name):
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute("INSERT INTO courses (name) VALUES (?)", (course_name,))
            print("Course added successfully!")

    def admin_delete_course(self):
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM courses")
            all_courses = cursor.fetchall()
            print("All courses:")
            for course in all_courses:
                print(f"CourseID: {course[0]}, Course Name: {course[1]}")

            deleted_course_id = input("Enter the CourseID you want to delete: ")
            cursor.execute("DELETE FROM courses WHERE course_id = ?", (deleted_course_id,))
            print("Course deleted successfully!")


# Example Usage:
system = CourseSelectionSystem()

# ... (rest of the code remains unchanged)

# Don't forget to close the connection when done
system.connection.close()
