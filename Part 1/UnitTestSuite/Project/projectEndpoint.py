#Project Endpoint Tests
import os
import subprocess
import pytest as pt
import requests

class TestGETProject:
    @pt.fixture(autouse=True)
    def setupAndTeardown(self):
        "Ensures the system is ready to be tested by setting up and tearing down the Manager after every test"
        ospath = os.path.dirname(os.path.dirname(__file__))
        pathh = f"{ospath}/ApplicationBeingTested/runTodoManagerRestAPI-1.5.5.jar"
        process = subprocess.Popen(["java", "-jar", pathh])

        yield

        process.terminate()
        process.wait()

    def test_correct_project_json(self):
        "Verifies that GET all projects runs correctly in JSON format"
        url = "http://localhost:4567/projects"
        response = requests.get(url, headers={"Accept": "application/json"})

        assert response.status_code == 200
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
                        {"id": "1"},
                        {"id": "2"}
                    ]
                }
            ]
        }

        assert data == expected_data, f'The expected response was {expected_data}, but the following data was received {data}'