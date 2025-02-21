#Project Endpoint Tests
import time
import pytest as pt
import requests

def wait_for_system(url, timeout=1, interval=0.5):
    start = time.time()
    while time.time() - start < timeout:
        try:
            response = requests.get(url, verify=False)
            if response.status_code == 200:
                return True
        except requests.RequestException:
            pass
        time.sleep(interval)
    raise RuntimeError(f"System did not become ready within {timeout} seconds.")

@pt.fixture(autouse = True, scope="function")
def is_system_ready():
    #Ensure the system is ready to be tested
    wait_for_system("http://localhost:4567/projects")
    yield

class TestProject:
    def test_GET_correct_project_json(self):
        "Verifies that GET all projects runs correctly in JSON format"
        
        url = "http://localhost:4567/projects"
        response = requests.get(url, headers={"Accept": "application/json"}, verify=False)

        assert response.status_code == 200, f"The status code is {response.status_code} instead of 200"
        data = response.json()
        expected_data = {
            "projects": [
                {
                    "id": "1",
                    "title": "Office Work",
                    "completed": "false",
                    "active": "false",
                    "description": "",
                    "tasks": [
                        {"id": "2"},
                        {"id": "1"}
                    ]
                }
            ]
        }

        expected_data2 = {
            "projects": [
                {
                    "id": "1",
                    "title": "Office Work",
                    "completed": "false",
                    "active": "false",
                    "description": "",
                    "tasks": [
                        {"id": "1"},
                        {"id": "2"}
                    ]
                }
            ]
        }

        assert (data == expected_data) or (data == expected_data2), f'The expected response was {expected_data}, but the following data was received {data}'

    def test_GET_correct_project_XML(self):
        "Verifies that GET all projects runs correctly in XML format"
        url = "http://localhost:4567/projects"
        response = requests.get(url, headers={"Accept": "application/xml"}, verify=False)

        assert response.status_code == 200, f"The status code is {response.status_code} instead of 200"
        data = response.content.decode('utf-8')
        expected_data = "<projects><project><active>false</active><description/><id>1</id><completed>false</completed><title>Office Work</title><tasks><id>2</id></tasks><tasks><id>1</id></tasks></project></projects>"
        expected_data2 = "<projects><project><active>false</active><description/><id>1</id><completed>false</completed><title>Office Work</title><tasks><id>1</id></tasks><tasks><id>2</id></tasks></project></projects>"


        assert (data == expected_data) or (data == expected_data2), f'The expected response was {expected_data}, but the following data was received {data}'
    
    def test_POST_project_json(self):
        "Verifies that a project is succesfully created with no attributes"
        url = "http://localhost:4567/projects"
        response = requests.post(url, headers={"Accept": "application/json"}, verify=False)

        data = response.json()
        expected_data = {
            "id": "2",
            "title": "",
            "completed": "false",
            "active": "false",
            "description": ""
        }

        #Teardown
        url = "http://localhost:4567/projects/2"
        requests.delete(url, headers={"Accept": "application/json"}, verify=False)

        assert response.status_code == 201, f"The status code is {response.status_code} instead of 201"
        assert data == expected_data, f'The expected response was {expected_data}, but the following data was received {data}'

    def test_POST_project_with_title_json(self):
        "Verifies that a project is succesfully created with a title attribute"
        url = "http://localhost:4567/projects?title=project"
        response = requests.post(url, headers={"Accept": "application/json"}, verify=False)

        data = response.json()
        expected_data = {
            "id": "2",
            "title": "project",
            "completed": "false",
            "active": "false",
            "description": ""
        }

        #Teardown
        url = "http://localhost:4567/projects/2"
        requests.delete(url, headers={"Accept": "application/json"}, verify=False)

        assert response.status_code == 201, f"The status code is {response.status_code} instead of 201"
        assert data == expected_data, f'The expected response was {expected_data}, but the following data was received {data}'
    
    def test_DELETE_project(self):
        "UNDOCUMENTED - Verifies that all projects are deleted when running delete on project"
        url = "http://localhost:4567/projects"
        response = requests.delete(url, headers={"Accept": "application/json"}, verify=False)

        assert response.status_code == 200, f"The status code is {response.status_code} instead of 200"

        response = requests.get(url, headers={"Accept": "application/xml"}, verify=False)
        data = response.json()

        assert data == ""

