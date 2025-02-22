#Script to run all tests
import os
import random
import subprocess
import pytest

ospath = os.path.dirname(os.path.dirname(__file__))

status = input("Is the Manager API already running? (Y/N): ")

if status == "N":
    pathh = f"{ospath}/ApplicationBeingTested/runTodoManagerRestAPI-1.5.5.jar"
    process = subprocess.Popen(["java", "-jar", pathh]) 
elif status != "Y":
    raise ValueError("Status should be Y or N")

#Regular
pytest.main([f"{ospath}/UnitTestSuite/Project/projectEndpoint.py", f"{ospath}/UnitTestSuite/Todo/todoEndpoint.py", "-vv"])

if status == "N":
    process.terminate()
    process.wait()

