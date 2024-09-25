from data_manager import load_data

# Load data from the test file
students, instructors, courses = load_data('test_data.json')

# Print loaded data to verify
for student in students:
    print(f"Student: {student.name}, Courses: {[course.course_name for course in student.registered_courses]}")
for instructor in instructors:
    print(f"Instructor: {instructor.name}, Courses: {[course.course_name for course in instructor.assigned_courses]}")
for course in courses:
    print(f"Course: {course.course_name}, Students: {[student.name for student in course.enrolled_students]}")
