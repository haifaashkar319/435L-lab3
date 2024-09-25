import tkinter as tk
import sqlite3
from tkinter import ttk, messagebox
from student import Student
from instructor import Instructor
from course import Course
from person import Person
from data_manager import save_data, load_data

# Data storage
Person.create_database()
Student.create_database()
Instructor.create_database()
Course.create_database()

def add_student():
    """
    Adds a student to the database using the information provided in the input fields.

    Retrieves student details from input fields, validates them, and inserts a new student record 
    into the database. Displays a success message upon completion or an error message if validation 
    or database errors occur.
    """
    student_name = student_name_entry.get()
    student_age = student_age_entry.get()
    student_email = student_email_entry.get()
    student_id = student_id_entry.get()

    if student_name and student_age and student_email and student_id:
        try:
            student_age = int(student_age)
            student_id = int(student_id)
            if not Student.validate_name(student_name):
                raise ValueError("Invalid name format.")
            if not Student.validate_email(student_email):
                raise ValueError("Invalid email format.")
            
            conn = sqlite3.connect('school.db')
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO student (name, age, email, student_id) 
                VALUES (?, ?, ?, ?)
            ''', (student_name, student_age, student_email, student_id))
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Success", f"Student {student_name} added.")
            update_treeview()
            refresh_dropdowns()
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except sqlite3.IntegrityError as e:
            messagebox.showerror("Error", f"Database error: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")
    else:
        messagebox.showerror("Error", "Please fill out all fields.")

def add_instructor():
    """
    Adds an instructor to the database using the information provided in the input fields.

    Retrieves instructor details from input fields, validates them, and inserts a new instructor record 
    into the database. Displays a success message upon completion or an error message if validation 
    or database errors occur.
    """
    instructor_name = instructor_name_entry.get()
    instructor_age = instructor_age_entry.get()
    instructor_email = instructor_email_entry.get()
    instructor_id = instructor_id_entry.get()

    if instructor_name and instructor_age and instructor_email and instructor_id:
        try:
            instructor_age = int(instructor_age)
            instructor_id = int(instructor_id)
            if not Instructor.validate_name(instructor_name):
                raise ValueError("Invalid name format.")
            if not Instructor.validate_email(instructor_email):
                raise ValueError("Invalid email format.")
            
            conn = sqlite3.connect('school.db')
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO instructor (name, age, email, instructor_id) 
                VALUES (?, ?, ?, ?)
            ''', (instructor_name, instructor_age, instructor_email, instructor_id))
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Success", f"Instructor {instructor_name} added.")
            update_treeview()
            refresh_dropdowns()
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except sqlite3.IntegrityError as e:
            messagebox.showerror("Error", f"Database error: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")
    else:
        messagebox.showerror("Error", "Please fill out all fields.")

