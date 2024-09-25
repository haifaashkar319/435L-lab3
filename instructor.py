import sqlite3
from person import Person
from course import Course  # Ensure this is imported if needed
from prettytable import PrettyTable

class Instructor(Person):
    """A class to represent an instructor, inheriting from Person."""

    # Class-level attribute to keep track of all instructor IDs
    existing_instructor_ids = set()

    def __init__(self, name, age, email, instructor_id):
        """Initialize an Instructor instance.

        Args:
            name (str): The name of the instructor.
            age (int): The age of the instructor, must be a positive integer.
            email (str): The email of the instructor, must be a valid email format.
            instructor_id (int): The unique identifier for the instructor, must be a positive integer.

        Raises:
            ValueError: If the instructor ID is not a positive integer or is not unique.
        """
        super().__init__(name, age, email)

        # Validate instructor_id: Must be a number and unique
        if not isinstance(instructor_id, int) or instructor_id <= 0:
            raise ValueError("Instructor ID must be a positive integer.")
        
        if instructor_id in Instructor.existing_instructor_ids:
            raise ValueError("Instructor ID must be unique.")
        
        # If valid, add instructor_id to the set of existing IDs
        Instructor.existing_instructor_ids.add(instructor_id)

        self.instructor_id = instructor_id
        self.assigned_courses = []

    def assign_course(self, course):
        """Assign a course to the instructor.

        Args:
            course (Course): The Course object to be assigned to the instructor.

        Prints:
            A message indicating whether the course was successfully assigned or if it was already assigned.
        """
        if not isinstance(course, Course):
            print("Invalid course. Please provide a Course object.")
            return
        if course in self.assigned_courses:
            print(f"Course {course.course_name} is already assigned.")
        else:
            self.assigned_courses.append(course)
            print(f"Course {course.course_name} has been assigned.")

    @classmethod
    def create_database(cls, db_name='school.db'):
        """Create the database and the instructor table if they do not exist.

        Args:
            db_name (str): The name of the database file. Defaults to 'school.db'.
        """
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        # Create the person table if it does not exist
        Person.create_database(db_name)
        # Create the instructor table with foreign key references to person table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS instructor (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER NOT NULL,
                email TEXT NOT NULL,
                instructor_id INTEGER NOT NULL UNIQUE,
                FOREIGN KEY (name, email) REFERENCES person (name, email) 
                ON DELETE CASCADE
            )
        ''')
        conn.commit()
        conn.close()

    def save_to_db(self, db_name='school.db'):
        """Save the current instructor instance to the database.

        Args:
            db_name (str): The name of the database file. Defaults to 'school.db'.

        Prints:
            Error message if there is an IntegrityError during saving.
        """
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        # Insert the instructor into the table
        try:
            cursor.execute('''
                INSERT INTO instructor (name, age, email, instructor_id) 
                VALUES (?, ?, ?, ?)
            ''', (self.name, self.age, self._email, self.instructor_id))
            conn.commit()
        except sqlite3.IntegrityError as e:
            print(f"Error saving to database: {e}")
        finally:
            conn.close()

    @classmethod
    def show_all_records(cls, db_name='school.db'):
        """Display all records in the instructor table.

        Args:
            db_name (str): The name of the database file. Defaults to 'school.db'.
        """
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM instructor')
        rows = cursor.fetchall()
        conn.close()

        # Use PrettyTable to display the data in a tabular format
        table = PrettyTable()
        table.field_names = ["ID", "Name", "Age", "Email", "Instructor ID"]
        for row in rows:
            table.add_row(row)
        
        print(table)
