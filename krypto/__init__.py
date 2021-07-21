import os

__version__ = "0.1.0"

token = os.getenv("TOKEN_GITHUB")
assert token is not None


from krypto.cli import cli as cli


# TODO[Enhancement]: Make config file @https://github.com/antoniouaa/krypto/issues/15
# Sometimes you might wanna have TODOs in your tests.
# Right now krypto will completely ignore any file with the
# test substring in the title. I want to be able to configure this behaviour.
# Perhaps read from pyproject.toml?
