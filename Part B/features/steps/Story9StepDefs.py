import requests
from behave import given, when, then
from runAllTests import BASE_URL, start_system, shutdown_system

@given('the following projects exists')
def step_given_following_projects_exist(context):
    """
    Creates projects based on the table provided.
    Expected table columns: p_id, active
    For example:
        | p_id     | active |
        | ECSE 200 | true   |
        | ECSE 201 | false  |
        | ECSE 205 | true   |
        | ECSE 210 | false  |
    """
    for row in context.table:
        title = row["p_id"]
        active = row["active"]
        payload = {
            "title": title,
            "description": f"Auto-created project {title} for filtering tests",
            "active": active
        }

        response = requests.post(f"{BASE_URL}/projects", json=payload)
        assert response.status_code == 201, f"Failed to create project {title}: {response.status_code} {response.text}"

@given('there are no projects with "active" set to "true"')
def step_given_no_active_projects(context):
    response = requests.get(f"{BASE_URL}/projects?active=true")
    if response.status_code == 200:
        projects = response.json().get("projects", [])
        for project in projects:
            project_id = project.get("id")
            del_response = requests.delete(f"{BASE_URL}/projects/{project_id}")

    response_check = requests.get(f"{BASE_URL}/projects?active=true")
    projects_check = response_check.json().get("projects", [])
    assert len(projects_check) == 0, f"Expected 0 active projects but found {len(projects_check)}"



@when('a student gets all project with an active status of "true"')
def step_when_get_projects_active_true(context):
    context.response = requests.get(f"{BASE_URL}/projects?active=true")

@when('a students gets all course project with an active status of "true"')
def step_when_get_course_projects_active_true(context):
    context.response = requests.get(f"{BASE_URL}/projects?active=true")

@when('a student gets all projects with invalid active status "{active}"')
def step_when_get_projects_invalid_active(context, active):
    context.response = requests.get(f"{BASE_URL}/projects?active={active}")

@then('the response contains all {p_id} with an active status of true')
def step_then_check_projects_in_response(context, p_id):
    """
    This step verifies that the response JSON contains projects with the given p_id
    and that their "active" status is "true". Since this is a Scenario Outline,
    the parameter p_id will be one of the expected project titles.
    """
    response_json = context.response.json()
    projects = response_json.get("projects", [])
    
    matching_projects = [project for project in projects if project.get("title") == p_id]
    assert matching_projects, f"Expected project with title '{p_id}' not found in response"
    
    for project in matching_projects:
        assert project.get("active") == "true", f"Project '{p_id}' does not have active status 'true'"

@then('the response status is {expected_status:d}')
def step_then_response_status(context, expected_status):
    actual_status = context.response.status_code
    assert actual_status == expected_status, f"Expected status {expected_status}, but got {actual_status}: {context.response.text}"

@then('the response contains an empty list')
def step_then_response_empty_list(context):
    response_json = context.response.json()
    projects = response_json.get("projects", None)
    if projects is None:
        projects = []
    assert isinstance(projects, list), "Expected projects to be a list"
    assert len(projects) == 0, f"Expected no projects but found {len(projects)}"

@then('"{message}" is returned')
def step_then_error_message(context, message):
    error_response = context.response.json()
    assert "errorMessages" in error_response, f"Expected errorMessages but got: {error_response}"
    assert message in error_response["errorMessages"], f"Expected error message '{message}', got: {error_response['errorMessages']}"

def before_scenario(context, scenario):
    start_system()

def after_scenario(context, scenario):
    shutdown_system()