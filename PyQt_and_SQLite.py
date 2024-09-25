import sys
import json
import sqlite3
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLabel, QLineEdit, QPushButton, QComboBox, QRadioButton, QButtonGroup, QTableView,
    QTabWidget, QDialog, QDialogButtonBox, QMessageBox
)
from PyQt5.QtCore import Qt, QAbstractTableModel, QVariant
from PyQt5.QtGui import QColor
from student import Student
from instructor import Instructor
from course import Course
from person import Person
from data_manager import save_data, load_data


Person.create_database()
Student.create_database()
Instructor.create_database()
Course.create_database()

class RecordTableModel(QAbstractTableModel):
    """
    A custom table model that displays data using PyQt5's QAbstractTableModel.

    This class is designed to handle a list of records and display them in a table
    with headers. It overrides the basic methods for determining row/column counts
    and providing data to the table view.

    Attributes:
        records (list): A list of records, where each record is typically a list or tuple
            representing a row in the table.
        headers (list): A list of column headers for the table.
    """
    
    def __init__(self, records, headers, parent=None):
        """
        Initialize the table model with records and headers.

        Args:
            records (list): The data for the table, a list of rows, where each row is a list or tuple.
            headers (list): The column headers for the table.
            parent (QWidget, optional): The parent widget of the table model. Defaults to None.
        """
        super().__init__(parent)
        self.records = records
        self.headers = headers

    def rowCount(self, parent=None):
        """
        Return the number of rows in the table.

        Args:
            parent (QModelIndex, optional): The parent index, not used here. Defaults to None.

        Returns:
            int: The number of rows in the table, based on the number of records.
        """
        return len(self.records)

    def columnCount(self, parent=None):
        """
        Return the number of columns in the table.

        Args:
            parent (QModelIndex, optional): The parent index, not used here. Defaults to None.

        Returns:
            int: The number of columns in the table, based on the length of the headers list.
        """
        return len(self.headers)

    def data(self, index, role=Qt.DisplayRole):
        """
        Provide data for the given index and role.

        This method is called by the view to get the data to display.

        Args:
            index (QModelIndex): The index of the cell that needs data.
            role (Qt.ItemDataRole): The role for which data is requested (e.g., display role).

        Returns:
            QVariant: The data for the requested index and role, or an invalid QVariant if
            the index is invalid or the role is not supported.
        """
        if not index.isValid():
            return QVariant()

        record = self.records[index.row()]
        if role == Qt.DisplayRole:
            return QVariant(record[index.column()])
        return QVariant()

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        """
        Provide header data for the table, either for rows or columns.

        Args:
            section (int): The section (row or column) number for which header data is requested.
            orientation (Qt.Orientation): The orientation (horizontal or vertical) of the header.
            role (Qt.ItemDataRole): The role for which the header data is requested.

        Returns:
            QVariant: The header data for the requested section and role, or an invalid QVariant
            if the role or orientation is not supported.
        """
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return QVariant(self.headers[section])
        return QVariant()

