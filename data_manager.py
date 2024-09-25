import json
from instructor import Instructor
from course import Course
from student import Student

def save_data(filename, instructors, students, courses):
    """Save the state of instructors, students, and courses to a JSON file.

    Args:
        filename (str): The name of the file where the data will be saved.
        instructors (list of Instructor): A list of Instructor objects to save.
        students (list of Student): A list of Student objects to save.
        courses (list of Course): A list of Course objects to save.

    Prints:
        A confirmation message indicating the data has been saved.
    """
    data_to_save = {
        "instructors": [{
            "name": instructor.name,
            "age": instructor.age,
            "_email": instructor._email,
            "instructor_id": instructor.instructor_id,
            "assigned_courses": [course.course_id for course in instructor.assigned_courses]
            }
            for instructor in instructors],
        "courses": [
            {
                "course_id": course.course_id,
                "course_name": course.course_name,
                "instructor_id": course.instructor.instructor_id,  # Save instructor ID only
                "enrolled_students": [student.student_id for student in course.enrolled_students]
            }
            for course in courses
        ],
        "students": [
            {
                "name": student.name,
                "age": student.age,
                "_email": student._email,
                "student_id": student.student_id,
                "registered_courses": [course.course_id for course in student.registered_courses]
            }
            for student in students
        ]
    }

    with open(filename, 'w') as file:
        json.dump(data_to_save, file, indent=4)

    print(f"Data saved to {filename}")

def load_data(filename):
    """Load the state of instructors, students, and courses from a JSON file.

    Args:
        filename (str): The name of the file from which to load the data.

    Returns:
        tuple: A tuple containing three dictionaries: 
            - instructor_dict: A dictionary of Instructor objects indexed by their IDs.
            - student_dict: A dictionary of Student objects indexed by their IDs.
            - course_dict: A dictionary of Course objects indexed by their IDs.
    """
    with open(filename, 'r') as file:
        data = json.load(file)
    
    # Create instructors
    instructor_dict = {}
    for instructor_data in data["instructors"]:
        instructor = Instructor(
            instructor_data["name"],
            instructor_data["age"],
            instructor_data["_email"],
            instructor_data["instructor_id"]
        )
        instructor_dict[instructor.instructor_id] = instructor

    # Rebuild the courses
    course_dict = {}
    for course_data in data["courses"]:
        # Find the instructor for this course
        instructor = instructor_dict.get(course_data["instructor_id"])
        
        # Create course with the found instructor
        course = Course(course_data["course_id"], course_data['course_name'], instructor)
        course_dict[course.course_id] = course

        # Assign this course to the instructor if available
        if instructor is not None:
            instructor.assign_course(course)

    # Rebuild the students and assign courses
    student_dict = {}
    for student_data in data["students"]:
        student = Student(
            student_data["name"],
            student_data["age"],
            student_data["_email"],
            student_data["student_id"]
        )
        student_dict[student.student_id] = student
        
        # Register the courses the student was enrolled in
        for course_id in student_data["registered_courses"]:
            if course_id in course_dict:
                student.register_course(course_dict[course_id])

    return instructor_dict, student_dict, course_dict
