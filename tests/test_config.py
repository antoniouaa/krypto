import pytest

from krypto.config import Config, DEFAULTS, PyProjectNotFound
from tests.conftest import sample_config


def test_config(tmp_path):
    pyproject = tmp_path / "pyproject.toml"
    pyproject.write_text(
        """
[tool.krypto]
comment = "#"
prefix = "TODO"
include = "tests"
attach-issue = false
    """.strip()
    )

    config = Config(pyproject)

    test_config = sample_config
    del test_config["dry"]
    del test_config["username"]
    del test_config["repository"]

    assert config.parse() == test_config


def test_config_malformed(tmp_path):
    pyproject = tmp_path / "pyproject.toml"
    pyproject.write_text(
        """
[tool.kry]
prefix = "TODO"
include = "tests"
attach-issue = false
    """.strip()
    )

    config = Config(pyproject)

    assert config.parse() == DEFAULTS


def test_config_not_found(tmp_path):
    pyproject = tmp_path

    config = Config(pyproject)

    with pytest.raises(PyProjectNotFound):
        config.parse()
