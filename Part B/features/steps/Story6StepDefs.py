import requests
from behave import given, when, then
import time
import subprocess
from runAllTests import ospath, start_system, shutdown_system, BASE_URL

@when('a student creates a course project with title "{title}" and description "{description}"')
def step_when_create_project_with_title_description(context, title, description):
    payload = {"title": title, "description": description}
    context.response = requests.post(f"{BASE_URL}/projects", json=payload)

@then('the course project with title "{title}" and description "{description}" is created')
def step_then_verify_project_created_title_description(context, title, description):
    assert context.response.status_code == 201, (
        f"Expected 201, got {context.response.status_code}: {context.response.text}"
    )
    created_project = context.response.json()
    assert created_project["title"] == title, (
        f"Expected title '{title}', got {created_project.get('title')}"
    )
    assert created_project["description"] == description, (
        f"Expected description '{description}', got {created_project.get('description')}"
    )
    projects_response = requests.get(f"{BASE_URL}/projects")
    assert projects_response.status_code == 200, (
        f"Failed to fetch projects: {projects_response.status_code}"
    )
    projects = projects_response.json()["projects"]
    matching_projects = [
        project for project in projects
        if project["title"] == title and project["description"] == description
    ]
    assert matching_projects, (
        f"Course with title '{title}' and description '{description}' not found in project list"
    )

@when('a student creates a course project for the upcoming semester with title "{title}" and active "false"')
def step_when_create_project_inactive(context, title):
    payload = {"title": title, "active": False}
    context.response = requests.post(f"{BASE_URL}/projects", json=payload)

@then('the course project with title "{title}" and active "false" is created')
def step_then_verify_project_created_inactive(context, title):
    assert context.response.status_code == 201, (
        f"Expected 201, got {context.response.status_code}: {context.response.text}"
    )
    created_project = context.response.json()
    assert created_project["title"] == title, (
        f"Expected title '{title}', got {created_project.get('title')}"
    )
    assert created_project.get("active") == "false", (
        f"Expected active 'false', got {created_project.get('active')}"
    )
    projects_response = requests.get(f"{BASE_URL}/projects")
    assert projects_response.status_code == 200, (
        f"Failed to fetch projects: {projects_response.status_code}"
    )
    projects = projects_response.json()["projects"]
    matching_projects = [
        project for project in projects
        if project["title"] == title and project.get("active") == "false"
    ]
    assert matching_projects, (
        f"Project with title '{title}' and active 'false' not found in project list"
    )

@when('a student creates a course project with an invalid completed status "{completed_status}"')
def step_when_create_project_invalid_completed(context, completed_status):
    payload = {"completed": completed_status}
    context.response = requests.post(f"{BASE_URL}/projects", json=payload)

@then('the response status is {expected_status:d}')
def step_then_response_status(context, expected_status):
    actual_status = context.response.status_code
    assert actual_status == expected_status, (
        f"Expected response status {expected_status}, but got {actual_status}: {context.response.text}"
    )

@then('the course project with completed "{completed_status}" is not created and an error message "{message}" is returned')
def step_then_verify_error_on_invalid_completed(context, completed_status, message):
    assert context.response.status_code == 400, (
        f"Expected 400, got {context.response.status_code}: {context.response.text}"
    )
    error_response = context.response.json()
    assert "errorMessages" in error_response, "Expected errorMessages in response"
    assert message in error_response["errorMessages"], (
        f"Expected error message '{message}', got {error_response['errorMessages']}"
    )

def before_scenario(context, scenario):
    """Reset system state before each test to ensure clean execution."""
    start_system()

def after_scenario(context, scenario):
    """Reset system state after each test to ensure test isolation."""
    shutdown_system()