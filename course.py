import sqlite3

class Course:
    def __init__(self, course_id, course_name, instructor=None):
        # Validate course_id: Must be a positive integer
        if not isinstance(course_id, int) or course_id <= 0:
            raise ValueError("course_id must be a positive integer.")
        
        # Validate course_name: Must contain only letters
        if not course_name.isalpha():
            raise ValueError("course_name must contain only letters.")
        
        self.course_id = course_id
        self.course_name = course_name
        self.instructor = None
        
        if instructor is not None:
            self.set_instructor(instructor)
    
    def set_instructor(self, instructor):
        from instructor import Instructor  # Import here to avoid circular import issues
        
        if not isinstance(instructor, Instructor):
            raise TypeError(f"Instructor must be an instance of Instructor or None, got {type(instructor).__name__}")
        
        self.instructor = instructor
        # Save instructor_id in the database
        self.save_to_db()
    
    def add_student(self, student):
        from student import Student  # Import here to avoid circular import issues
        
        if not isinstance(student, Student):
            print("Invalid student. Please provide a Student object.")
            return
        
        conn = sqlite3.connect('school.db')
        cursor = conn.cursor()
        
        try:
            # Insert student into the registration table
            cursor.execute('''
                INSERT OR IGNORE INTO registration (student_id, course_id)
                VALUES (?, ?)
            ''', (student.student_id, self.course_id))
            
            conn.commit()
            print(f"Student {student.name} has been enrolled in {self.course_name}.")
        except sqlite3.IntegrityError as e:
            print(f"Error enrolling student: {e}")
        finally:
            conn.close()
    
    @classmethod
    def create_database(cls, db_name='school.db'):
        """Create the database and the course table if they do not exist."""
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        
        # Create the course table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS course (
                course_id INTEGER PRIMARY KEY,
                course_name TEXT NOT NULL,
                instructor_id INTEGER,
                FOREIGN KEY (instructor_id) REFERENCES instructor (instructor_id)
                ON DELETE SET NULL
            )
        ''')
        
        # Create the registration table if not exists
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
        """Save the current course instance to the database."""
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT OR REPLACE INTO course (course_id, course_name, instructor_id) 
                VALUES (?, ?, ?)
            ''', (self.course_id, self.course_name, self.instructor.instructor_id if self.instructor else None))
            conn.commit()
        except sqlite3.IntegrityError as e:
            print(f"Error saving to database: {e}")
        finally:
            conn.close()
    
    @classmethod
    def show_all_records(cls, db_name='school.db'):
        """Display all records in the course table."""
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM course')
        rows = cursor.fetchall()
        conn.close()

        from prettytable import PrettyTable
        table = PrettyTable()
        table.field_names = ["Course ID", "Course Name", "Instructor ID"]
        for row in rows:
            table.add_row(row)
        
        print(table)