class MainWindow(QMainWindow):
    """
    Main window class for the School Management System.

    This class provides the user interface (UI) for managing students, instructors,
    courses, registrations, and assignments within a school system. The window consists 
    of multiple tabs, each handling different aspects of the management system such as 
    adding students, instructors, courses, registering students to courses, and assigning 
    instructors to courses.

    Attributes:
        students (list): A list of student records (initially empty).
        instructors (list): A list of instructor records (initially empty).
        courses (list): A list of course records (initially empty).
    """
    def __init__(self):
        """
        Initializes the main window of the School Management System.
        
        Sets up the window's title, size, and initializes the user interface by creating
        tabs for different system operations.
        """
        super().__init__()
        self.setWindowTitle("School Management System")
        self.setGeometry(100, 100, 800, 800)
        
        self.students = []
        self.instructors = []
        self.courses = []

        self.initUI()

    def initUI(self):
        """
        Initializes the user interface by creating tabs for student, instructor, course 
        management, registration, assignment, and record viewing.
        
        This method sets up the main tab widget and calls methods to set up each tab's 
        individual layout and components.
        """
        # Create tabs
        tabs = QTabWidget()
        self.setCentralWidget(tabs)

        self.student_tab = QWidget()
        self.instructor_tab = QWidget()
        self.course_tab = QWidget()
        self.register_tab = QWidget()
        self.assign_tab = QWidget()
        self.view_tab = QWidget()

        tabs.addTab(self.student_tab, 'Student')
        tabs.addTab(self.instructor_tab, 'Instructor')
        tabs.addTab(self.course_tab, 'Course')
        tabs.addTab(self.register_tab, 'Register')
        tabs.addTab(self.assign_tab, 'Assign')
        tabs.addTab(self.view_tab, 'View Records')

        # Initialize UI components
        self.initStudentTab()
        self.initInstructorTab()
        self.initCourseTab()
        self.initRegisterTab()
        self.initAssignTab()
        self.initViewTab()

    def initStudentTab(self):
        """
        Initializes the UI layout and components for the 'Student' tab.
        
        The 'Student' tab allows users to add a student by entering their name, age, email, 
        and student ID, then clicking the "Add Student" button.
        """
        layout = QVBoxLayout()
        
        # Form Layout
        form_layout = QFormLayout()
        
        self.student_name_entry = QLineEdit()
        self.student_age_entry = QLineEdit()
        self.student_email_entry = QLineEdit()
        self.student_id_entry = QLineEdit()
        
        form_layout.addRow(QLabel("Student Name:"), self.student_name_entry)
        form_layout.addRow(QLabel("Age:"), self.student_age_entry)
        form_layout.addRow(QLabel("Email:"), self.student_email_entry)
        form_layout.addRow(QLabel("Student ID:"), self.student_id_entry)
        
        # Add Student Button
        add_student_button = QPushButton("Add Student")
        add_student_button.clicked.connect(self.add_student)
        
        # Add Button to Form Layout
        form_layout.addRow("", add_student_button)
        
        # Set Form Layout to Main Layout
        layout.addLayout(form_layout)
        
        self.student_tab.setLayout(layout)


    def initInstructorTab(self):
        """
        Initializes the UI layout and components for the 'Instructor' tab.
        
        The 'Instructor' tab allows users to add an instructor by entering their name, age, 
        email, and instructor ID, then clicking the "Add Instructor" button.
        """
        layout = QVBoxLayout()
        form_layout = QFormLayout()
        
        self.instructor_name_entry = QLineEdit()
        self.instructor_age_entry = QLineEdit()
        self.instructor_email_entry = QLineEdit()
        self.instructor_id_entry = QLineEdit()
        
        form_layout.addRow(QLabel("Instructor Name:"), self.instructor_name_entry)
        form_layout.addRow(QLabel("Age:"), self.instructor_age_entry)
        form_layout.addRow(QLabel("Email:"), self.instructor_email_entry)
        form_layout.addRow(QLabel("Instructor ID:"), self.instructor_id_entry)
        
        add_instructor_button = QPushButton("Add Instructor")
        add_instructor_button.clicked.connect(self.add_instructor)
        
        form_layout.addRow("", add_instructor_button)
        layout.addLayout(form_layout)
        layout.addWidget(add_instructor_button)
        self.instructor_tab.setLayout(layout)

    def initCourseTab(self):
        """
        Initializes the UI layout and components for the 'Course' tab.
        
        The 'Course' tab allows users to add a course by entering the course name, course ID,
        and selecting an instructor from a combo box, then clicking the "Add Course" button.
        """
        layout = QVBoxLayout()
        form_layout = QFormLayout()
        
        self.course_name_entry = QLineEdit()
        self.course_id_entry = QLineEdit()
        self.course_instructor_combo = QComboBox()
        
        form_layout.addRow(QLabel("Course Name:"), self.course_name_entry)
        form_layout.addRow(QLabel("Course ID:"), self.course_id_entry)
        form_layout.addRow(QLabel("Select Instructor:"), self.course_instructor_combo)
        
        add_course_button = QPushButton("Add Course")
        add_course_button.clicked.connect(self.add_course)
        form_layout.addRow("", add_course_button)
        layout.addLayout(form_layout)
        layout.addWidget(add_course_button)
        self.course_tab.setLayout(layout)

    def initRegisterTab(self):
        """
        Initializes the UI layout and components for the 'Register' tab.
        
        The 'Register' tab allows users to register students to courses by selecting a student
        and a course from combo boxes, then clicking the "Register" button.
        """
        layout = QVBoxLayout()
        form_layout = QFormLayout()
        
        self.student_combo = QComboBox()
        self.course_combo = QComboBox()
        
        form_layout.addRow(QLabel("Select Student:"), self.student_combo)
        form_layout.addRow(QLabel("Select Course:"), self.course_combo)
        
        register_button = QPushButton("Register")
        register_button.clicked.connect(self.register_student)
        form_layout.addRow("", register_button)
        layout.addLayout(form_layout)
        layout.addWidget(register_button)
        self.register_tab.setLayout(layout)

    def initAssignTab(self):
        """
        Initializes the UI layout and components for the 'Assign' tab.
        
        The 'Assign' tab allows users to assign instructors to courses by selecting an instructor
        and a course from combo boxes, then clicking the "Assign" button.
        """
        layout = QVBoxLayout()
        form_layout = QFormLayout()
        
        self.instructor_combo = QComboBox()
        self.course_combo_assign = QComboBox()
        
        form_layout.addRow(QLabel("Select Instructor:"), self.instructor_combo)
        form_layout.addRow(QLabel("Select Course:"), self.course_combo_assign)
        
        assign_button = QPushButton("Assign")
        assign_button.clicked.connect(self.assign_instructor)
        form_layout.addRow("", assign_button)
        layout.addLayout(form_layout)
        layout.addWidget(assign_button)
        self.assign_tab.setLayout(layout)

    def initViewTab(self):
        """
        Initializes the UI layout and components for the 'View Records' tab.
        
        The 'View Records' tab allows users to view and manage records, including saving and loading
        data, searching for specific records, and displaying them in a table view.
        """
        
        layout = QVBoxLayout()
        
        # Buttons
        button_layout = QHBoxLayout()
        save_button = QPushButton("Save Data")
        load_button = QPushButton("Load Data")
        save_button.clicked.connect(self.save_data_to_file)
        load_button.clicked.connect(self.load_data_from_file)
        button_layout.addWidget(save_button)
        button_layout.addWidget(load_button)
        
        # Search fields
        search_layout = QFormLayout()
        self.search_name_entry = QLineEdit()
        self.search_id_entry = QLineEdit()
        search_layout.addRow(QLabel("Search by Name:"), self.search_name_entry)
        search_layout.addRow(QLabel("Search by ID:"), self.search_id_entry)
        
        # Search options
        self.search_option_group = QButtonGroup()
        student_radio = QRadioButton("Student")
        instructor_radio = QRadioButton("Instructor")
        course_radio = QRadioButton("Course")
        self.search_option_group.addButton(student_radio, 1)
        self.search_option_group.addButton(instructor_radio, 2)
        self.search_option_group.addButton(course_radio, 3)
        
        search_layout.addRow(student_radio, instructor_radio)
        search_layout.addRow(course_radio)
        
        search_button = QPushButton("Search")
        search_button.clicked.connect(self.search_records)
        
        # TreeView
        self.tree_view = QTableView()
        self.update_treeview()
        
        layout.addLayout(button_layout)
        layout.addLayout(search_layout)
        layout.addWidget(search_button)
        layout.addWidget(self.tree_view)
        
        self.view_tab.setLayout(layout)

    def update_treeview(self):
        """
        Updates the data in the tree view for displaying records of students, instructors, and courses.
        
        This method fetches data from the SQLite database, formats it into a list, and sets it as the 
        data source for the table view in the 'View Records' tab.
        """
        headers = ["ID", "Name", "Type/Instructor"]
        records = []

        # Connect to the database
        conn = sqlite3.connect('school.db')
        cursor = conn.cursor()

        # Fetch students from the database
        cursor.execute("SELECT student_id, name FROM student")
        students = cursor.fetchall()
        for student in students:
            records.append([student[0], student[1], "Student"])

        # Fetch instructors from the database
        cursor.execute("SELECT instructor_id, name FROM instructor")
        instructors = cursor.fetchall()
        for instructor in instructors:
            records.append([instructor[0], instructor[1], "Instructor"])

        # Fetch courses from the database
        cursor.execute('''
            SELECT course.course_id, course.course_name, instructor.name
            FROM course
            LEFT JOIN instructor ON course.instructor_id = instructor.instructor_id
        ''')
        courses = cursor.fetchall()
        for course in courses:
            instructor_name = course[2] if course[2] is not None else "N/A"
            records.append([course[0], course[1], instructor_name])

        # Close the database connection
        conn.close()

        # Update the tree view
        self.model = RecordTableModel(records, headers)
        self.tree_view.setModel(self.model)

    def refresh_dropdowns(self):
        """
    Refreshes the dropdown menus for instructors, students, and courses.

    This method clears the current items in the instructor, student, and course-related
    dropdown menus (combo boxes), then fetches the latest data from the SQLite database to
    repopulate them. This ensures that the dropdowns are always up to date with the most
    recent entries in the 'instructor', 'student', and 'course' tables.

    The method performs the following operations:
        - Clears the existing items in the combo boxes.
        - Fetches instructor records and adds them to the appropriate instructor combo boxes.
        - Fetches student records and adds them to the student combo box.
        - Fetches course records and adds them to the course-related combo boxes.

    The combo boxes updated by this method are:
        - self.course_instructor_combo: Dropdown for selecting an instructor when adding a course.
        - self.student_combo: Dropdown for selecting a student when registering them for a course.
        - self.course_combo: Dropdown for selecting a course when registering a student.
        - self.instructor_combo: Dropdown for selecting an instructor when assigning them to a course.
        - self.course_combo_assign: Dropdown for selecting a course when assigning an instructor.

    Database:
        - Connects to the SQLite database 'school.db' to fetch the latest data from the 
          'instructor', 'student', and 'course' tables.

    Returns:
        None
    """
    # Clear existing items
        self.course_instructor_combo.clear()
        self.student_combo.clear()
        self.course_combo.clear()
        self.instructor_combo.clear()
        self.course_combo_assign.clear()

        # Connect to the database
        conn = sqlite3.connect('school.db')
        cursor = conn.cursor()

        # Fetch instructors and populate the instructor-related dropdowns
        cursor.execute("SELECT instructor_id, name FROM instructor")
        instructors = cursor.fetchall()
        for instructor in instructors:
            instructor_id, name = instructor
            # Add instructor name and ID to the combo boxes
            self.course_instructor_combo.addItem(name, instructor_id)
            self.instructor_combo.addItem(name, instructor_id)

        # Fetch students and populate the student dropdown
        cursor.execute("SELECT student_id, name FROM student")
        students = cursor.fetchall()
        for student in students:
            student_id, name = student
            # Add student name and ID to the combo box
            self.student_combo.addItem(name, student_id)

        # Fetch courses and populate the course-related dropdowns
        cursor.execute("SELECT course_id, course_name FROM course")
        courses = cursor.fetchall()
        for course in courses:
            course_id, course_name = course
            # Add course name and ID to the combo boxes
            self.course_combo.addItem(course_name, course_id)
            self.course_combo_assign.addItem(course_name, course_id)

        # Close the database connection
        conn.close()

    def add_student(self):
        """
    Adds a new student to the database and updates the UI.

    This method retrieves the student's name, age, email, and student ID from the UI entries,
    then inserts this information into the 'student' table in the SQLite database. After the
    student is successfully added, it updates the tree view and refreshes the dropdown menus.

    Input:
        - Name, age, email, and student ID are retrieved from the corresponding UI elements.

    Database:
        - Inserts a new student record into the 'student' table.

    Exceptions:
        - Shows an error message if any exceptions occur during the process, such as 
          invalid inputs or database connection issues.

    Returns:
        None
    """
        try:
            name = self.student_name_entry.text()
            age = int(self.student_age_entry.text())
            email = self.student_email_entry.text()
            student_id = int(self.student_id_entry.text())

            # Insert the student into the database
            conn = sqlite3.connect('school.db')
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO student (student_id, name, age, email)
                VALUES (?, ?, ?, ?)
            ''', (student_id, name, age, email))
            conn.commit()
            conn.close()

            # Update UI
            self.update_treeview()
            self.refresh_dropdowns()
        except Exception as e:
            self.show_error_message("Error adding student", str(e))

    def add_instructor(self):
        """
    Adds a new instructor to the database and updates the UI.

    This method retrieves the instructor's name, age, email, and instructor ID from the UI entries,
    then inserts this information into the 'instructor' table in the SQLite database. After the
    instructor is successfully added, it updates the tree view and refreshes the dropdown menus.

    Input:
        - Name, age, email, and instructor ID are retrieved from the corresponding UI elements.

    Database:
        - Inserts a new instructor record into the 'instructor' table.

    Exceptions:
        - Shows an error message if any exceptions occur during the process, such as 
          invalid inputs or database connection issues.

    Returns:
        None
    """
        try:
            name = self.instructor_name_entry.text()
            age = int(self.instructor_age_entry.text())
            email = self.instructor_email_entry.text()
            instructor_id = int(self.instructor_id_entry.text())

            # Insert the instructor into the database
            conn = sqlite3.connect('school.db')
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO instructor (instructor_id, name, age, email)
                VALUES (?, ?, ?, ?)
            ''', (instructor_id, name, age, email))
            conn.commit()
            conn.close()

            # Update UI
            self.update_treeview()
            self.refresh_dropdowns()
        except Exception as e:
            self.show_error_message("Error adding instructor", str(e))

    def add_course(self):
        """
    Adds a new course to the internal list and updates the UI.

    This method retrieves the course name, course ID, and selected instructor from the UI entries,
    creates a `Course` object, and adds it to the internal list of courses. It then updates the
    tree view and refreshes the dropdown menus.

    Input:
        - Course name and course ID are retrieved from the UI entries.
        - Instructor is retrieved from the course instructor dropdown (combo box).

    Exceptions:
        - Shows an error message if any exceptions occur during the process, such as 
          invalid inputs.

    Returns:
        None
    """
        try:
            course_name = self.course_name_entry.text()
            course_id = int(self.course_id_entry.text())
            instructor = self.course_instructor_combo.currentData()
            
            course = Course(course_id, course_name, instructor)
            self.courses.append(course)
            self.update_treeview()
            self.refresh_dropdowns()
        except Exception as e:
            self.show_error_message("Error adding course", str(e))

    def register_student(self):
        """
    Registers a student for a course by inserting a record into the registration table.

    This method retrieves the selected student and course IDs from the dropdown menus,
    then inserts the student and course pairing into the 'registration' table in the SQLite database.
    It then updates the tree view.

    Input:
        - Student ID and course ID are retrieved from the dropdown menus (combo boxes).

    Database:
        - Inserts a new record into the 'registration' table.

    Exceptions:
        - Shows an error message if any exceptions occur during the process, such as 
          database connection issues.

    Returns:
        None
    """
    
        try:
            student_id = self.student_combo.currentData()  # Assume this returns the student ID
            course_id = self.course_combo.currentData()  # Assume this returns the course ID

            if course_id and student_id:
                # Insert into the registration table
                conn = sqlite3.connect('school.db')
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO registration (student_id, course_id)
                    VALUES (?, ?)
                ''', (student_id, course_id))
                conn.commit()
                conn.close()

                # Update UI
                self.update_treeview()
        except Exception as e:
            self.show_error_message("Error registering student", str(e))

    def assign_instructor(self):
        """
    Assigns an instructor to a course by updating the course record in the database.

    This method retrieves the selected course and instructor IDs from the dropdown menus,
    then updates the instructor assignment in the 'course' table of the SQLite database.
    After the instructor is assigned, it updates the tree view.

    Input:
        - Course ID and instructor ID are retrieved from the dropdown menus (combo boxes).

    Database:
        - Updates the 'instructor_id' field for the course in the 'course' table.

    Exceptions:
        - Shows an error message if any exceptions occur during the process, such as 
          database connection issues.

    Returns:
        None
    """
        try:
            instructor_id = self.instructor_combo.currentData()  # Assume this returns the instructor ID
            course_id = self.course_combo_assign.currentData()  # Assume this returns the course ID

            if course_id and instructor_id:
                # Update the course in the database
                conn = sqlite3.connect('school.db')
                cursor = conn.cursor()
                cursor.execute('''
                    UPDATE course
                    SET instructor_id = ?
                    WHERE course_id = ?
                ''', (instructor_id, course_id))
                conn.commit()
                conn.close()

                # Update UI
                self.update_treeview()
        except Exception as e:
            self.show_error_message("Error assigning instructor", str(e))

    def search_records(self):
        """
    Searches for students, instructors, or courses in the database based on the input.

    This method retrieves search parameters from the UI, such as a name or ID, and the type
    of record (student, instructor, or course). It then queries the database for matching
    records and displays the results in the tree view.

    Input:
        - Search parameters (name and ID) are retrieved from the UI entries.
        - Search type is determined by the selected option (student, instructor, or course).

    Database:
        - Queries the relevant tables (student, instructor, course) and fetches records that match the criteria.

    Output:
        - Displays the search results in the tree view with columns "ID", "Name", and "Type/Instructor".

    Exceptions:
        - Shows an error message if any exceptions occur during the process, such as 
          database connection issues.

    Returns:
        None
    """
        try:
            search_name = self.search_name_entry.text()
            search_id = self.search_id_entry.text()
            search_type = self.search_option_group.checkedId()
            
            found_records = []
            conn = sqlite3.connect('school.db')
            cursor = conn.cursor()

            if search_type == 1:  # Student
                query = "SELECT student_id, name FROM student WHERE name LIKE ? OR student_id = ?"
                cursor.execute(query, ('%' + search_name + '%', search_id))
                students = cursor.fetchall()
                for student in students:
                    found_records.append([student[0], student[1], "Student"])
            
            elif search_type == 2:  # Instructor
                query = "SELECT instructor_id, name FROM instructor WHERE name LIKE ? OR instructor_id = ?"
                cursor.execute(query, ('%' + search_name + '%', search_id))
                instructors = cursor.fetchall()
                for instructor in instructors:
                    found_records.append([instructor[0], instructor[1], "Instructor"])

            elif search_type == 3:  # Course
                query = '''
                    SELECT course.course_id, course.course_name, instructor.name
                    FROM course
                    LEFT JOIN instructor ON course.instructor_id = instructor.instructor_id
                    WHERE course.course_name LIKE ? OR course.course_id = ?
                '''
                cursor.execute(query, ('%' + search_name + '%', search_id))
                courses = cursor.fetchall()
                for course in courses:
                    instructor_name = course[2] if course[2] else "N/A"
                    found_records.append([course[0], course[1], instructor_name])

            conn.close()
            
            # Update the tree view with search results
            self.model = RecordTableModel(found_records, ["ID", "Name", "Type/Instructor"])
            self.tree_view.setModel(self.model)
        except Exception as e:
            self.show_error_message("Error searching records", str(e))

    def save_data_to_file(self):
        """
    Saves all data (instructors, courses, students, and their relationships) from the SQLite database 
    to a JSON file.

    This method fetches all data from the 'instructor', 'course', 'student', and 'registration' tables
    in the SQLite database. It organizes the data into dictionaries for instructors, courses, and students.
    The relationships between students and courses, as well as instructors and courses, are also maintained
    in the output JSON file. Each entity is then saved to 'school_data.json'.

    Database:
        - Fetches data from the 'instructor', 'course', 'student', and 'registration' tables.

    Output:
        - A JSON file ('school_data.json') containing all the data and relationships.

    Exceptions:
        - Displays an error message using `show_error_message()` if any exceptions occur during the process, 
          such as issues with database connectivity or file writing.

    Returns:
        None
    """
        try:
            filename = "school_data.json"  # Set the filename to save
            
            # Fetch data from the database
            conn = sqlite3.connect('school.db')
            cursor = conn.cursor()

            # Fetch instructors
            cursor.execute("SELECT instructor_id, name, age, email FROM instructor")
            instructors = cursor.fetchall()
            instructor_list = []
            for inst in instructors:
                instructor_list.append({
                    "instructor_id": inst[0],
                    "name": inst[1],
                    "age": inst[2],
                    "_email": inst[3],  # Note: using '_email' to match the format in the JSON file
                    "assigned_courses": []  # Will populate this next
                })

            # Fetch courses and assign instructors to courses
            cursor.execute("SELECT course_id, course_name, instructor_id FROM course")
            courses = cursor.fetchall()
            course_list = []
            for course in courses:
                course_id, course_name, instructor_id = course
                course_list.append({
                    "course_id": course_id,
                    "course_name": course_name,
                    "instructor_id": instructor_id,
                    "enrolled_students": []
                })

                # Assign the course to the instructor's 'assigned_courses'
                for instructor in instructor_list:
                    if instructor["instructor_id"] == instructor_id:
                        instructor["assigned_courses"].append(course_id)

            # Fetch students and their registered courses
            cursor.execute("SELECT student_id, name, age, email FROM student")
            students = cursor.fetchall()
            student_list = []
            for stud in students:
                student_list.append({
                    "student_id": stud[0],
                    "name": stud[1],
                    "age": stud[2],
                    "_email": stud[3],  # Note: using '_email' to match the format in the JSON file
                    "registered_courses": []
                })

            # Fetch student-course registrations
            cursor.execute("SELECT student_id, course_id FROM registration")
            registrations = cursor.fetchall()
            for registration in registrations:
                student_id, course_id = registration
                # Add course to the student's 'registered_courses'
                for student in student_list:
                    if student["student_id"] == student_id:
                        student["registered_courses"].append(course_id)
                # Add student to the course's 'enrolled_students'
                for course in course_list:
                    if course["course_id"] == course_id:
                        course["enrolled_students"].append(student_id)

            conn.close()

            # Save to JSON
            data = {
                "instructors": instructor_list,
                "courses": course_list,
                "students": student_list
            }
            with open(filename, 'w') as json_file:
                json.dump(data, json_file, indent=4)

            self.show_info_message("Data saved successfully.")
        except Exception as e:
            self.show_error_message("Error saving data", str(e))

    def load_data_from_file(self):
        """
    Loads data from a JSON file into the SQLite database and updates the UI.

    This method reads the 'school_data.json' file, which contains instructors, courses, students, 
    and their relationships (such as registrations and course assignments). It inserts this data 
    into the 'instructor', 'course', 'student', and 'registration' tables in the SQLite database. 
    The UI elements such as the tree view and dropdowns are also updated with the loaded data.

    Input:
        - A JSON file ('school_data.json') containing instructors, courses, students, and relationships.

    Database:
        - Inserts data into the 'instructor', 'course', 'student', and 'registration' tables.

    UI:
        - Updates the tree view and dropdown menus to reflect the loaded data.

    Exceptions:
        - Displays an error message using `show_error_message()` if any exceptions occur during the process,
          such as issues with file reading or database insertion.

    Returns:
        None
    """
        try:
            filename = "school_data.json"  # Set the filename to load
            instructor_dict, student_dict, course_dict = load_data(filename)

            # Convert the dictionaries to lists
            instructors = list(instructor_dict.values())
            students = list(student_dict.values())
            courses = list(course_dict.values())

            # Insert data into the database
            conn = sqlite3.connect('school.db')
            cursor = conn.cursor()

            # Insert instructors
            for instructor in instructors:
                cursor.execute('''
                    INSERT OR IGNORE INTO instructor (instructor_id, name, age, email)
                    VALUES (?, ?, ?, ?)
                ''', (instructor['instructor_id'], instructor['name'], instructor['age'], instructor['_email']))

            # Insert courses
            for course in courses:
                cursor.execute('''
                    INSERT OR IGNORE INTO course (course_id, course_name, instructor_id)
                    VALUES (?, ?, ?)
                ''', (course['course_id'], course['course_name'], course['instructor_id']))

            # Insert students
            for student in students:
                cursor.execute('''
                    INSERT OR IGNORE INTO student (student_id, name, age, email)
                    VALUES (?, ?, ?, ?)
                ''', (student['student_id'], student['name'], student['age'], student['_email']))

            # Insert registrations (many-to-many relationships)
            for student in students:
                for course_id in student['registered_courses']:
                    cursor.execute('''
                        INSERT OR IGNORE INTO registration (student_id, course_id)
                        VALUES (?, ?)
                    ''', (student['student_id'], course_id))

            conn.commit()
            conn.close()

            # Update the UI
            self.update_treeview()  # Update the tree view to reflect the loaded data
            self.refresh_dropdowns()  # Refresh the dropdowns to show the loaded data

            self.show_info_message("Data loaded successfully.")
        except Exception as e:
            self.show_error_message("Error loading data", str(e))

    def show_error_message(self, title, message):
        """
    Displays a critical error message in a message box.

    This method is used to show an error message dialog with a specific title and message content
    when an exception or an error occurs during the program's execution.

    Input:
        - title (str): The title of the error message box.
        - message (str): The detailed error message to be displayed.

    Output:
        - A message box showing the error details.

    Returns:
        None
    """
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setText(message)
        msg_box.setWindowTitle(title)
        msg_box.exec_()

    def show_info_message(self, message):
        """
    Displays an informational message in a message box.

    This method is used to show a message dialog with a specified informational message content,
    typically when a process, such as data saving or loading, has completed successfully.

    Input:
        - message (str): The message content to be displayed.

    Output:
        - A message box showing the informational message.

    Returns:
        None
    """
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setText(message)
        msg_box.setWindowTitle("Info")
        msg_box.exec_()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
