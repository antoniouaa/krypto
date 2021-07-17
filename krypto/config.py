import tomli


class PyProjectNotFound(Exception):
    ...


DEFAULTS = {"prefix": "TODO", "attach-issue": False}


class Config:
    def __init__(self, config: str):
        self.config_file = config

    def parse(self) -> dict:
        if self.config_file == "pyproject.toml":
            try:
                with open(self.config_file) as config:
                    return tomli.load(config)["tool"]["krypto"]
            except KeyError:
                return DEFAULTS
        raise PyProjectNotFound("pyproject.toml selected but not found")
