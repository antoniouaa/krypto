import os
import pathlib

__version__ = "0.1.0"

import click

token = os.getenv("TOKEN_GITHUB")
assert token is not None

from krypto.todo import parse
from krypto.github import main


# TODO[Enhancement]: Make config file
# Sometimes you might wanna have TODOs in your tests.
# Right now krypto will completely ignore any file with the
# substring "test" in the path. I would want to be able to
# configure this behaviour.

# TODO[Enhancement, Bug]: Allow for different standard labels to be attached to the issues
# Mayhap I would like to assign a todo certain labels like `Enhancement`
# Possible syntax `# Enhancement: title here`
# or maybe `# TODO[Enhancement]: title here`
# Labels are overwritten right now instead of extended

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

    successful, failed = main(token, todos)
    click.echo("Finished creating issues!")
    if successful:
        click.echo("\nIssues successfully created/updated:")
        for title in successful:
            click.echo(f"\t- {title}")
    if failed:
        click.echo("\nSome issues have failed:")
        for title in failed:
            click.echo(f"\t- {title}")