class TestProjectID:
    def test_GET_existing_project_json(self):
        "Verifies that a project with an existing ID is succesfully retrieved in JSON"
        url = "http://localhost:4567/projects/1"
        response = requests.get(url, headers={"Accept": "application/json"}, verify=False)

        assert response.status_code == 200, f"The status code is {response.status_code} instead of 200"

        data = response.json()
        expected_data = {
            "projects": [
                {
                    "id": "1",
                    "title": "Office Work",
                    "completed": "false",
                    "active": "false",
                    "description": "",
                    "tasks": [
                        {"id": "2"},
                        {"id": "1"}
                    ]
                }
            ]
        }

        expected_data2 = {
            "projects": [
                {
                    "id": "1",
                    "title": "Office Work",
                    "completed": "false",
                    "active": "false",
                    "description": "",
                    "tasks": [
                        {"id": "1"},
                        {"id": "2"}
                    ]
                }
            ]
        }

        assert (data == expected_data) or (data == expected_data2), f'The expected response was {expected_data}, but the following data was received {data}'

    def test_GET_existing_project_XML(self):
        "Verifies that a project with an existing ID is succesfully retrieved in XML"
        url = "http://localhost:4567/projects/1"
        response = requests.get(url, headers={"Accept": "application/xml"}, verify=False)

        assert response.status_code == 200, f"The status code is {response.status_code} instead of 200"
        data = response.content.decode('utf-8')
        expected_data = "<projects><project><active>false</active><description/><id>1</id><completed>false</completed><title>Office Work</title><tasks><id>2</id></tasks><tasks><id>1</id></tasks></project></projects>"
        expected_data2 = "<projects><project><active>false</active><description/><id>1</id><completed>false</completed><title>Office Work</title><tasks><id>1</id></tasks><tasks><id>2</id></tasks></project></projects>"


        assert (data == expected_data) or (data == expected_data2), f'The expected response was {expected_data}, but the following data was received {data}'

    def test_GET_nonexisting_project_JSON(self):
        "Verifies that a project with an non existing ID is not retrieved"
        url = "http://localhost:4567/projects/2"
        response = requests.get(url, headers={"Accept": "application/json"}, verify=False)

        assert response.status_code == 404, f"The status code is {response.status_code} instead of 404"

        data = response.json()
        expected_response = {
            "errorMessages": [
                "Could not find an instance with projects/2"
            ]
        }

        assert data == expected_response, f'The expected response was {expected_response}, but the following data was received {data}'

    def test_HEAD_existing_project(self):
        "Verifies that a project header is successfully retrieved"
        url = "http://localhost:4567/projects/1"
        response = requests.head(url, headers={"Accept": "application/json"}, verify=False)
        assert response.status_code == 200, f"The status code is {response.status_code} instead of 200"
    
    def test_PUT_existing_project(self):
        "Verifies that an existing project description is succesfully modified"
        url = "http://localhost:4567/projects"
        requests.post(url)

        url = "http://localhost:4567/projects/2?description=Hi"
        response = requests.put(url, headers={"Accept": "application/json"}, verify=False)

        data = response.json()
        expected_data = {
                "id": "2",
                "title": "",
                "completed": "false",
                "active": "false",
                "description": "Hi",
        }

        url = "http://localhost:4567/projects/2"
        requests.delete(url)

        assert response.status_code == 200, f"The status code is {response.status_code} instead of 200"
        assert (data == expected_data), f'The expected response was {expected_data}, but the following data was received {data}'

