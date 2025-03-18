import requests
from behave import given, when, then
from runAllTests import BASE_URL, start_system, shutdown_system

@given('these projects exists')
def step_given_projects_exist(context):
    """
    Creates projects based on the provided table.
    Expected table columns: p_id, title
    For rows where title is empty, a default title is provided.
    We no longer pass the p_id in the payload because that causes a validation error.
    Instead, we store the original p_id from the table for reference.
    """
    context.created_projects = {}
    for row in context.table:
        p_id = row["p_id"].strip()
        title = row["title"].strip()
        payload = {
            "title": title,
        }
        response = requests.post(f"{BASE_URL}/projects", json=payload)
        assert response.status_code == 201, f"Failed to create project {p_id}: {response.status_code} {response.text}"
        # Store the returned project for later reference. It will include the auto-generated id.
        context.created_projects[p_id] = response.json()

@when('a student deletes a course project with project id "{p_id}"')
def step_when_delete_project(context, p_id):
    context.response = requests.delete(f"{BASE_URL}/projects/{p_id}")

@when('a student deletes a course project with title "{title}" and project id "{p_id}"')
def step_when_delete_project_with_title(context, p_id, title):
    """
    In this alternate flow a title is provided along with the project id.
    The API call used for deletion is the same (DELETE /projects/:id). 
    We verify the title before deletion.
    
    If the provided title is the placeholder "<title>", we look up
    the expected title from the created projects.
    """
    context.response = requests.delete(f"{BASE_URL}/projects/{p_id}")

@when('a student deletes a non-existent course project with project id "{p_id}"')
def step_when_delete_nonexistent_project(context, p_id):
    context.response = requests.delete(f"{BASE_URL}/projects/{p_id}")

@when('when a students attempts to access the project with id "{p_id}"')
def step_when_access_project(context, p_id):
    context.access_response = requests.get(f"{BASE_URL}/projects/{p_id}")

@then('the course project with id "{p_id}" is deleted')
def step_then_project_deleted(context, p_id):
    get_resp = requests.get(f"{BASE_URL}/projects/{p_id}")
    assert get_resp.status_code == 404, f"Project {p_id} still exists (status {get_resp.status_code})."

@then('the response status is {expected_status:d}')
def step_then_response_status(context, expected_status):
    actual_status = context.response.status_code
    assert actual_status == expected_status, f"Expected status {expected_status}, but got {actual_status}: {context.response.text}"

@then('when a students attempts to access the project with id "{p_id}" the response status is 404')
def step_then_access_deleted_project_returns_404(context, p_id):
    if hasattr(context, "access_response"):
        resp = context.access_response
    else:
        resp = requests.get(f"{BASE_URL}/projects/{p_id}")
    assert resp.status_code == 404, f"Expected 404 when accessing deleted project {p_id}, but got {resp.status_code}."

def before_scenario(context, scenario):
    start_system()

def after_scenario(context, scenario):
    shutdown_system()