def add_course():
    """
    Adds a course to the database using the information provided in the input fields.

    Retrieves course details from input fields, validates them, and inserts a new course record 
    into the database. Displays a success message upon completion or an error message if validation 
    or database errors occur.
    """
    course_name = course_name_entry.get()
    course_id = course_id_entry.get()
    instructor_text = course_instructor_combo.get()

    if course_name and course_id:
        try:
            course_id = int(course_id)
            
            instructor_id = None
            if instructor_text and instructor_text != "None":
                instructor_id = int(instructor_text.split('(')[-1].strip(')'))

                conn = sqlite3.connect('school.db')
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM instructor WHERE instructor_id = ?', (instructor_id,))
                instructor = cursor.fetchone()
                conn.close()

                if instructor is None:
                    raise ValueError("Instructor not found")

            conn = sqlite3.connect('school.db')
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO course (course_id, course_name, instructor_id) 
                VALUES (?, ?, ?)
            ''', (course_id, course_name, instructor_id))
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Success", f"Course {course_name} added.")
            update_treeview()
            refresh_dropdowns()
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except sqlite3.IntegrityError as e:
            messagebox.showerror("Error", f"Database error: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")
    else:
        messagebox.showerror("Error", "Please fill out all fields.")

def register_student():
    """
    Registers a student to a course based on selections from dropdowns.

    Extracts student and course IDs from the dropdown selections, checks their existence in the database, 
    and registers the student for the selected course. Displays success or error messages based on the outcome.
    """
    student_text = student_combo.get()
    course_text = course_combo.get()

    if student_text and course_text:
        try:
            student_id = int(student_text.split('(')[-1].strip(')'))
            course_id = int(course_text.split('(')[-1].strip(')'))

            conn = sqlite3.connect('school.db')
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM student WHERE student_id = ?', (student_id,))
            student = cursor.fetchone()

            cursor.execute('SELECT * FROM course WHERE course_id = ?', (course_id,))
            course = cursor.fetchone()

            if student is None or course is None:
                raise ValueError("Student or course not found")

            cursor.execute('''
                INSERT INTO registration (student_id, course_id) 
                VALUES (?, ?)
            ''', (student_id, course_id))
            conn.commit()
            conn.close()

            messagebox.showinfo("Success", f"Student {student_text} registered to course {course_text}.")
            update_treeview()
            refresh_dropdowns()
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except sqlite3.IntegrityError as e:
            messagebox.showerror("Error", f"Database error: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"Unexpected error: {str(e)}")
    else:
        messagebox.showerror("Error", "Please select both student and course.")

def assign_instructor():
    """
    Assigns an instructor to a course based on selections from dropdowns.

    Extracts instructor and course IDs from the dropdown selections, checks their existence in the database, 
    and assigns the instructor to the selected course. Displays success or error messages based on the outcome.
    """
    instructor_text = instructor_combo.get()
    course_text = course_combo_assign.get()

    if instructor_text and course_text:
        try:
            instructor_id = int(instructor_text.split('(')[-1].strip(')'))
            course_id = int(course_text.split('(')[-1].strip(')'))

            conn = sqlite3.connect('school.db')
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM instructor WHERE instructor_id = ?', (instructor_id,))
            instructor = cursor.fetchone()

            cursor.execute('SELECT * FROM course WHERE course_id = ?', (course_id,))
            course = cursor.fetchone()

            if instructor is None or course is None:
                raise ValueError("Instructor or course not found")

            cursor.execute('''
                UPDATE course 
                SET instructor_id = ? 
                WHERE course_id = ?
            ''', (instructor_id, course_id))
            conn.commit()
            conn.close()

            messagebox.showinfo("Success", f"Instructor {instructor_text} assigned to course {course_text}.")
            update_treeview()
            refresh_dropdowns()
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except sqlite3.IntegrityError as e:
            messagebox.showerror("Error", f"Database error: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"Unexpected error: {str(e)}")
    else:
        messagebox.showerror("Error", "Invalid instructor or course selection.")

def refresh_dropdowns():
    """
    Refreshes the dropdown menus with the latest data from the database.

    Populates student, instructor, and course dropdowns with current records from the database.
    """
    conn = sqlite3.connect('school.db')
    cursor = conn.cursor()
    cursor.execute('SELECT name, student_id FROM student')
    students = cursor.fetchall()
    student_combo['values'] = [f"{name} ({student_id})" for name, student_id in students]

    cursor.execute('SELECT name, instructor_id FROM instructor')
    instructors = cursor.fetchall()
    instructor_combo['values'] = [f"{name} ({instructor_id})" for name, instructor_id in instructors]

    cursor.execute('SELECT course_name, course_id FROM course')
    courses = cursor.fetchall()
    course_combo['values'] = [f"{course_name} ({course_id})" for course_name, course_id in courses]
    course_combo_assign['values'] = [f"{course_name} ({course_id})" for course_name, course_id in courses]
    
    conn.close()

def update_treeview():
    """
    Updates the treeview with the latest records from the database.

    Clears the current treeview data and repopulates it with updated records for students, instructors, and courses.
    """
    for i in tree.get_children():
        tree.delete(i)

    conn = sqlite3.connect('school.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT s.name, s.age, s.email, s.student_id, c.course_name, i.name
        FROM registration r
        JOIN student s ON r.student_id = s.student_id
        JOIN course c ON r.course_id = c.course_id
        JOIN instructor i ON c.instructor_id = i.instructor_id
    ''')
    records = cursor.fetchall()
    conn.close()

    for record in records:
        tree.insert('', 'end', values=record)

