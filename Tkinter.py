import tkinter as tk
from tkinter import ttk, messagebox
from student import Student
from instructor import Instructor
from course import Course
from data_manager import save_data, load_data

# Data storage
students = []
instructors = []
courses = []

# Functionality to add a student
def add_student():
    student_name = student_name_entry.get()
    student_age = student_age_entry.get()
    student_email = student_email_entry.get()
    student_id = student_id_entry.get()

    if student_name and student_age and student_email and student_id:
        try:
            # Create a Student instance
            student = Student(student_name, int(student_age), student_email, int(student_id))
            students.append(student)
            messagebox.showinfo("Success", f"Student {student_name} added.")
            update_treeview()
            refresh_dropdowns()
        except ValueError as e:
            # Catch validation errors from the Student class
            messagebox.showerror("Error", str(e))
    else:
        messagebox.showerror("Error", "Please fill out all fields.")

# Functionality to add an instructor
def add_instructor():
    instructor_name = instructor_name_entry.get()
    instructor_age = instructor_age_entry.get()
    instructor_email = instructor_email_entry.get()
    instructor_id = instructor_id_entry.get()

    if instructor_name and instructor_age and instructor_email and instructor_id:
        try:
            # Create an Instructor instance
            instructor = Instructor(instructor_name, int(instructor_age), instructor_email, int(instructor_id))
            instructors.append(instructor)
            messagebox.showinfo("Success", f"Instructor {instructor_name} added.")
            update_treeview()
            refresh_dropdowns()
        except ValueError as e:
            # Catch validation errors from the Instructor class
            messagebox.showerror("Error", str(e))
    else:
        messagebox.showerror("Error", "Please fill out all fields.")

# Functionality to add a course
def add_course():
    course_name = course_name_entry.get()
    course_id = int(course_id_entry.get())
    instructor_text = course_instructor_combo.get()  # Get instructor text from dropdown

    if course_name and course_id:
        try:
            instructor = None

            # Only find instructor if an ID is provided (and is not "None")
            if instructor_text and instructor_text != "None":
                # Extract instructor ID and convert it to an integer
                instructor_id = int(instructor_text.split('(')[-1].strip(')'))
                print("Extracted ID:", instructor_id)
                print("Type of Extracted ID:", type(instructor_id))

                # Find the instructor instance by ID
                instructor = next((inst for inst in instructors if inst.instructor_id == instructor_id), None)
                if instructor is None:
                    raise ValueError("Instructor not found")

            # Create a Course instance with or without an instructor
            course = Course(course_id, course_name, instructor)
            courses.append(course)

            # Assign the course to the instructor if an instructor is provided
            if instructor is not None:
                instructor.assign_course(course)

            messagebox.showinfo("Success", f"Course {course_name} added.")
            update_treeview()
            refresh_dropdowns()
        except ValueError as e:
            messagebox.showerror("Error", str(e))
    else:
        messagebox.showerror("Error", "Please fill out all fields.")

# Register student for a course
def register_student():
    # Extract student and course data from dropdowns
    student_text = student_combo.get()
    course_text = course_combo.get()

    if student_text and course_text:
        try:
            # Extract IDs from the selected text
            student_id = int(student_text.split('(')[-1].strip(')'))
            course_id = int(course_text.split('(')[-1].strip(')'))

            # Find student and course instances
            student = next((stud for stud in students if stud.student_id == student_id), None)
            course = next((crs for crs in courses if crs.course_id == course_id), None)

            if student is None or course is None:
                raise ValueError("Student or course not found")

            # Register the student to the course using the Student method
            student.register_course(course)

            # Add student to the course using the Course method
            course.add_student(student)

            messagebox.showinfo("Success", f"Student {student.name} registered to course {course.course_name}.")
            update_treeview()
            refresh_dropdowns()
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Unexpected error: {str(e)}")
    else:
        messagebox.showerror("Error", "Please select both student and course.")

