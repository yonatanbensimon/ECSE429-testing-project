#Script to run all tests
import os
import pytest

ospath = os.path.dirname(os.path.dirname(__file__))

pytest.main([f"{ospath}/UnitTestSuite/Project/projectEndpoint.py", f"{ospath}/UnitTestSuite/Todo/todoEndpoint.py"])