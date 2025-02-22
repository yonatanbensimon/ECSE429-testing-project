#Todo Test
import pytest as pt
import requests
import random
import subprocess
import time
import os

BASE_URL = "http://localhost:4567/todos"
SHUTDOWN_URL = "http://localhost:4567/shutdown"
HEADERS_JSON = {"Content-Type": "application/json", "Accept": "application/json"}
HEADERS_XML = {"Content-Type": "application/xml", "Accept": "application/xml"}

def is_api_running():
    print("Checking if the API is running")
    try:
        response = requests.get("http://localhost:4567")
        return response.status_code < 500
    except requests.exceptions.ConnectionError:
        return False
    
def wait_for_api_to_be_ready():
    """Wait for the API to be fully ready before proceeding."""
    server_ready = False
    while not server_ready:
        try:
            response = requests.get("http://localhost:4567", headers=HEADERS_JSON)
            if response.status_code == 200:  # Adjust based on your expected response code
                server_ready = True
        except requests.exceptions.ConnectionError:
            pass  # Ignore connection errors and retry

def shutdown_api():
    """Call the API shutdown endpoint."""
    try:
        response = requests.get(SHUTDOWN_URL)
        if response.status_code == 200:
            print("API shutdown successfully")
    except requests.exceptions.RequestException:
        print("Failed to shut down the API")

