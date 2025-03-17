import requests
import json
from behave import given, when, then
import time
import subprocess
from runAllTests import ospath, start_system, shutdown_system, BASE_URL



@when('a student creates an assignment task with title "{title}" and description "{description}"')
def step_when_create_assignment_with_title_and_description(context, title, description):
    payload = {"title": title, "description": description}
    context.response = requests.post(f"{BASE_URL}/todos", json=payload)

@then('the assignment task with title "{title}" and description "{description}" is created')
def step_then_verify_assignment_created(context, title, description):
    assert context.response.status_code == 201, f"Expected 201, got {context.response.status_code}: {context.response.text}"
    created_task = context.response.json()
    assert created_task["title"] == title, f"Expected title '{title}', got {created_task.get('title')}"
    assert created_task["description"] == description, f"Expected description '{description}', got {created_task.get('description')}"

    # Fetch all todos to verify the new assignment is in the list
    response = requests.get(f"{BASE_URL}/todos")
    assert response.status_code == 200, f"Failed to fetch todos: {response.status_code}"
    
    todos = response.json()["todos"]
    matching_todos = [todo for todo in todos if todo["title"] == title and todo["description"] == description]
    
    assert matching_todos, f"Assignment with title '{title}' and description '{description}' not found in todos list"

@when('a student creates an assignment task with title "{title}"')
def step_when_create_assignment_with_title_only(context, title):
    payload = {"title": title}
    context.response = requests.post(f"{BASE_URL}/todos", json=payload)

@then('the assignment task with title "{title}" is created')
def step_then_verify_assignment_created_with_title_only(context, title):
    assert context.response.status_code == 201, f"Expected 201, got {context.response.status_code}: {context.response.text}"
    created_task = context.response.json()
    assert created_task["title"] == title, f"Expected title '{title}', got {created_task.get('title')}"
    assert "description" not in created_task or created_task["description"] == "", f"Expected no description, but got '{created_task.get('description')}'"

    # Fetch all todos to verify the new assignment is in the list
    response = requests.get(f"{BASE_URL}/todos")
    assert response.status_code == 200, f"Failed to fetch todos: {response.status_code}"
    
    todos = response.json()["todos"]
    matching_todos = [todo for todo in todos if todo["title"] == title and todo["description"] == ""]
    
    assert matching_todos, f"Assignment with title '{title}' not found in todos list"

@when('a student creates an assignment task with description "{description}"')
def step_when_create_assignment_with_description_only(context, description):
    payload = {"description": description}
    context.response = requests.post(f"{BASE_URL}/todos", json=payload)

@then('the assignment task with description "{description}" is not created and an error message "{message}" is returned')
def step_then_verify_error_on_missing_title(context, description, message):
    assert context.response.status_code == 400, f"Expected 400, got {context.response.status_code}: {context.response.text}"
    error_response = context.response.json()
    assert "errorMessages" in error_response, "Expected errorMessages in response"
    assert message in error_response["errorMessages"], f"Expected error message '{message}', got {error_response['errorMessages']}"

def before_scenario(context, scenario):
    """Reset system state before each test to ensure clean execution."""
    start_system()

def after_scenario(context, scenario):
    """Reset system state after each test to ensure test isolation."""
    shutdown_system()
