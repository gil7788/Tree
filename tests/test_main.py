# test_my_script.py
import pytest
from src.script import main


@pytest.mark.parametrize(
    "test_input,expected", [
        (["--string", "hello", "--integer", "1", "-v"], "Received string: hello, Received integer: 1, Verbose: on"),
        (["--string", "hello", "--integer", "1"], "Received string: hello, Received integer: 1, Verbose: off"),
        (["--string", "world", "--integer", "2", "-v"], "Received string: world, Received integer: 2, Verbose: on"),
        (["--string", "world", "--integer", "2"], "Received string: world, Received integer: 2, Verbose: off"),
        (["--string", "test", "-v"], "Received string: test, Received integer: 0, Verbose: on"),
        (["--string", "test"], "Received string: test, Received integer: 0, Verbose: off"),
        (["--integer", "3", "-v"], "Received string: , Received integer: 3, Verbose: on"),
        (["--integer", "3"], "Received string: , Received integer: 3, Verbose: off"),
    ]
)
def test_process_arguments(test_input, expected):
    assert main(test_input) == expected
