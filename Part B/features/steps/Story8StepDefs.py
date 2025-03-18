import requests
from behave import given, when, then
from runAllTests import BASE_URL, start_system, shutdown_system

@given('that the class project with id "{p_id}" has a completed status of "true"')
def step_given_project_completed_true(context, p_id):
    response = requests.get(f"{BASE_URL}/projects/{p_id}")
    if response.status_code != 200:
        payload = {
            "title": f"Class Project {p_id}",
            "description": "Auto-created project for testing",
            "completed": "true"
        }
        create_response = requests.post(f"{BASE_URL}/projects", json=payload)
        assert create_response.status_code == 201, f"Unable to create project {p_id} with completed true: {create_response.text}"
    else:
        payload = {"completed": "true"}
        update_response = requests.post(f"{BASE_URL}/projects/{p_id}", json=payload)
        assert update_response.status_code == 200, f"Failed to update project {p_id} to completed true: {update_response.text}"
    context.project_id = p_id

@given('that the class project with id "{p_id}" does not exist')
def step_given_project_not_exist(context, p_id):
    response = requests.get(f"{BASE_URL}/projects/{p_id}")
    if response.status_code == 200:
        del_response = requests.delete(f"{BASE_URL}/projects/{p_id}")

    response = requests.get(f"{BASE_URL}/projects/{p_id}")
    assert response.status_code == 404, f"Project {p_id} still exists when it should not."
    context.project_id = p_id

@when('a student modifies the completed status of project with id {p_id} with status "true"')
def step_when_modify_completed_status_with(context, p_id):
    payload = {"completed": "true"}
    context.response = requests.post(f"{BASE_URL}/projects/{p_id}", json=payload)

@when('a student modifies the completed status of project with id {p_id} to "true"')
def step_when_modify_completed_status_to(context, p_id):
    payload = {"completed": "true"}
    context.response = requests.post(f"{BASE_URL}/projects/{p_id}", json=payload)

@when('a student attempts to modify the completed status of project with id {p_id} to "true"')
def step_when_modify_completed_nonexistent(context, p_id):
    payload = {"completed": "true"}
    context.response = requests.post(f"{BASE_URL}/projects/{p_id}", json=payload)

@then('the completed status of the project with id "{p_id}" should be "false"')
def step_then_verify_completed_status(context, p_id):
    response = requests.get(f"{BASE_URL}/projects/{p_id}")
    assert response.status_code == 200, f"Failed to retrieve project {p_id}: {response.status_code}"
    project = response.json()

    assert project.get("completed") == "false", (
        f"Expected completed status to be 'false', got '{project.get('completed')}'"
    )

@then('the response status is {expected_status:d}')
def step_then_response_status(context, expected_status):
    actual_status = context.response.status_code
    assert actual_status == expected_status, (
        f"Expected response status {expected_status} but got {actual_status}: {context.response.text}"
    )

@then('"{message}" is returned')
def step_then_error_message(context, message):
    error_response = context.response.json()
    assert "errorMessages" in error_response, f"Response missing 'errorMessages': {error_response}"
    assert message in error_response["errorMessages"], (
        f"Expected error message '{message}', got: {error_response['errorMessages']}"
    )

def before_scenario(context, scenario):
    start_system()

def after_scenario(context, scenario):
    shutdown_system()