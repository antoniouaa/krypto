import pytest

from krypto.todo import parse, TODOError


def test_todo_numbers_in_label():
    test_program = """
def test_func(*args, **kwargs):
    # TODO[123]: title
    # body of todo
"""
    with pytest.raises(TODOError):
        parse(test_program)


def test_todo_bad_brackets():
    parens = """
def test_func(*args, **kwargs):
    # TODO(Bug, Enhancement): title
    # body of todo
"""
    with pytest.raises(TODOError):
        parse(parens)

    curly = """
def test_func(*args, **kwargs):
    # TODO(Bug, Enhancement): title
    # body of todo
"""
    with pytest.raises(TODOError):
        parse(curly)
