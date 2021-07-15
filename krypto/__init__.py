import os
import pathlib

import click

token = os.getenv("GITHUB_PERSONAL_TOKEN")
assert token is not None

__version__ = "0.1.0"

from krypto.todo import parse
from krypto.github import create_issues

# TODO[Enhancement]: Make config file
# Sometimes you might wanna have TODOs in your tests.
# Right now krypto will completely ignore any file with the
# substring "test" in the path. I would want to be able to
# configure this behaviour.


# TODO[Enhancement]: Allow for different standard labels to be attached to the issues
# Mayhap I would like to assign a todo certain labels like `Enhancement`
# Possible syntax `# Enhancement: title here`
# or maybe `# TODO[Enhancement]: title here`


# TODO: Possible creation of pre-push git hook
# Think about making this into a git script to
# hook into the pre-push action instead of having to run
# the script manually


@click.command()
@click.argument("path")
def run(path):
    todos = []
    for file in pathlib.Path(path).glob("**/*py"):
        if "test" not in str(file):
            with open(file) as f:
                lst = parse(f.read(), file)
                if lst:
                    todos.extend(lst)

    failed = create_issues(todos, token=token)
    if todos:
        print("Finished creating issues!")
    if failed:
        print("Some issues have failed")
        for todo in failed:
            print(todo.title)
