import requests
import json
from behave import given, when, then
import time
import subprocess
from runAllTests import ospath, start_system, shutdown_system, BASE_URL



@given('the student has the following courses')
def step_given_student_has_courses(context):
    """Create or ensure courses are present."""
    for row in context.table:
        title = row["title"]
        description = row["description"]
        completed = row["completed"].lower() == "true"
        active = row["active"].lower() == "true"

        response = requests.post(f"{BASE_URL}/projects", json={
            "title": title,
            "description": description,
            "completed": completed,
            "active": active
        })
        assert response.status_code == 201, f"Failed to create course {title}"

@given('the student has the following assignments in course {course_title}')
def step_given_student_assignments_in_course(context, course_title):
    """Assign tasks to courses."""
    course_id = None
    # Find course ID by title
    response = requests.get(f"{BASE_URL}/projects")
    courses = response.json()["projects"]
    for course in courses:
        if course["title"] == course_title:
            course_id = course["id"]
            break
    
    assert course_id, f"Course {course_title} not found"
    
    # Assign the given assignments to the course
    for row in context.table:
        assignment_title = row["title"]
        done_status = row["doneStatus"]
        
        # Find assignment ID
        response = requests.get(f"{BASE_URL}/todos")
        todos = response.json()["todos"]
        assignment = next((t for t in todos if t["title"] == assignment_title), None)
        assert assignment, f"Assignment {assignment_title} not found"
        
        # Add the assignment to the course
        todo_id = assignment["id"]
        response = requests.put(f"{BASE_URL}/todos/{todo_id}", json={"title": assignment_title, "description": assignment["description"], "doneStatus": assignment["doneStatus"].lower() == "true", "tasksof": [{"id": course_id}]})
        assert response.status_code == 200, f"Failed to assign {assignment_title} to course {course_title}"

@when('a student removes assignment "{assignment_title}" from course "{course_title}"')
def step_when_student_removes_assignment(context, assignment_title, course_title):
    """Remove an assignment from a course by updating the `tasksof` field to an empty list."""
    # Find the assignment ID
    response = requests.get(f"{BASE_URL}/todos")
    todos = response.json()["todos"]
    assignment = next((t for t in todos if t["title"] == assignment_title), None)
    assert assignment, f"Assignment {assignment_title} not found"

    # Remove the course association by setting `tasksof` to an empty list
    todo_id = assignment["id"]
    response = requests.put(f"{BASE_URL}/todos/{todo_id}", json={"title": assignment["title"], "description": assignment["description"], "doneStatus": assignment["doneStatus"].lower() == "true", "tasksof": []})
    
    context.response = response
    assert response.status_code == 200, f"Failed to remove {assignment_title} from course {course_title}"

@then('assignment "{assignment_title}" is removed from course "{course_title}"')
def step_then_assignment_removed_from_course(context, assignment_title, course_title):
    """Ensure the assignment is no longer associated with the course."""
    # Retrieve the assignment and check that `tasksof` is empty
    response = requests.get(f"{BASE_URL}/todos")
    todos = response.json()["todos"]
    assignment = next((t for t in todos if t["title"] == assignment_title), None)
    assert assignment, f"Assignment {assignment_title} not found after deletion attempt"
    
    assert assignment.get("tasksof", []) == [], f"Assignment {assignment_title} is still associated with a course"

    # Check in /projects to ensure the assignment is not listed in the course's tasks
    response = requests.get(f"{BASE_URL}/projects")
    courses = response.json()["projects"]

    course = next((c for c in courses if c["title"] == course_title), None)
    assert course, f"Course {course_title} not found in /projects"

    course_assignments = course.get("tasks", [])
    assert assignment["id"] not in [ass["id"] for ass in course_assignments], \
        f"Assignment {assignment_title} is still listed in course {course_title}"

@when('a student removes assignment task with id {non_existent_id} from course {course_title}')
def step_when_student_removes_non_existent_id(context, non_existent_id, course_title):
    context.response = requests.put(f"{BASE_URL}/todos/{non_existent_id}")


def before_scenario(context, scenario):
    """Reset system state before each test to ensure clean execution."""
    start_system()

def after_scenario(context, scenario):
    """Reset system state after each test to ensure test isolation."""
    shutdown_system()