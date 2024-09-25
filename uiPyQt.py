import sys
import json
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
from data_manager import save_data, load_data

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
        for student in self.students:
            records.append([student.student_id, student.name, "Student"])
        for instructor in self.instructors:
            records.append([instructor.instructor_id, instructor.name, "Instructor"])
        for course in self.courses:
            instructor_name = course.instructor.name if course.instructor else "N/A"
            records.append([course.course_id, course.course_name, instructor_name])
        
        self.model = RecordTableModel(records, headers)
        self.tree_view.setModel(self.model)

    def refresh_dropdowns(self):
        self.course_instructor_combo.clear()
        self.student_combo.clear()
        self.course_combo.clear()
        self.instructor_combo.clear()
        self.course_combo_assign.clear()
        
        for instructor in self.instructors:
            self.course_instructor_combo.addItem(instructor.name, instructor)
            self.instructor_combo.addItem(instructor.name, instructor)
        
        for student in self.students:
            self.student_combo.addItem(student.name, student)
        
        for course in self.courses:
            self.course_combo.addItem(course.course_name, course)
            self.course_combo_assign.addItem(course.course_name, course)

    def add_student(self):
        try:
            name = self.student_name_entry.text()
            age = int(self.student_age_entry.text())
            print (age)
            email = self.student_email_entry.text()
            student_id = int(self.student_id_entry.text())
            
            student = Student(name, age, email, student_id)
            self.students.append(student)
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
            
            instructor = Instructor(name, age, email, instructor_id)
            self.instructors.append(instructor)
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
            student = self.student_combo.currentData()
            course = self.course_combo.currentData()
            
            if course and student:
                course.add_student(student)
                self.update_treeview()
        except Exception as e:
            self.show_error_message("Error registering student", str(e))

    def assign_instructor(self):
        try:
            instructor = self.instructor_combo.currentData()
            course = self.course_combo_assign.currentData()
            
            if course and instructor:
                course.assign_instructor(instructor)
                self.update_treeview()
        except Exception as e:
            self.show_error_message("Error assigning instructor", str(e))

    def search_records(self):
        try:
            search_name = self.search_name_entry.text()
            search_id = self.search_id_entry.text()
            search_type = self.search_option_group.checkedId()
            
            found_records = []
            
            if search_type == 1:  # Student
                for student in self.students:
                    if search_name.lower() in student.name.lower() or search_id == student.student_id:
                        found_records.append([student.student_id, student.name, "Student"])
            elif search_type == 2:  # Instructor
                for instructor in self.instructors:
                    if search_name.lower() in instructor.name.lower() or search_id == instructor.instructor_id:
                        found_records.append([instructor.instructor_id, instructor.name, "Instructor"])
            elif search_type == 3:  # Course
                for course in self.courses:
                    if search_name.lower() in course.course_name.lower() or search_id == course.course_id:
                        instructor_name = course.instructor.name if course.instructor else "N/A"
                        found_records.append([course.course_id, course.course_name, instructor_name])
            
            self.model = RecordTableModel(found_records, ["ID", "Name", "Type/Instructor"])
            self.tree_view.setModel(self.model)
        except Exception as e:
            self.show_error_message("Error searching records", str(e))

    def save_data_to_file(self):
        try:
            filename = "school_data.json"  # Set the filename to save
            save_data(filename, self.instructors, self.students, self.courses)
            self.show_info_message("Data saved successfully.")
        except Exception as e:
            self.show_error_message("Error saving data", str(e))

    def load_data_from_file(self):
        try:
            filename = "school_data.json"  # Set the filename to load
            instructor_dict, student_dict, course_dict = load_data(filename)

            # Convert the dictionaries to lists and store them in the instance attributes
            self.instructors = list(instructor_dict.values())
            self.students = list(student_dict.values())
            self.courses = list(course_dict.values())

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
