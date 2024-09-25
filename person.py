import sqlite3
import re
from prettytable import PrettyTable

class Person:
    """A class to represent a person with name, age, and email."""

    def __init__(self, name, age, email):
        """Initialize a Person instance.

        Args:
            name (str): The name of the person.
            age (int): The age of the person, must be a positive integer.
            email (str): The email of the person, must be a valid email format.

        Raises:
            ValueError: If the name is invalid, age is not a positive integer,
                        or email format is invalid.
        """
        # Validate name
        if not self.validate_name(name):
            raise ValueError(f"Invalid name: '{name}'. Name should contain only alphabetic characters and spaces.")
        
        # Validate age
        if not isinstance(age, int) or age <= 0:
            raise ValueError("Age must be a positive integer.")
        
        # Validate email
        if not self.validate_email(email):
            raise ValueError(f"Invalid email format: '{email}'.")

        self.name = name
        self.age = age
        self._email = email

    def introduce(self):
        """Introduce the person by name and age."""
        print(f"Hello, my name is {self.name} and my age is {self.age}.")

    @staticmethod
    def validate_name(name):
        """Validate the name.

        Args:
            name (str): The name to validate.

        Returns:
            bool: True if the name is valid, otherwise False.
        """
        # Name validation: should contain only alphabets and spaces
        pattern = r'^[A-Za-z\s]+$'
        return re.match(pattern, name) is not None

    @staticmethod
    def validate_email(email):
        """Validate the email format.

        Args:
            email (str): The email to validate.

        Returns:
            bool: True if the email format is valid, otherwise False.
        """
        # Basic email validation using regex
        pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return re.match(pattern, email) is not None

    @classmethod
    def create_database(cls, db_name='school.db'):
        """Create the database and the person table if they do not exist.

        Args:
            db_name (str): The name of the database file. Defaults to 'school.db'.
        """
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        # Create the person table
        cursor.execute(''' 
            CREATE TABLE IF NOT EXISTS person (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER NOT NULL,
                email TEXT NOT NULL UNIQUE
            )
        ''')
        conn.commit()
        conn.close()

    def save_to_db(self, db_name='school.db'):
        """Save the current person instance to the database.

        Args:
            db_name (str): The name of the database file. Defaults to 'school.db'.
        
        Prints:
            Error message if there is an IntegrityError during saving.
        """
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        # Insert the person into the table
        try:
            cursor.execute(''' 
                INSERT INTO person (name, age, email) 
                VALUES (?, ?, ?)
            ''', (self.name, self.age, self._email))
            conn.commit()
        except sqlite3.IntegrityError as e:
            print(f"Error saving to database: {e}")
        finally:
            conn.close()

    @classmethod
    def show_all_records(cls, db_name='school.db'):
        """Display all records in the person table.

        Args:
            db_name (str): The name of the database file. Defaults to 'school.db'.
        """
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM person')
        rows = cursor.fetchall()
        conn.close()

        # Use PrettyTable to display the data in a tabular format
        table = PrettyTable()
        table.field_names = ["ID", "Name", "Age", "Email"]
        for row in rows:
            table.add_row(row)
        
        print(table)
