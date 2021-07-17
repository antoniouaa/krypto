import tomli


class PyProjectNotFound(Exception):
    ...


class Config:
    def __init__(self, cwd: str, config: str):
        self.cwd = cwd
        self.config_file = config

    def parse(self):
        try:
            with open(self.config_file) as config:
                return tomli.load(config)["tool"]["krypto"]
        except FileNotFoundError:
            if self.config_file == "pyproject.toml":
                raise PyProjectNotFound("pyproject.toml selected but not found")
            raise PyProjectNotFound("Config file not found")
