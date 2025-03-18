import requests
import json
from behave import given, when, then
import time
import subprocess
from runAllTests import ospath, start_system, shutdown_system, BASE_URL

@given("the API is running")
def step_given_api_running(context):
    response = requests.get(f"{BASE_URL}")
    assert response.status_code == 200, f"API is not running: {response.text}"

@given("the student has the following assignments")
def step_given_student_has_assignments(context):
    """Set up assignments in the system based on the table provided in the feature file."""
    # Delete existing todos to ensure a clean state
    response = requests.get(f"{BASE_URL}/todos")
    if response.status_code == 200:
        for todo in response.json()["todos"]:
            requests.delete(f"{BASE_URL}/todos/{todo['id']}")

    for row in context.table:
        context.assignments = context.table
        payload = {
            "title": row["title"],
            "description": row["description"],
            "doneStatus": row["doneStatus"].lower() == "true"
        }
        response = requests.post(f"{BASE_URL}/todos", json=payload)
        assert response.status_code == 201, f"Failed to create assignment: {response.text}"

@given("the API is running and the student has the following assignments")
def step_given_student_has_assignments(context):
    """Ensure the API is running and initialize assignments."""
    response = requests.get(BASE_URL)
    assert response.status_code == 200, "API is not running"

    # Delete existing todos to ensure a clean state
    response = requests.get(f"{BASE_URL}/todos")
    if response.status_code == 200:
        for todo in response.json()["todos"]:
            requests.delete(f"{BASE_URL}/todos/{todo['id']}")
            
    for row in context.table:
        assignment = {
            "title": row["title"],
            "description": row["description"],
            "doneStatus": row["doneStatus"].lower() == "true"  # Convert string to boolean
        }
        response = requests.post(f"{BASE_URL}/todos", json=assignment)
        assert response.status_code == 201, f"Failed to create assignment {row['title']}, got {response.status_code}"

@then("an error message {message} is returned with status code {status_code}")
def step_then_verify_error_message(context, message, status_code):
    """Check that an error is returned when an invalid doneStatus is used."""
    assert context.response.status_code == int(status_code), f"Expected 400 Bad Request, got {context.response.status_code}"
    response_json = context.response.json()
    assert message in response_json["errorMessages"], f"Expected error '{message}', got {response_json.get('errorMessage', '')}"


@when('a student completes assignment {title}')
def step_when_complete_assignment(context, title):
    """Complete an assignment task by setting doneStatus to True."""
    response = requests.get(f"{BASE_URL}/todos")  # Fetch all todos
    assert response.status_code == 200, f"Failed to retrieve assignments with status code {response.status_code}"

    todos = response.json()["todos"]
    todo_to_complete = next((t for t in todos if t["title"] == title), None)
    assert todo_to_complete, f"Assignment with title {title} not found"
    
    # Update the doneStatus to True
    context.response = requests.put(f"{BASE_URL}/todos/{todo_to_complete['id']}", json={"title": title, "doneStatus": True})
    assert context.response.status_code == 200, f"Failed to complete task {title}"

@given("an assignment task with id {non_existent_id} does not exist")
def step_given_assignment_does_not_exist(context, non_existent_id):
    """Ensure the assignment task does not exist before testing."""
    response = requests.get(f"{BASE_URL}/todos/{non_existent_id}")
    assert response.status_code == 404, f"Assignment {non_existent_id} exists when it shouldn't"



