#Project Endpoint Tests
import pytest as pt

class projectEndpoint:
    def test_project_example(self):
        with pt.raises(ZeroDivisionError):
            return 5 / 0