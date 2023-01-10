import pytest

def test_upper():
    string = 'hello'
    upper = string.upper()

    assert upper == 'HELLO'
