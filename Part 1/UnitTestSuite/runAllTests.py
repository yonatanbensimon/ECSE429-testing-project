#Script to run all tests
import pytest
import projectEndpoint
import todoEndpoint

pytest.main(projectEndpoint, todoEndpoint)