from krypto.todo import parse

from tests.conftest import sample_config, sample_symbols


def test_todo_empty_brackets():
    test_program = """
def test_func(*args, **kwargs):
    # TODO[]: Implement this function
"""
    todos = parse(test_program, extension="py")
    assert len(todos) == 1
    assert todos[0].title == "Implement this function"
    assert todos[0].labels == []


def test_todo_one_label():
    test_program = """
def test_func(*args, **kwargs):
    # TODO[Enhancement]: Implement this function
"""
    todos = parse(test_program, extension="py")
    assert len(todos) == 1
    assert todos[0].labels == ["Enhancement"]
    assert todos[0].title == "Implement this function"


def test_todo_no_labels():
    test_program = """
def test_func(*args, **kwargs):
    # TODO: Implement this function
"""
    todos = parse(test_program, extension="py")
    assert len(todos) == 1
    assert todos[0].labels == []
    assert todos[0].title == "Implement this function"


def test_todo_many_labels():
    test_program = """
def test_func(*args, **kwargs):
    # TODO[Enhancement, Bug, Feature]: Implement this function
"""
    todos = parse(test_program, extension="py")
    assert len(todos) == 1
    assert todos[0].labels == ["Enhancement", "Bug", "Feature"]
    assert todos[0].title == "Implement this function"


def test_todo_label_separator():
    test_program = """
def test_func(*args, **kwargs):
    # TODO[Enhancement - Bug - Feature]: Implement this function
    # TODO[Enhancement / Bug / Feature]: Implement this function
    # TODO[Enhancement # Bug # Feature]: Implement this function
    # TODO[Enhancement ~ Bug ~ Feature]: Implement this function
    # TODO[Enhancement \\ Bug \\ Feature]: Implement this function
"""
    todos = parse(test_program, extension="py")
    for todo in todos:
        assert todo.labels == ["Enhancement", "Bug", "Feature"]
        assert todo.title == "Implement this function"


def test_todo_mixed_separator():
    test_program = """
def test_func(*args, **kwargs):
    # TODO[Enhancement / Bug - Feature]: Implement this function
    # TODO[Enhancement#Bug / Feature]: Implement this function
    # TODO[Enhancement#Bug,Feature]: Implement this function
    # TODO[Enhancement\\Bug ~Feature]: Implement this function
    # TODO[Enhancement\\Bug\\Feature]: Implement this function
"""

    todos = parse(test_program, extension="py")
    for todo in todos:
        assert todo.labels == ["Enhancement", "Bug", "Feature"]
        assert todo.title == "Implement this function"
