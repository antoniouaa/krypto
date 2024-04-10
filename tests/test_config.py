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
src = "krypto"
include = "tests"
attach-issue = false
    """.strip()
    )

    config = Config(pyproject)

    test_config_dict = sample_config
    del test_config_dict["dry"]
    del test_config_dict["username"]
    del test_config_dict["repository"]

    assert config.parse() == test_config_dict


def test_config_malformed(tmp_path):
    pyproject = tmp_path / "pyproject.toml"
    pyproject.write_text(
        """
[tool.kry]
prefix = "TODO"
src = "krypto"
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
