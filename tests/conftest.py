import pathlib

import pytest

from krypto.todo import Todo


username = "antoniouaa"
repository = "krypto"


@pytest.fixture(scope="function")
def sample_todo():
    info = {
        "title": "This is a sample title",
        "body": "this is the body of the todo",
        "labels": ["Enhancement", "Bug"],
        "line_no": 10,
        "origin": pathlib.Path("."),
    }
    return Todo(**info)