def edit_record():
    """
    Edit the selected record in the Treeview.

    Retrieves the selected record's data, opens an edit window,
    and allows the user to modify the record. Upon saving, updates
    the record in the database.
    """
    selected_item = tree.selection()

    if not selected_item:
        messagebox.showerror("Error", "No record selected.")
        return

    # Retrieve the record's data
    selected_id = tree.item(selected_item, 'values')[3]  # Assuming "ID" is at index 3
    record_type = search_option.get()

    conn = sqlite3.connect('school.db')
    cursor = conn.cursor()

    # Fetch the record based on the type
    if record_type == "Student":
        cursor.execute('SELECT * FROM student WHERE student_id = ?', (selected_id,))
    elif record_type == "Instructor":
        cursor.execute('SELECT * FROM instructor WHERE instructor_id = ?', (selected_id,))
    elif record_type == "Course":
        cursor.execute('SELECT * FROM course WHERE course_id = ?', (selected_id,))
    else:
        messagebox.showerror("Error", "Invalid record type.")
        conn.close()
        return

    record = cursor.fetchone()
    if record:
        # Open a new window for editing the record
        edit_window = tk.Toplevel(root)
        edit_window.title("Edit Record")

        # Set up fields for editing
        tk.Label(edit_window, text="Name:").pack(pady=5)
        name_entry = tk.Entry(edit_window)
        name_entry.pack(pady=5)
        name_entry.insert(0, record[1])  # Pre-fill with current value

        tk.Label(edit_window, text="Age:").pack(pady=5)
        age_entry = tk.Entry(edit_window)
        age_entry.pack(pady=5)
        age_entry.insert(0, record[2])  # Pre-fill with current value

        tk.Label(edit_window, text="Email:").pack(pady=5)
        email_entry = tk.Entry(edit_window)
        email_entry.pack(pady=5)
        email_entry.insert(0, record[3])  # Pre-fill with current value

        # Set up fields based on record type
        id_label = tk.Label(edit_window, text=f"{record_type} ID:")
        id_label.pack(pady=5)
        id_entry = tk.Entry(edit_window)
        id_entry.pack(pady=5)
        id_entry.insert(0, record[0])  # Pre-fill with current value

        # Function to save changes
        def save_changes():
            try:
                name = name_entry.get()
                age = int(age_entry.get())
                email = email_entry.get()
                id_value = int(id_entry.get())

                # Update record based on type
                if record_type == "Student":
                    cursor.execute('''
                        UPDATE student
                        SET name = ?, age = ?, email = ?
                        WHERE student_id = ?
                    ''', (name, age, email, id_value))
                elif record_type == "Instructor":
                    cursor.execute('''
                        UPDATE instructor
                        SET name = ?, age = ?, email = ?
                        WHERE instructor_id = ?
                    ''', (name, age, email, id_value))
                elif record_type == "Course":
                    cursor.execute('''
                        UPDATE course
                        SET course_name = ?
                        WHERE course_id = ?
                    ''', (name, id_value))

                conn.commit()
                edit_window.destroy()
                update_treeview()
                messagebox.showinfo("Success", "Record updated successfully.")
            except ValueError as e:
                messagebox.showerror("Error", "Invalid input. Please check your entries.")

        tk.Button(edit_window, text="Save Changes", command=save_changes).pack(pady=10)
    else:
        messagebox.showerror("Error", "Record not found.")

    conn.close()


