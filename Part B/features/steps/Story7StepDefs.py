import requests
from behave import given, when, then
from runAllTests import BASE_URL, start_system, shutdown_system

@given('a task with ID "{t_id}" exists')
def step_given_task_exists(context, t_id):
    response = requests.get(f"{BASE_URL}/todos/{t_id}")
    if response.status_code != 200:
        payload = {
            "title": f"Task {t_id}",
            "doneStatus": False
        }
        create_response = requests.post(f"{BASE_URL}/todos", json=payload)
        assert create_response.status_code == 201, f"Unable to create task with id {t_id}"
        task = create_response.json()
        context.task_id = task.get("id")
    else:
        task = response.json()
        context.task_id = task.get("id")

@given('that the task with "{t_id}" is already linked to the project with id "{p_id}"')
def step_given_task_already_linked(context, t_id, p_id):
    payload = {"id": context.task_id}
    project_id = getattr(context, "project_id", p_id)
    response = requests.post(f"{BASE_URL}/projects/{project_id}/tasks", json=payload)
    if response.status_code not in (200, 201):
        assert False, f"Error pre-linking task: {response.status_code} - {response.text}"

@when('a student adds an assignment task with id {t_id} to a project with id {p_id}')
def step_when_add_task(context, t_id, p_id):
    payload = {"id": context.task_id}
    project_id = getattr(context, "project_id", p_id)
    context.response = requests.post(f"{BASE_URL}/projects/{project_id}/tasks", json=payload)

@when('a students adds the assignment task with id {t_id} to the project with id "{p_id}"')
def step_when_add_task_already_linked(context, t_id, p_id):
    payload = {"id": context.task_id}
    project_id = getattr(context, "project_id", p_id)
    context.response = requests.post(f"{BASE_URL}/projects/{project_id}/tasks", json=payload)

@when('a students adds an assignment task with a non existend id "{t_id}" to project with id "{p_id}"')
def step_when_add_nonexistent_task(context, t_id, p_id):
    payload = {"id": t_id}
    project_id = getattr(context, "project_id", p_id)
    context.response = requests.post(f"{BASE_URL}/projects/{project_id}/tasks", json=payload)

@then('the task with id {t_id} is added to the project with id {p_id}')
def step_then_verify_task_linked(context, t_id, p_id):
    project_id = getattr(context, "project_id", p_id)
    response = requests.get(f"{BASE_URL}/projects/{project_id}/tasks")
    assert response.status_code == 200, f"Failed to fetch tasks of project {project_id}: {response.status_code}"
    
    todos = response.json().get("todos")
    assert todos is not None, "Response JSON does not contain the 'todos' key"
    
    found = any(str(todo.get("id")) == str(context.task_id) for todo in todos)
    assert found, f"Task with id {context.task_id} was not found linked to project {project_id}"

@then('the response status is {expected_status:d}')
def step_then_response_status(context, expected_status):
    actual_status = context.response.status_code
    assert actual_status == expected_status, f"Expected status {expected_status} but got {actual_status}: {context.response.text}"

@then('"{message}" is returned')
def step_then_error_message(context, message):
    error_response = context.response.json()
    assert "errorMessages" in error_response, f"Response missing 'errorMessages': {error_response}"
    assert message in error_response["errorMessages"], f"Expected error message '{message}', got: {error_response['errorMessages']}"

def before_scenario(context, scenario):
    start_system()

def after_scenario(context, scenario):
    shutdown_system()