class TestProjectIDTask:
    def test_GET_task_existing_project_json(self):
        "Verifies that tasks from a project with an existing ID is succesfully retrieved in JSON"
        url = "http://localhost:4567/projects/1/tasks"
        response = requests.get(url, headers={"Accept": "application/json"}, verify=False)

        assert response.status_code == 200, f"The status code is {response.status_code} instead of 200"

        data = response.json()
        expected_data = {  
            "todos": [
                {
                    "id": "2",
                    "title": "file paperwork",
                    "doneStatus": "false",
                    "description": "",
                    "tasksof": [
                        {
                            "id": "1"
                        }
                    ]
                },
                {
                    "id": "1",
                    "title": "scan paperwork",
                    "doneStatus": "false",
                    "description": "",
                    "categories": [
                        {
                            "id": "1"
                        }
                    ],
                    "tasksof": [
                        {
                            "id": "1"
                        }
                    ]
                }
            ]
        }

        expected_data2 = {  
            "todos": [
                {
                    "id": "1",
                    "title": "scan paperwork",
                    "doneStatus": "false",
                    "description": "",
                    "categories": [
                        {
                            "id": "1"
                        }
                    ],
                    "tasksof": [
                        {
                            "id": "1"
                        }
                    ]
                },
                {
                    "id": "2",
                    "title": "file paperwork",
                    "doneStatus": "false",
                    "description": "",
                    "tasksof": [
                        {
                            "id": "1"
                        }
                    ]
                }
            ]
        }

        assert (data == expected_data) or (data == expected_data2), f'The expected response was {expected_data}, but the following data was received {data}'

    def test_GET_existing_project_XML(self):
        "Verifies that tasks from a project with an existing ID is succesfully retrieved in XML"
        url = "http://localhost:4567/projects/1/tasks"
        response = requests.get(url, headers={"Accept": "application/xml"}, verify=False)

        assert response.status_code == 200, f"The status code is {response.status_code} instead of 200"
        data = response.content.decode('utf-8')
        expected_data = "<todos><todo><doneStatus>false</doneStatus><description/><tasksof><id>1</id></tasksof><id>1</id><categories><id>1</id></categories><title>scan paperwork</title></todo><todo><doneStatus>false</doneStatus><description/><tasksof><id>1</id></tasksof><id>2</id><title>file paperwork</title></todo></todos>"
        expected_data2 = "<todos><todo><doneStatus>false</doneStatus><description/><tasksof><id>1</id></tasksof><id>2</id><title>file paperwork</title></todo><todo><doneStatus>false</doneStatus><description/><tasksof><id>1</id></tasksof><id>1</id><categories><id>1</id></categories><title>scan paperwork</title></todo></todos>"

        assert (data == expected_data) or (data == expected_data2), f'The expected response was {expected_data}, but the following data was received {data}'

    def test_GET_tasks_non_existing_project(self):
        "Verifies that a 404 error is thrown when tasks of a project with a non existing ID is requested"
        url = "http://localhost:4567/projects/2/tasks"
        response = requests.get(url, headers={"Accept": "application/json"}, verify=False)

        assert response.status_code == 404, f"The status code is {response.status_code} instead of 404"

    def test_GET_task_from_project_task_id(self):
        "UNDOCUMENTED Verifies that a task is succesfuly retrieved from a project with a task ID"
        url = "http://localhost:4567/projects/1/tasks/1"
        response = requests.get(url, headers={"Accept": "application/json"}, verify=False)

        assert response.status_code == 200, f"The status code is {response.status_code} instead of 200"
        
        data = response.json()
        expected_data = {
                    "id": "1",
                    "title": "scan paperwork",
                    "doneStatus": "false",
                    "description": "",
                    "categories": [
                        {
                            "id": "1"
                        }
                    ],
                    "tasksof": [
                        {
                            "id": "1"
                        }
                    ]
                }

        assert (data == expected_data), f'The expected response was {expected_data}, but the following data was received {data}'