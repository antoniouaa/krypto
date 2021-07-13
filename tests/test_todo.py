from wingman import todo as TODO


def test_todo():
    test_program = """
def test_func(*args, **kwargs):
    # TODO: Implement this function
"""
    todos = TODO.parse(test_program)
    assert len(todos) == 1
    assert todos[0].title == "Implement this function"


def test_todo_many():
    test_program = """
def test_func(*args, **kwargs):
    # TODO: Implement this function
    # TODO: Check if the assertions pass
"""
    todos = TODO.parse(test_program)
    print(todos)
    assert len(todos) == 2
    assert todos[0].title == "Implement this function"
    assert todos[1].title == "Check if the assertions pass"


def test_todo_with_body():
    test_program = """
def test_func(*args, **kwargs):
    # TODO: Implement this function
    # This function should perform some task
    # and return some output
"""
    todos = TODO.parse(test_program)
    assert len(todos) == 1
    todo = todos[0]
    print(todo)
    assert todo.title == "Implement this function"
    assert todo.body == "This function should perform some task\nand return some output"