class TesttodoEndpoint:
    

    @pt.fixture(autouse=True)
    def save_initial_state(self):
        response = requests.get(BASE_URL, headers=HEADERS_JSON)
        assert response.status_code == 200
        self.initial_todos = response.json()
        print(response.json())

    def test_get_all_todos_json(self):
        response = requests.get(BASE_URL, headers=HEADERS_JSON)
        assert response.status_code == 200
        data = response.json()
        expected_data = self.initial_todos
        assert data == expected_data, f'The expected response was {expected_data}, but the following data was received {data}'

    def test_get_all_todos_xml(self):
        response = requests.get(BASE_URL, headers=HEADERS_XML)
        assert response.status_code == 200
        data = response.text
        assert '<todos>' in data
        assert '</todos>' in data

    def test_get_todo_filter_query(self):
        response = requests.get(BASE_URL, headers=HEADERS_JSON)
        assert response.status_code == 200
        data = response.json()
        expected_data = self.initial_todos
        assert data == expected_data, f'The expected response was {expected_data}, but the following data was received {data}'

    def test_get_todo_filter_query_xml(self):
        response = requests.get(BASE_URL, params={"doneStatus": "false"}, headers=HEADERS_XML)
        assert response.status_code == 200
        data = response.text
        assert '<todos>' in data
        assert '</todos>' in data

    def test_put_todo(self):
        todo = random.choice(self.initial_todos["todos"])
        response = requests.put(BASE_URL, json=todo, headers=HEADERS_JSON)
        assert response.status_code == 405

    def test_post_todo(self):
        todo = {
            "title": "Test Todo",
            "doneStatus": "false",
            "description": "This is a test todo",
            "tasksof": [
                {
                    "id": "1"
                }
            ]
        }
        response = requests.post(BASE_URL, json=todo, headers=HEADERS_JSON)
        assert response.status_code == 201
        data = response.json()
        print(data)
        assert data['id'] == '3'
        assert data['title'] == todo['title']
        assert data['doneStatus'] == todo['doneStatus']
        assert data['description'] == todo['description']
        assert data['tasksof'] == todo['tasksof']

        # Verify that the initial data has not changed
        response = requests.get(BASE_URL, headers=HEADERS_JSON)
        assert response.status_code == 200
        current_todos = response.json()
        assert all(todo in current_todos for todo in self.initial_todos), "Initial todos have changed"

    def test_post_todo_xml(self):
        todo = {
            "title": "Test Todo",
            "doneStatus": "false",
            "description": "This is a test todo",
            "tasksof": [
                {
                    "id": "1"
                }
            ]
        }
        response = requests.post(BASE_URL, json=todo, headers=HEADERS_XML)
        assert response.status_code == 201
        data = response.text
        assert '<todo>' in data
        assert '</todo>' in data
        assert '<id>3</id>' in data
        assert f'<title>{todo["title"]}</title>' in data
        assert f'<doneStatus>{todo["doneStatus"]}</doneStatus>' in data
        assert f'<description>{todo["description"]}</description>' in data
        assert '<tasksof>' in data
        assert '</tasksof>' in data
        assert '<task id="1"/>' in data
        
        # Verify that the initial data has not changed
        response = requests.get(BASE_URL, headers=HEADERS_JSON)
        assert response.status_code == 200
        current_todos = response.json()
        assert all(todo in current_todos for todo in self.initial_todos), "Initial todos have changed"

    def test_post_todo_missing_title(self):
        todo = {
            "doneStatus": False,
            "description": "This is a test todo",
            "tasksof": [
                {
                    "id": "1"
                }
            ]
        }
        response = requests.post(BASE_URL, json=todo, headers=HEADERS_JSON)
        assert response.status_code == 400
        data = response.json()
        assert data == {'errorMessages': ['title : field is mandatory']}

    def test_post_todo_string_doneStatus(self):
        todo = {
            "title": "Test Todo",
            "doneStatus": "False",
            "description": "This is a test todo",
            "tasksof": [
                {
                    "id": "1"
                }
            ]
        }
        response = requests.post(BASE_URL, json=todo, headers=HEADERS_JSON)
        assert response.status_code == 400
        data = response.json()
        assert data == {'errorMessages': ['Failed Validation: doneStatus should be BOOLEAN']}

    def test_post_todo_id_included(self):
        todo = {
            "id": "3",
            "title": "Test Todo",
            "doneStatus": False,
            "description": "This is a test todo",
            "tasksof": [
                {
                    "id": "1"
                }
            ]
        }
        response = requests.post(BASE_URL, json=todo, headers=HEADERS_JSON)
        assert response.status_code == 400
        data = response.json()
        assert data == {'errorMessages': ['Invalid Creation: Failed Validation: Not allowed to create with id']}

    def test_delete_todo(self):
        response = requests.delete(BASE_URL, headers=HEADERS_JSON)
        assert response.status_code == 405

    def test_options_todo(self):
        response = requests.options(BASE_URL)
        assert response.status_code == 200
        assert response.headers['Allow'] == 'OPTIONS, GET, HEAD, POST'

    def test_head_todo(self):
        response = requests.head(BASE_URL)
        assert response.status_code == 200
        assert len(response.text) == 0
        assert response.headers['Content-Type'] == 'application/json'
        assert response.headers['Transfer-Encoding'] == 'chunked'
        assert response.headers['Server'] == 'Jetty(9.4.z-SNAPSHOT)'

    def test_patch_todo(self):
        todo = random.choice(self.initial_todos["todos"])
        response = requests.patch(BASE_URL, json=todo, headers=HEADERS_JSON)
        assert response.status_code == 405

    def test_get_todo_id(self):
        todo = random.choice(self.initial_todos["todos"])
        response = requests.get(f"{BASE_URL}/{todo['id']}", headers=HEADERS_JSON)
        assert response.status_code == 200
        data = response.json()["todos"][0]
        assert data == todo

    def test_get_todo_id_xml(self):
        todo = random.choice(self.initial_todos["todos"])
        response = requests.get(f"{BASE_URL}/{todo['id']}", headers=HEADERS_XML)
        assert response.status_code == 200
        data = response.text
        assert '<todo>' in data
        assert '</todo>' in data

    def test_get_todo_id_not_found(self):
        response = requests.get(f"{BASE_URL}/420", headers=HEADERS_JSON)
        assert response.status_code == 404
        data = response.json()
        assert data == {'errorMessages': ['Could not find an instance with todos/420']}

    def test_put_todo_id(self):
        todo = random.choice(self.initial_todos["todos"])
        new_todo = {
            "title": "scan a lot of paperwork",
            "doneStatus": "true",
            "description": "this was tough",
        }
        response = requests.put(f"{BASE_URL}/{todo['id']}", json=new_todo, headers=HEADERS_JSON)
        assert response.status_code == 200
        data = response.json()
        assert data['id'] == todo['id']
        assert data['title'] == new_todo['title']
        assert data['doneStatus'] == new_todo['doneStatus']
        assert data['description'] == new_todo['description']
        assert data['tasksof'] == todo['tasksof']

        # Verify that the initial data has not changed, excluding the modified todo
        response = requests.get(BASE_URL, headers=HEADERS_JSON)
        assert response.status_code == 200
        current_todos = response.json()
        initial_todos_excluding_modified = [t for t in self.initial_todos if t['id'] != todo['id']]
        assert all(todo in current_todos for todo in initial_todos_excluding_modified), "Initial todos have changed"

    def test_put_todo_id_xml(self):
        todo = random.choice(self.initial_todos["todos"])
        new_todo = {
            "title": "scan a lot of paperwork",
            "doneStatus": "true",
            "description": "this was tough",
        }
        response = requests.put(f"{BASE_URL}/{todo['id']}", json=new_todo, headers=HEADERS_XML)
        assert response.status_code == 200
        data = response.text
        assert '<todo>' in data
        assert '</todo>' in data
        assert f'<id>{todo["id"]}</id>' in data
        assert f'<title>{new_todo["title"]}</title>' in data
        assert f'<doneStatus>{new_todo["doneStatus"]}</doneStatus>' in data
        assert f'<description>{new_todo["description"]}</description>' in data
        assert '<tasksof>' in data
        assert '</tasksof>' in data

        # Verify that the initial data has not changed, excluding the modified todo
        response = requests.get(BASE_URL, headers=HEADERS_JSON)
        assert response.status_code == 200
        current_todos = response.json()
        initial_todos_excluding_modified = [t for t in self.initial_todos if t['id'] != todo['id']]
        assert all(todo in current_todos for todo in initial_todos_excluding_modified), "Initial todos have changed"

    def test_put_todo_id_not_found(self):
        new_todo = {
            "title": "scan a lot of paperwork",
            "doneStatus": True,
            "description": "this was tough",
        }
        response = requests.put(f"{BASE_URL}/420", json=new_todo, headers=HEADERS_JSON)
        assert response.status_code == 404
        data = response.json()
        assert data == {'errorMessages': ['Invalid GUID for 420 entity todo']}

        # Verify that the initial data has not changed
        response = requests.get(BASE_URL, headers=HEADERS_JSON)
        assert response.status_code == 200
        current_todos = response.json()
        assert all(todo in current_todos for todo in self.initial_todos), "Initial todos have changed"

    def test_put_todo_id_removing_title(self):
        todo = random.choice(self.initial_todos["todos"])
        new_todo = {
            "title": "",
            "doneStatus": True,
            "description": "this was tough",
        }

        response = requests.put(f"{BASE_URL}/{todo['id']}", json=new_todo, headers=HEADERS_JSON)
        assert response.status_code == 400
        data = response.json()
        assert data == {'errorMessages': ['Failed Validation: title : can not be empty']}

        # Verify that the initial data has not changed
        response = requests.get(BASE_URL, headers=HEADERS_JSON)
        assert response.status_code == 200
        current_todos = response.json()
        assert all(todo in current_todos for todo in self.initial_todos), "Initial todos have changed"

    def test_put_todo_id_remove_tasksof(self):
        todo = random.choice(self.initial_todos["todos"])
        new_todo = {
            "title": "scan a lot of paperwork",
            "doneStatus": "true",
            "description": "this was tough",
            "tasksof": []
        }

        response = requests.put(f"{BASE_URL}/{todo['id']}", json=new_todo, headers=HEADERS_JSON)
        assert response.status_code == 200
        data = response.json()
        assert data['id'] == todo['id']
        assert data['title'] == new_todo['title']
        assert data['doneStatus'] == new_todo['doneStatus']
        assert data['description'] == new_todo['description']
        assert data['tasksof'] == []

        # Verify that tasksof was removed from the todo
        response = requests.get(f"{BASE_URL}/{todo['id']}", headers=HEADERS_JSON)
        assert response.status_code == 200
        data = response.json()
        assert data['tasksof'] == []

        # Verify that the initial data has not changed, excluding the modified todo
        response = requests.get(BASE_URL, headers=HEADERS_JSON)
        assert response.status_code == 200
        current_todos = response.json()
        initial_todos_excluding_modified = [t for t in self.initial_todos if t['id'] != todo['id']]
        assert all(todo in current_todos for todo in initial_todos_excluding_modified), "Initial todos have changed"

    def test_post_todo_id(self):
        todo = random.choice(self.initial_todos["todos"])
        new_todo = {
            "title": "scan a lot of paperwork",
            "doneStatus": "true",
            "description": "this was tough",
        }
        response = requests.post(f"{BASE_URL}/{todo['id']}", json=new_todo, headers=HEADERS_JSON)
        assert response.status_code == 200
        data = response.json()
        assert data['id'] == todo['id']
        assert data['title'] == new_todo['title']
        assert data['doneStatus'] == new_todo['doneStatus']
        assert data['description'] == new_todo['description']
        assert data['tasksof'] == todo['tasksof']

        # Verify that the todo was updated
        response = requests.get(f"{BASE_URL}/{todo['id']}", headers=HEADERS_JSON)
        assert response.status_code == 200
        data = response.json()
        assert data['id'] == todo['id']
        assert data['title'] == new_todo['title']
        assert data['doneStatus'] == new_todo['doneStatus']
        assert data['description'] == new_todo['description']
        assert data['tasksof'] == todo['tasksof']

        # Verify that the initial data has not changed, excluding the modified todo
        response = requests.get(BASE_URL, headers=HEADERS_JSON)
        assert response.status_code == 200
        current_todos = response.json()
        initial_todos_excluding_modified = [t for t in self.initial_todos if t['id'] != todo['id']]
        assert all(todo in current_todos for todo in initial_todos_excluding_modified), "Initial todos have changed"

    def test_post_todo_id_xml(self):
        todo = random.choice(self.initial_todos["todos"])
        new_todo = {
            "title": "scan a lot of paperwork",
            "doneStatus": "true",
            "description": "this was tough",
        }
        response = requests.post(f"{BASE_URL}/{todo['id']}", json=new_todo, headers=HEADERS_XML)
        assert response.status_code == 200
        data = response.text
        assert '<todo>' in data
        assert '</todo>' in data
        assert f'<id>{todo["id"]}</id>' in data
        assert f'<title>{new_todo["title"]}</title>' in data
        assert f'<doneStatus>{new_todo["doneStatus"]}</doneStatus>' in data
        assert f'<description>{new_todo["description"]}</description>' in data
        assert '<tasksof>' in data
        assert '</tasksof>' in data

        # Verify that the todo was updated
        response = requests.get(f"{BASE_URL}/{todo['id']}", headers=HEADERS_JSON)
        assert response.status_code == 200
        data = response.json()
        assert data['id'] == todo['id']
        assert data['title'] == new_todo['title']
        assert data['doneStatus'] == new_todo['doneStatus']
        assert data['description'] == new_todo['description']
        assert data['tasksof'] == todo['tasksof']

        # Verify that the initial data has not changed, excluding the modified todo
        response = requests.get(BASE_URL, headers=HEADERS_JSON)
        assert response.status_code == 200
        current_todos = response.json()
        initial_todos_excluding_modified = [t for t in self.initial_todos if t['id'] != todo['id']]
        assert all(todo in current_todos for todo in initial_todos_excluding_modified), "Initial todos have changed"

    def test_post_todo_id_not_found(self):
        new_todo = {
            "title": "scan a lot of paperwork",
            "doneStatus": True,
            "description": "this was tough",
        }
        response = requests.post(f"{BASE_URL}/420", json=new_todo, headers=HEADERS_JSON)
        assert response.status_code == 404
        data = response.json()
        assert data == {'errorMessages': ['No such todo entity instance with GUID or ID 420 found']}

        # Verify that the initial data has not changed
        response = requests.get(BASE_URL, headers=HEADERS_JSON)
        assert response.status_code == 200
        current_todos = response.json()
        assert all(todo in current_todos for todo in self.initial_todos), "Initial todos have changed"

    def test_post_todo_id_removing_description(self):
        todo = random.choice(self.initial_todos["todos"])
        new_todo = {
            "title": "scan a lot of paperwork",
            "doneStatus": "true",
            "description": "",
        }

        response = requests.post(f"{BASE_URL}/{todo['id']}", json=new_todo, headers=HEADERS_JSON)
        assert response.status_code == 200
        data = response.json()
        assert data['id'] == todo['id']
        assert data['title'] == new_todo['title']
        assert data['doneStatus'] == new_todo['doneStatus']
        assert data['description'] == new_todo['description']
        assert data['tasksof'] == todo['tasksof']

        # Verify that the todo was updated
        response = requests.get(f"{BASE_URL}/{todo['id']}", headers=HEADERS_JSON)
        assert response.status_code == 200
        data = response.json()
        assert data['id'] == todo['id']
        assert data['title'] == new_todo['title']
        assert data['doneStatus'] == new_todo['doneStatus']
        assert data['description'] == new_todo['description']
        assert data['tasksof'] == todo['tasksof']

        # Verify that the initial data has not changed, excluding the modified todo
        response = requests.get(BASE_URL, headers=HEADERS_JSON)
        assert response.status_code == 200
        current_todos = response.json()
        initial_todos_excluding_modified = [t for t in self.initial_todos if t['id'] != todo['id']]
        assert all(todo in current_todos for todo in initial_todos_excluding_modified), "Initial todos have changed"

    def test_post_todo_id_removing_title(self):
        todo = random.choice(self.initial_todos["todos"])
        new_todo = {
            "title": "",
            "doneStatus": True,
            "description": "this was tough",
        }

        response = requests.post(f"{BASE_URL}/{todo['id']}", json=new_todo, headers=HEADERS_JSON)
        assert response.status_code == 400
        data = response.json()
        assert data == {'errorMessages': ['Failed Validation: title : can not be empty']}

        # Verify that the initial data has not changed
        response = requests.get(BASE_URL, headers=HEADERS_JSON)
        assert response.status_code == 200
        current_todos = response.json()
        assert all(todo in current_todos for todo in self.initial_todos), "Initial todos have changed"

    def test_post_todo_id_removing_tasksof_BUG(self):
        "Bug: API doesn't update the todo when tasksof is empty"
        todo = random.choice(self.initial_todos["todos"])
        new_todo = {
            "title": "scan a lot of paperwork",
            "doneStatus": "true",
            "description": "this was tough",
            "tasksof": []
        }

        response = requests.post(f"{BASE_URL}/{todo['id']}", json=new_todo, headers=HEADERS_JSON)
        assert response.status_code == 200
        data = response.json()
        assert data['id'] == todo['id']
        assert data['title'] == new_todo['title']
        assert data['doneStatus'] == new_todo['doneStatus']
        assert data['description'] == new_todo['description']
        assert data['tasksof'] == []

        # Verify that the todo was updated
        response = requests.get(f"{BASE_URL}/{todo['id']}", headers=HEADERS_JSON)
        assert response.status_code == 200
        data = response.json()
        assert data['tasksof'] == []

        # Verify that the initial data has not changed
        response = requests.get(BASE_URL, headers=HEADERS_JSON)
        assert response.status_code == 200
        current_todos = response.json()
        assert all(todo in current_todos for todo in self.initial_todos), "Initial todos have changed"

    def test_delete_todo_id(self):
        todo = random.choice(self.initial_todos["todos"])
        response = requests.delete(f"{BASE_URL}/{todo['id']}", headers=HEADERS_JSON)
        assert response.status_code == 200

        # Verify that the todo was deleted
        response = requests.get(f"{BASE_URL}/{todo['id']}", headers=HEADERS_JSON)
        assert response.status_code == 404
        data = response.json()
        assert data == {'errorMessages': ['Could not find an instance with todos/' + todo['id']]}

    def test_delete_todo_id_xml(self):
        todo = random.choice(self.initial_todos["todos"])
        response = requests.delete(f"{BASE_URL}/{todo['id']}", headers=HEADERS_XML)
        assert response.status_code == 200
        data = response.text

        # Verify that the todo was deleted
        response = requests.get(f"{BASE_URL}/{todo['id']}", headers=HEADERS_JSON)
        assert response.status_code == 404
        data = response.json()
        assert data == {'errorMessages': ['Could not find an instance with todos/' + todo['id']]}

    def test_delete_todo_id_not_found(self):
        response = requests.delete(f"{BASE_URL}/420", headers=HEADERS_JSON)
        assert response.status_code == 404
        data = response.json()
        assert data == {'errorMessages': ['Could not find any instances with todos/420']}

        # Verify that the initial data has not changed
        response = requests.get(BASE_URL, headers=HEADERS_JSON)
        assert response.status_code == 200
        current_todos = response.json()
        assert all(todo in current_todos for todo in self.initial_todos), "Initial todos have changed"

    def test_todos_id_tasksof_not_found_BUG(self):
        "Bug: API returns 200 instead of 404 when the todo is not found"
        response = requests.get(f"{BASE_URL}/420/tasksof", headers=HEADERS_JSON)
        assert response.status_code == 404
        data = response.json()
        assert data == {'errorMessages': ['Could not find an instance with todos/420']}