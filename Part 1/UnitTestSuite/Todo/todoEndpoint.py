#Todo Test
import pytest as pt

class TesttodoEndpoint:
    def test_todo_example(self):
        with pt.raises(ZeroDivisionError):
            return 5 / 0