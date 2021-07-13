import os
import pathlib

import dotenv
import click

dotenv.load_dotenv()
token = os.getenv("GITHUB_PERSONAL_TOKEN")

from wingman.todo import parse as parse


@click.command()
@click.argument("path")
def run(path):
    todos = {}
    for file in pathlib.Path(path).glob("**/*py"):
        with open(file) as f:
            todo = parse(f.read(), file)
            if todo:
                todos[str(file)] = todo
    print(todos)


if __name__ == "__main__":
    run()
