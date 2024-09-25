import sqlite3
from person import Person
from course import Course
from prettytable import PrettyTable

class Student(Person):
    """A class to represent a student, inheriting from Person."""

    def __init__(self, name, age, email, student_id):
        """Initialize a Student instance.

        Args:
            name (str): The name of the student.
            age (int): The age of the student, must be a positive integer.
            email (str): The email of the student, must be a valid email format.
            student_id (int or float): The unique identifier for the student, must be a positive number.

        Raises:
            ValueError: If the student ID is not a positive number.
        """
        super().__init__(name, age, email)

        # Validate student_id
        if not isinstance(student_id, (float, int)) or student_id <= 0:
            raise ValueError("Student ID must be a positive integer.")
        
        self.student_id = student_id
        self.registered_courses = []

    def register_course(self, course):
        """Register a course for the student.

        Args:
            course (Course): The Course object to be registered for the student.

        Prints:
            A message indicating whether the course was successfully registered or if it was already registered.
        """
        if not isinstance(course, Course):
            print("Invalid course. Please provide a Course object.")
            return
        
        if course in self.registered_courses:
            print(f"Course {course.course_name} is already registered.")
        else:
            self.registered_courses.append(course)
            print(f"Course {course.course_name} has been registered.")

    @classmethod
    def create_database(cls, db_name='school.db'):
        """Create the database and the student table if they do not exist.

        Args:
            db_name (str): The name of the database file. Defaults to 'school.db'.
        """
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        # Create the person table if it does not exist
        Person.create_database(db_name)
        # Create the student table with foreign key references to person table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS student (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER NOT NULL,
                email TEXT NOT NULL,
                student_id INTEGER NOT NULL UNIQUE,
                FOREIGN KEY (name, email) REFERENCES person (name, email) 
                ON DELETE CASCADE
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS registration (
                student_id INTEGER,
                course_id INTEGER,
                PRIMARY KEY (student_id, course_id),
                FOREIGN KEY (student_id) REFERENCES student (student_id) ON DELETE CASCADE,
                FOREIGN KEY (course_id) REFERENCES course (course_id) ON DELETE CASCADE
            )
        ''')
        conn.commit()
        conn.close()

    def save_to_db(self, db_name='school.db'):
        """Save the current student instance to the database.

        Args:
            db_name (str): The name of the database file. Defaults to 'school.db'.

        Prints:
            Error message if there is an IntegrityError during saving.
        """
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        # Insert the student into the table
        try:
            cursor.execute('''
                INSERT INTO student (name, age, email, student_id) 
                VALUES (?, ?, ?, ?)
            ''', (self.name, self.age, self._email, self.student_id))
            conn.commit()
        except sqlite3.IntegrityError as e:
            print(f"Error saving to database: {e}")
        finally:
            conn.close()

    @classmethod
    def show_all_records(cls, db_name='school.db'):
        """Display all records in the student table.

        Args:
            db_name (str): The name of the database file. Defaults to 'school.db'.
        """
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM student')
        rows = cursor.fetchall()
        conn.close()

        # Use PrettyTable to display the data in a tabular format
        table = PrettyTable()
        table.field_names = ["ID", "Name", "Age", "Email", "Student ID"]
        for row in rows:
            table.add_row(row)
        
        print(table)
