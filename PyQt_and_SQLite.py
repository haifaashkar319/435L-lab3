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
    def __init__(self, records, headers, parent=None):
        super().__init__(parent)
        self.records = records
        self.headers = headers

    def rowCount(self, parent=None):
        return len(self.records)

    def columnCount(self, parent=None):
        return len(self.headers)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return QVariant()

        record = self.records[index.row()]
        if role == Qt.DisplayRole:
            return QVariant(record[index.column()])
        return QVariant()

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return QVariant(self.headers[section])
        return QVariant()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("School Management System")
        self.setGeometry(100, 100, 800, 800)
        
        self.students = []
        self.instructors = []
        self.courses = []

        self.initUI()

    def initUI(self):
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
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setText(message)
        msg_box.setWindowTitle(title)
        msg_box.exec_()

    def show_info_message(self, message):
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
