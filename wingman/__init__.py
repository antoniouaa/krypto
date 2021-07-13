import pathlib
import os

import dotenv
import click

dotenv.load_dotenv()
token = os.getenv("GITHUB_PERSONAL_TOKEN")

__version__ = "0.1.0"

from wingman.todo import parse as parse


@click.command()
@click.argument("path")
def run(path):
    todos = {}
    for file in pathlib.Path(path).glob("**/*py"):
        if "test" not in str(file):
            with open(file) as f:
                todo = parse(f.read(), file)
                if todo:
                    todos[str(file)] = todo
    print(todos)
