from wingman import todo


def test_todo():
    test_program = """
def test_func(*args, **kwargs):
    # TODO: Implement this function
"""
    todos = todo.parse(test_program)
    assert len(todos) == 1


def test_todo_many():
    test_program = """
def test_func(*args, **kwargs):
    # TODO: Implement this function
    # TODO: Check if the assertions pass
"""
    todos = todo.parse(test_program)
    assert len(todos) == 2
    assert todos[0].title == "Implement this function"
    assert todos[1].title == "Check if the assertions pass"
