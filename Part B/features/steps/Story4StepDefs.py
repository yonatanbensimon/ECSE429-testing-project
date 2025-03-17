import requests
import json
from behave import given, when, then
import time
import subprocess
from runAllTests import ospath, start_system, shutdown_system, BASE_URL


@when('a student deletes an assignment task with title {title}')
def step_when_delete_assignment(context, title):
    """Delete the assignment task by title."""
    response = requests.get(f"{BASE_URL}/todos")  # Fetch all todos
    assert response.status_code == 200, f"Failed to retrieve assignments with status code {response.status_code}"

    todos = response.json()["todos"]
    todo_to_delete = next((t for t in todos if t["title"] == title), None)
    assert todo_to_delete, f"Assignment with title {title} not found"
    
    # Perform the delete operation
    delete_response = requests.delete(f"{BASE_URL}/todos/{todo_to_delete['id']}")
    context.response = delete_response

@then('the assignment task with title {title} is deleted')
def step_then_verify_task_deleted(context, title):
    """Verify that the assignment task has been deleted."""
    assert context.response.status_code == 200, f"Failed to delete task with status code {context.response.status_code}"
    
    # Verify the task is no longer in the list of assignments
    response = requests.get(f"{BASE_URL}/todos")
    todos = response.json()["todos"]
    assert not any(todo["title"] == title for todo in todos), f"Task {title} was not deleted successfully"


@when('a student deletes assignment task with id {non_existent_id}')
def step_when_delete_non_existent_assignment(context, non_existent_id):
    """Attempt to delete a non-existent assignment task."""
    context.response = requests.delete(f"{BASE_URL}/todos/{non_existent_id}")


def before_scenario(context, scenario):
    """Reset system state before each test to ensure clean execution."""
    start_system()

def after_scenario(context, scenario):
    """Reset system state after each test to ensure test isolation."""
    shutdown_system()