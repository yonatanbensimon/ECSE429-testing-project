import requests
import json
from behave import given, when, then
import time
import subprocess
from runAllTests import ospath, start_system, shutdown_system, BASE_URL

@when("a student views unfinished assignments")
def step_when_view_unfinished_assignments(context):
    """Request only unfinished assignments (doneStatus=false)."""
    context.response = requests.get(f"{BASE_URL}/todos?doneStatus=false")


@when('a student views unfinished assignments with invalid doneStatus "{invalid_status}"')
def step_when_view_invalid_done_status(context, invalid_status):
    """Request unfinished assignments with an invalid doneStatus value."""
    context.response = requests.get(f"{BASE_URL}/todos?doneStatus={invalid_status}")


@then("the unfinished assignments are displayed")
def step_then_verify_unfinished_assignments(context):
    """Verify that only unfinished assignments are returned."""
    assert hasattr(context, "assignments"), "Assignments data not found in context"

    # Extract expected unfinished assignments
    expected_titles = [row["title"] for row in context.assignments if row["doneStatus"] == "false"]

    # Fetch actual unfinished assignments from API
    response = requests.get(f"{BASE_URL}/todos")
    assert response.status_code == 200, f"Failed to fetch todos: {response.text}"
    todos = response.json()["todos"]

    actual_titles = [todo["title"] for todo in todos if todo["doneStatus"] == "false"]

    assert set(actual_titles) == set(expected_titles), (
        f"Expected unfinished assignments: {expected_titles}, but got {actual_titles}"
    )
    
@then("no unfinished assignments are displayed")
def step_then_verify_no_unfinished_assignments(context):
    """Ensure that no unfinished assignments are returned."""
    assert context.response.status_code == 200, f"Expected 200 OK, got {context.response.status_code}"
    assert context.response.json()["todos"] == [], "Expected no unfinished assignments, but some were returned"



def before_scenario(context, scenario):
    """Reset system state before each test to ensure clean execution."""
    start_system()

def after_scenario(context, scenario):
    """Reset system state after each test to ensure test isolation."""
    shutdown_system()