import tomli


class PyProjectNotFound(Exception):
    ...


DEFAULTS = {"prefix": "TODO", "attach-issue": False}


class Config:
    def __init__(self, config: str):
        self.config_file = config

    def parse(self) -> dict:
        if "pyproject.toml" in str(self.config_file):
            try:
                with open(self.config_file) as config:
                    found = tomli.load(config)["tool"]["krypto"]
                    return {**DEFAULTS, **found}
            except (KeyError, FileNotFoundError):
                return DEFAULTS
        raise PyProjectNotFound("pyproject.toml selected but not found")
