#Script to run all tests
import os
import random
import subprocess
import sys
import requests
import time
from behave.__main__ import Configuration, run_behave, Runner

ospath = os.path.dirname(os.path.dirname(__file__))
BASE_URL = "http://localhost:4567"

def shutdown_system():
    """Shutdown the API to reset the system state."""
    try:
        requests.post("http://localhost:4567/shutdown")
    except requests.exceptions.RequestException:
        pass

def start_system():
    """Start the API to prepare for testing."""
    try:
        # Check if the API is already running
        response = requests.get(BASE_URL, timeout=2)
        if response.status_code == 200:
            print("Server is already running. Skipping startup.")
            return None  # No need to start a new instance
    except requests.exceptions.RequestException:
        pass  # Server is not running, so proceed with startup

    print("Starting the server...")
    process = subprocess.Popen(["java", "-jar", f"{ospath}/ApplicationBeingTested/runTodoManagerRestAPI-1.5.5.jar"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # Wait for the server to be ready
    while True:
        try:
            response = requests.get(BASE_URL, timeout=2)
            if response.status_code == 200:
                print("Server is ready!")
                break
        except requests.exceptions.RequestException:
            time.sleep(1)  # Wait before retrying

    return process

class ShuffleRunner(Runner):

    def feature_locations(self):
        locations = super().feature_locations()
        random.shuffle(locations)
        return locations
    
def main():
    status = input("Is the Manager API already running? (Y/N): ")

    if status == "N":
        pathh = f"{ospath}/ApplicationBeingTested/runTodoManagerRestAPI-1.5.5.jar"
        process = subprocess.Popen(["java", "-jar", pathh]) 
    elif status != "Y":
        raise ValueError("Status should be Y or N")
    
    config = Configuration()
    exit_code = run_behave(config, runner_class=ShuffleRunner)

    if status == "N":
        process.terminate()
        process.wait()

    return exit_code

if __name__ == "__main__":
    sys.exit(main())

