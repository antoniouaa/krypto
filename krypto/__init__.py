import os

__version__ = "0.1.0"

token = os.getenv("TOKEN_GITHUB")
assert token is not None


from krypto.cli import run as run


# TODO[Enhancement]: Make config file - https://github.com/antoniouaa/krypto/issues/15
# Sometimes you might wanna have TODOs in your tests.
# Right now krypto will completely ignore any file with the
# configure this behaviour. Perhaps read from pyproject.toml?


# TODO[Enhancement, Bug]: Allow for different standard labels to be attached to the issues - https://github.com/antoniouaa/krypto/issues/23
# Mayhap I would like to assign a todo certain labels like `Enhancement`
# Possible syntax `# Enhancement: title here`
# or maybe `# TODO[Enhancement]: title here`
# Labels are overwritten right now instead of extended
