import requests
import json
from behave import given, when, then
import time
import subprocess
from runAllTests import ospath, start_system, shutdown_system, BASE_URL



@then('the assignment task {title} is marked as complete')
def step_then_assignment_is_complete(context, title):
    """Verify that the assignment task is now complete."""
    assert context.response.status_code == 200, f"Expected 200 OK, got {context.response.status_code}"

    # Fetch the updated assignment to verify the change
    response = requests.get(f"{BASE_URL}/todos")
    assert response.status_code == 200, "Failed to retrieve updated assignments"

    todos = response.json()["todos"]
    todo = next((t for t in todos if t["title"] == title), None)
    assert todo and todo["doneStatus"].lower() == "true", f"Assignment {title} should be complete but got {todo['doneStatus']}"


@when('a student uncompletes assignment {title}')
def step_when_student_uncompletes_assignment(context, title):
    """Mark an assignment as incomplete (doneStatus=False)."""
    response = requests.get(f"{BASE_URL}/todos")
    assert response.status_code == 200, "Failed to retrieve assignments"

    todos = response.json()["todos"]
    todo = next((t for t in todos if t["title"] == title), None)
    assert todo, f"Assignment {title} not found"

    todo_id = todo["id"]
    update_response = requests.put(f"{BASE_URL}/todos/{todo_id}", json={"title": title, "description": todo["description"], "doneStatus": False})
    context.response = update_response


@then('the assignment task {title} is marked as incomplete')
def step_then_assignment_is_incomplete(context, title):
    """Verify that the assignment task is now incomplete."""
    assert context.response.status_code == 200, f"Expected 200 OK, got {context.response.status_code}"

    response = requests.get(f"{BASE_URL}/todos")
    assert response.status_code == 200, "Failed to retrieve updated assignments"

    todos = response.json()["todos"]
    todo = next((t for t in todos if t["title"] == title), None)
    assert todo and todo["doneStatus"].lower() == "false", f"Assignment {title} should be incomplete but got {todo['doneStatus']}"



@when("a student updates assignment task {non_existent_id} with status {doneStatus}")
def step_when_student_updates_nonexistent_assignment(context, non_existent_id, doneStatus):
    """Try updating a nonexistent assignment."""
    update_response = requests.put(f"{BASE_URL}/todos/{non_existent_id}", json={"doneStatus": doneStatus.lower() == "true"})
    context.response = update_response


def before_scenario(context, scenario):
    """Reset system state before each test to ensure clean execution."""
    start_system()

def after_scenario(context, scenario):
    """Reset system state after each test to ensure test isolation."""
    shutdown_system()