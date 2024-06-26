import os

__version__ = "0.1.0"

token = os.getenv("KRYPTO_TOKEN")
assert token is not None


from krypto.cli import cli as cli


# TODO[Enhancement]: Make config file
# Sometimes you might wanna have TODOs in your tests.
# Right now krypto will completely ignore any file with the
# test substring in the title. I want to be able to configure this behaviour.
# Perhaps read from pyproject.toml?


# TODO[Enhancement]: Allow specifying branch name
# When krypto creates an issue and attaches a link to the todo locally,
# it only considers todos in the master branch. It would be nice to be able
# to either specify which branch you're on or have krypto automatically
# figure it out and adjust links.


# TODO[Bug]: CLI tests failing
# Click is just being annoying with the testing