# Assign instructor to a course
def assign_instructor():
    # Extract instructor and course data from dropdowns
    instructor_text = instructor_combo.get()
    course_text = course_combo_assign.get()

    if instructor_text and course_text:
        try:
            # Extract IDs from the selected text
            instructor_id = int(instructor_text.split('(')[-1].strip(')'))
            course_id = int(course_text.split('(')[-1].strip(')'))

            # Find the instructor and course objects
            instructor = next((inst for inst in instructors if inst.instructor_id == instructor_id), None)
            course = next((crs for crs in courses if crs.course_id == course_id), None)

            if instructor is None or course is None:
                raise ValueError("Instructor or course not found")

            # Assign the instructor to the course
            course.instructor = instructor  # Set the course's instructor to the Instructor object
            instructor.assign_course(course)  # Add the course to the instructor's assigned courses

            messagebox.showinfo("Success", f"Instructor {instructor.name} assigned to {course.course_name}.")
            update_treeview()
            refresh_dropdowns()
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Unexpected error: {str(e)}")
    else:
        messagebox.showerror("Error", "Invalid instructor or course selection.")

def refresh_dropdowns():
    # Populate student dropdown with "Name (ID)"
    student_combo['values'] = [f"{student.name} ({student.student_id})" for student in students]

    # Populate instructor dropdown with "Name (ID)"
    instructor_combo['values'] = [f"{instructor.name} ({instructor.instructor_id})" for instructor in instructors]

    # Populate course dropdowns with "Course Name (ID)"
    course_combo['values'] = [f"{course.course_name} ({course.course_id})" for course in courses]
    course_combo_assign['values'] = [f"{course.course_name} ({course.course_id})" for course in courses]

    # Populate course instructor dropdown with "Instructor Name (ID)"
    course_instructor_combo['values'] = [f"{instructor.name} ({instructor.instructor_id})" for instructor in instructors]

# Update the Treeview with all records
def update_treeview():
    for row in tree.get_children():
        tree.delete(row)

    # Add students to the treeview
    for student in students:
        # tree.insert('', 'end', values=(student.name, student.age, student._email, student.student_id, "Student"))
        tree.insert('', 'end', values =(student.student_id, student.name, "Student"))

    # Add instructors to the treeview
    for instructor in instructors:
        tree.insert('', 'end', values=(instructor.instructor_id, instructor.name, "Instructor"))

    # Add courses to the treeview
    for course in courses:
        tree.insert('', 'end', values=(course.course_id,  course.course_name, "Course"))


def edit_record():
    # Get the selected item
    selected_item = tree.selection()

    if not selected_item:
        messagebox.showerror("Error", "No record selected.")
        return

    # Retrieve the record's data (Assuming "ID" is the primary key in the Treeview)
    selected_id = tree.item(selected_item, 'values')[0]

    # Find the selected record by ID
    if search_option.get() == "Student":
        record = next((stud for stud in students if stud.student_id == int(selected_id)), None)
    elif search_option.get() == "Instructor":
        record = next((inst for inst in instructors if inst.instructor_id == int(selected_id)), None)
    elif search_option.get() == "Course":
        record = next((crs for crs in courses if crs.course_id == selected_id), None)

    if record:
        # Open a new window for editing the record
        edit_window = tk.Toplevel(root)
        edit_window.title("Edit Record")

        # Set up the fields for editing based on the type
        tk.Label(edit_window, text="Name:").pack(pady=5)
        name_entry = tk.Entry(edit_window)
        name_entry.pack(pady=5)
        name_entry.insert(0, record.name)  # Pre-fill with current value

        tk.Label(edit_window, text="Age:").pack(pady=5)
        age_entry = tk.Entry(edit_window)
        age_entry.pack(pady=5)
        age_entry.insert(0, record.age)  # Pre-fill with current value

        tk.Label(edit_window, text="Email:").pack(pady=5)
        email_entry = tk.Entry(edit_window)
        email_entry.pack(pady=5)
        email_entry.insert(0, record._email)  # Pre-fill with current value

        # Set up fields based on record type
        if isinstance(record, Student):
            tk.Label(edit_window, text="Student ID:").pack(pady=5)
            id_entry = tk.Entry(edit_window)
            id_entry.pack(pady=5)
            id_entry.insert(0, record.student_id)  # Pre-fill with current value

        elif isinstance(record, Instructor):
            tk.Label(edit_window, text="Instructor ID:").pack(pady=5)
            id_entry = tk.Entry(edit_window)
            id_entry.pack(pady=5)
            id_entry.insert(0, record.instructor_id)  # Pre-fill with current value

        elif isinstance(record, Course):
            tk.Label(edit_window, text="Course ID:").pack(pady=5)
            id_entry = tk.Entry(edit_window)
            id_entry.pack(pady=5)
            id_entry.insert(0, record.course_id)  # Pre-fill with current value

        # Function to save the changes
        def save_changes():
            try:
                # Validate and update the common record fields
                record.name = name_entry.get()
                record.age = int(age_entry.get())
                record._email = email_entry.get()

                if isinstance(record, Student):
                    # Validate and update the student-specific fields
                    record.student_id = int(id_entry.get())

                elif isinstance(record, Instructor):
                    # Validate and update the instructor-specific fields
                    record.instructor_id = int(id_entry.get())

                elif isinstance(record, Course):
                    # Validate and update the course-specific fields
                    record.course_id = id_entry.get()

                # Make sure to update Treeview to reflect the changes
                update_treeview()
                edit_window.destroy()
                messagebox.showinfo("Success", "Record updated successfully.")
            except ValueError as e:
                messagebox.showerror("Error", str(e))

        tk.Button(edit_window, text="Save Changes", command=save_changes).pack(pady=10)
    else:
        messagebox.showerror("Error", "Record not found.")