def delete_record():
    """
    Delete the selected record from the database.

    Removes the selected record based on the type from the database 
    and updates the Treeview to reflect changes.
    """
    selected_item = tree.selection()

    if not selected_item:
        messagebox.showerror("Error", "No record selected.")
        return

    selected_id = tree.item(selected_item, 'values')[3]  # Assuming "ID" is at index 3
    record_type = search_option.get()

    conn = sqlite3.connect('school.db')
    cursor = conn.cursor()

    try:
        if record_type == "Student":
            cursor.execute('DELETE FROM student WHERE student_id = ?', (selected_id,))
        elif record_type == "Instructor":
            cursor.execute('DELETE FROM instructor WHERE instructor_id = ?', (selected_id,))
        elif record_type == "Course":
            cursor.execute('DELETE FROM course WHERE course_id = ?', (selected_id,))
        else:
            messagebox.showerror("Error", "Invalid record type.")
            conn.close()
            return

        conn.commit()
        update_treeview()
        messagebox.showinfo("Success", "Record deleted successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"Unexpected error: {str(e)}")
    finally:
        conn.close()

import json
import sqlite3

def save_data_to_file():
    """
    Saves the student, instructor, and course data from the database to a JSON file.

    This function connects to the SQLite database, retrieves data from the 
    student, instructor, and course tables, organizes it into a dictionary, 
    and then writes the dictionary to a JSON file named 'school_data.json'.
    If the data is saved successfully, a success message is displayed. 
    If an error occurs during the process, an error message is shown.

    Returns:
        None
    """
    try:
        # Set the filename to save
        filename = "school_data.json"
        data = {
            "students": [],
            "instructors": [],
            "courses": []
        }

        # Connect to the database
        conn = sqlite3.connect('school.db')
        cursor = conn.cursor()

        # Fetch students
        cursor.execute("SELECT * FROM student")
        students = cursor.fetchall()
        data["students"] = [{"student_id": row[0], "name": row[1], "age": row[2], "email": row[3]} for row in students]

        # Fetch instructors
        cursor.execute("SELECT * FROM instructor")
        instructors = cursor.fetchall()
        data["instructors"] = [{"instructor_id": row[0], "name": row[1], "age": row[2], "email": row[3]} for row in instructors]

        # Fetch courses
        cursor.execute("SELECT * FROM course")
        courses = cursor.fetchall()
        data["courses"] = [{"course_id": row[0], "course_name": row[1], "instructor_id": row[2]} for row in courses]

        # Save data to JSON file
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)

        conn.close()
        messagebox.showinfo("Success", "Data saved to JSON successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"Error saving data to JSON: {str(e)}")

def load_data_from_file():
    """
    Loads student, instructor, and course data from a JSON file into the database.

    This function reads the data from a JSON file named 'school_data.json', 
    and for each record in the students, instructors, and courses sections, 
    it inserts the data into the corresponding tables in the SQLite database 
    if the record does not already exist. After loading the data, it updates 
    the UI components accordingly. If the data is loaded successfully, a 
    success message is displayed. If an error occurs during the process, 
    an error message is shown.

    Returns:
        None
    """
    
    global students, instructors, courses
    try:
        # Set the filename to load
        filename = "school_data.json"
        
        # Load data from the JSON file
        with open(filename, 'r') as f:
            data = json.load(f)

        conn = sqlite3.connect('school.db')
        cursor = conn.cursor()

        # Insert students into the database if they don't already exist
        for student in data["students"]:
            cursor.execute('''
                INSERT INTO student (student_id, name, age, email)
                SELECT ?, ?, ?, ?
                WHERE NOT EXISTS (SELECT 1 FROM student WHERE student_id = ?)
            ''', (student["student_id"], student["name"], student["age"], student["_email"], student["student_id"]))

        # Insert instructors into the database if they don't already exist
        for instructor in data["instructors"]:
            cursor.execute('''
                INSERT INTO instructor (instructor_id, name, age, email)
                SELECT ?, ?, ?, ?
                WHERE NOT EXISTS (SELECT 1 FROM instructor WHERE instructor_id = ?)
            ''', (instructor["instructor_id"], instructor["name"], instructor["age"], instructor["_email"], instructor["instructor_id"]))

        # Insert courses into the database if they don't already exist
        for course in data["courses"]:
            cursor.execute('''
                INSERT INTO course (course_id, course_name, instructor_id)
                SELECT ?, ?, ?
                WHERE NOT EXISTS (SELECT 1 FROM course WHERE course_id = ?)
            ''', (course["course_id"], course["course_name"], course["instructor_id"], course["course_id"]))

        conn.commit()
        conn.close()

        # Update the UI
        update_treeview()
        refresh_dropdowns()
        messagebox.showinfo("Success", "Data loaded from JSON and added to the database successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"Error loading data from JSON: {str(e)}")

def search_records():
    """
    Searches for records in the database based on the user's input.

    This function retrieves the user's search queries for name and ID, 
    clears the current contents of the treeview, and performs a search 
    in the database based on the selected record type (Student, Instructor, 
    or Course). It constructs the appropriate SQL query with filters for 
    name and ID, executes the query, and populates the treeview with the 
    results. If an error occurs during the search process, an error message 
    is displayed.

    Returns:
        None
    """
    name_query = search_name_entry.get().strip().lower()
    id_query = search_id_entry.get().strip().lower()
    search_type = search_option.get()

    # Clear the treeview
    for item in tree.get_children():
        tree.delete(item)

    try:
        conn = sqlite3.connect('school.db')
        cursor = conn.cursor()

        # Search Students
        if search_type == "Student":
            query = "SELECT student_id, name FROM student WHERE 1=1"
            params = []

            # Add filters for name and ID
            if name_query:
                query += " AND LOWER(name) LIKE ?"
                params.append(f"%{name_query}%")
            if id_query:
                query += " AND student_id LIKE ?"
                params.append(f"%{id_query}%")
            
            cursor.execute(query, params)
            students = cursor.fetchall()
            for student in students:
                tree.insert("", "end", values=(student[0], student[1], "Student"))

        # Search Instructors
        elif search_type == "Instructor":
            query = "SELECT instructor_id, name FROM instructor WHERE 1=1"
            params = []

            # Add filters for name and ID
            if name_query:
                query += " AND LOWER(name) LIKE ?"
                params.append(f"%{name_query}%")
            if id_query:
                query += " AND instructor_id LIKE ?"
                params.append(f"%{id_query}%")
            
            cursor.execute(query, params)
            instructors = cursor.fetchall()
            for instructor in instructors:
                tree.insert("", "end", values=(instructor[0], instructor[1], "Instructor"))

        # Search Courses
        elif search_type == "Course":
            query = """
            SELECT course.course_id, course.course_name, instructor.name
            FROM course
            LEFT JOIN instructor ON course.instructor_id = instructor.instructor_id
            WHERE 1=1
            """
            params = []

            # Add filters for name and ID
            if name_query:
                query += " AND LOWER(course.course_name) LIKE ?"
                params.append(f"%{name_query}%")
            if id_query:
                query += " AND course.course_id LIKE ?"
                params.append(f"%{id_query}%")
            
            cursor.execute(query, params)
            courses = cursor.fetchall()
            for course in courses:
                instructor_name = course[2] if course[2] else "N/A"
                tree.insert("", "end", values=(course[0], course[1], instructor_name))
        else:
            messagebox.showerror("Error", "Invalid search type selected.")
        
        conn.close()
    except Exception as e:
        messagebox.showerror("Error", f"Error searching records: {str(e)}")

# Create the main window
root = tk.Tk()
root.title("School Management System")
root.geometry("900x900")
# Styling variables


# Create tabs
notebook = ttk.Notebook(root)
notebook.pack(pady=10, expand=True)

# Create frames for each tab
student_frame = ttk.Frame(notebook, width=800, height=600)
instructor_frame = ttk.Frame(notebook, width=800, height=600)
course_frame = ttk.Frame(notebook, width=800, height=600)
register_frame = ttk.Frame(notebook, width=800, height=600)
assign_frame = ttk.Frame(notebook, width=800, height=600)
view_frame = ttk.Frame(notebook, width=800, height=600)

student_frame.pack(fill='both', expand=True, pady=20)
instructor_frame.pack(fill='both', expand=True, pady=20)
course_frame.pack(fill='both', expand=True, pady=20)
register_frame.pack(fill='both', expand=True, pady=20)
assign_frame.pack(fill='both', expand=True, pady=20)
view_frame.pack(fill='both', expand=True, pady=20)

# Add tabs to the notebook
notebook.add(student_frame, text='Student')
notebook.add(instructor_frame, text='Instructor')
notebook.add(course_frame, text='Course')
notebook.add(register_frame, text='Register')
notebook.add(assign_frame, text='Assign')
notebook.add(view_frame, text='View Records')

# Student form
tk.Label(student_frame, text="Student Name:").pack(pady=5)
student_name_entry = tk.Entry(student_frame)
student_name_entry.pack(pady=5)

tk.Label(student_frame, text="Age:").pack(pady=5)
student_age_entry = tk.Entry(student_frame)
student_age_entry.pack(pady=5)

tk.Label(student_frame, text="Email:").pack(pady=5)
student_email_entry = tk.Entry(student_frame)
student_email_entry.pack(pady=5)

tk.Label(student_frame, text="Student ID:").pack(pady=5)
student_id_entry = tk.Entry(student_frame)
student_id_entry.pack(pady=5)

tk.Button(student_frame, text="Add Student", command=add_student).pack(pady=10)

# Instructor form
tk.Label(instructor_frame, text="Instructor Name:").pack(pady=5)
instructor_name_entry = tk.Entry(instructor_frame)
instructor_name_entry.pack(pady=5)

tk.Label(instructor_frame, text="Age:").pack(pady=5)
instructor_age_entry = tk.Entry(instructor_frame)
instructor_age_entry.pack(pady=5)

tk.Label(instructor_frame, text="Email:").pack(pady=5)
instructor_email_entry = tk.Entry(instructor_frame)
instructor_email_entry.pack(pady=5)

tk.Label(instructor_frame, text="Instructor ID:").pack(pady=5)
instructor_id_entry = tk.Entry(instructor_frame)
instructor_id_entry.pack(pady=5)

tk.Button(instructor_frame, text="Add Instructor", command=add_instructor).pack(pady=10)

# Course form
tk.Label(course_frame, text="Course Name:").pack(pady=5)
course_name_entry = tk.Entry(course_frame)
course_name_entry.pack(pady=5)

tk.Label(course_frame, text="Course ID:").pack(pady=5)
course_id_entry = tk.Entry(course_frame)
course_id_entry.pack(pady=5)

# Instructor dropdown
tk.Label(course_frame, text="Select Instructor:").pack(pady=5)
course_instructor_combo = ttk.Combobox(course_frame)
course_instructor_combo.pack(pady=5)

tk.Button(course_frame, text="Add Course", command=add_course).pack(pady=10)

# Register student for course
tk.Label(register_frame, text="Select Student:").pack(pady=5)
student_combo = ttk.Combobox(register_frame)
student_combo.pack(pady=5)

tk.Label(register_frame, text="Select Course:").pack(pady=5)
course_combo = ttk.Combobox(register_frame)
course_combo.pack(pady=5)

tk.Button(register_frame, text="Register", command=register_student).pack(pady=10)

# Assign instructor to course
tk.Label(assign_frame, text="Select Instructor:").pack(pady=5)
instructor_combo = ttk.Combobox(assign_frame)
instructor_combo.pack(pady=5)

tk.Label(assign_frame, text="Select Course:").pack(pady=5)
course_combo_assign = ttk.Combobox(assign_frame)
course_combo_assign.pack(pady=5)

tk.Button(assign_frame, text="Assign", command=assign_instructor).pack(pady=10)

# Search Widgets
# Add Save and Load buttons
tk.Button(view_frame, text="Save Data", command=save_data_to_file).pack(pady=5)
tk.Button(view_frame, text="Load Data", command=load_data_from_file).pack(pady=5)

tk.Label(view_frame, text="Search by Name:").pack(pady=5)
search_name_entry = tk.Entry(view_frame)
search_name_entry.pack(pady=5)

tk.Label(view_frame, text="Search by ID:").pack(pady=5)
search_id_entry = tk.Entry(view_frame)
search_id_entry.pack(pady=5)

# Create a frame for search options
search_frame = tk.Frame(view_frame)
search_frame.pack(pady=5)

# Add search options for 'Course'
search_option = tk.StringVar(value="Student")  # Default to "Student"

# Add radio buttons for search options (Student, Instructor, Course)
tk.Radiobutton(search_frame, text="Student", variable=search_option, value="Student").pack(side=tk.LEFT)
tk.Radiobutton(search_frame, text="Instructor", variable=search_option, value="Instructor").pack(side=tk.LEFT)
tk.Radiobutton(search_frame, text="Course", variable=search_option, value="Course").pack(side=tk.LEFT)

# Search Button
tk.Button(view_frame, text="Search", command=search_records).pack(pady=10)

# Treeview to display records
tree = ttk.Treeview(view_frame, columns=("ID", "Name", "Type/Instructor"), show="headings", height=15)
tree.heading("ID", text="ID")
tree.heading("Name", text="Name")
tree.heading("Type/Instructor", text="Type/Instructor")
tree.pack(pady=10)

# Add Edit and Delete buttons
tk.Button(view_frame, text="Edit Record", command=edit_record).pack(side=tk.LEFT, padx=10)
tk.Button(view_frame, text="Delete Record", command=delete_record).pack(side=tk.LEFT, padx=10)


# Initialize the application
update_treeview()

# Run the application
root.mainloop()