def delete_record():
    # Get the selected item
    selected_item = tree.selection()

    if not selected_item:
        messagebox.showerror("Error", "No record selected.")
        return

    # Retrieve the record's data
    selected_id = tree.item(selected_item, 'values')[0]

    # Find and delete the record by ID
    if search_option.get() == "Student":
        global students
        students = [stud for stud in students if stud.student_id != int(selected_id)]
    elif search_option.get() == "Instructor":
        global instructors
        instructors = [inst for inst in instructors if inst.instructor_id != int(selected_id)]
    elif search_option.get() == "Course":
        global courses
        courses = [crs for crs in courses if crs.course_id != selected_id]

    # Update the Treeview
    update_treeview()
    messagebox.showinfo("Success", "Record deleted successfully.")


def save_data_to_file():
    try:
        filename = "school_data.json"  # Set the filename to save
        save_data(filename, instructors, students, courses)
        messagebox.showinfo("Success", "Data saved successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"Error saving data: {str(e)}")

def load_data_from_file():
    global students, instructors, courses
    try:
        filename = "school_data.json"  # Set the filename to load
        instructor_dict, student_dict, course_dict = load_data(filename)

        # Convert the dictionaries to lists for use in the application
        instructors = list(instructor_dict.values())
        students = list(student_dict.values())
        courses = list(course_dict.values())

        # Update the UI
        update_treeview()
        refresh_dropdowns()
        messagebox.showinfo("Success", "Data loaded successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"Error loading data: {str(e)}")

def search_records():
    # Get the search query values
    name_query = search_name_entry.get().strip().lower()
    id_query = search_id_entry.get().strip().lower()
    search_type = search_option.get()

    # Clear the treeview
    for item in tree.get_children():
        tree.delete(item)

    # Search Students
    if search_type == "Student":
        for student in students:
            if (name_query in student.name.lower() or not name_query) and \
               (id_query in student.student_id.lower() or not id_query):
                tree.insert("", "end", values=(student.student_id, student.name, "Student"))
    
    # Search Instructors
    elif search_type == "Instructor":
        for instructor in instructors:
            if (name_query in instructor.name.lower() or not name_query) and \
               (id_query in instructor.instructor_id.lower() or not id_query):
                tree.insert("", "end", values=(instructor.instructor_id, instructor.name, "Instructor"))
    
    # Search Courses
    elif search_type == "Course":
        for course in courses:
            if (name_query in course.course_name.lower() or not name_query) and \
               (id_query in course.course_id.lower() or not id_query):
                instructor_name = course.instructor.name if course.instructor else "N/A"
                tree.insert("", "end", values=(course.course_id, course.course_name, instructor_name))
    else:
        messagebox.showerror("Error", "Invalid search type selected.")

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
