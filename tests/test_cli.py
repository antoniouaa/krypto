import pathlib

import responses
from click.testing import CliRunner

from krypto.cli import IssueRunner, run, install
from krypto.github import prepare_body
from tests.conftest import (
    sample_config,
    username,
    repository,
    url,
    todo_from_json,
    raw_todo,
)


def test_runner():
    runner = IssueRunner(
        "./tests",
        pathlib.Path.cwd(),
        config=sample_config,
    )
    assert runner.cwd.parts[-1] == "krypto"
    assert runner.config["username"] == username
    assert runner.config["repository"] == repository
    assert runner.todos == []

    assert str(runner) == "Runner: cwd@krypto\n0 todos"


def test_runner_requests(mock_requests, sample_todo):
    runner = IssueRunner(
        "./tests",
        pathlib.Path.cwd(),
        config={**sample_config, "dry": False},
    )

    todo = sample_todo
    todo.issue_no = 1
    runner.todos = [todo]

    json = prepare_body(sample_todo, username=username, repository=repository)
    mock_requests.add(
        responses.GET,
        f"{url}?state=all",
        json=todo_from_json,
        status=200,
    )
    mock_requests.add(
        responses.PATCH,
        f"{url}/1",
        json=json,
        status=200,
    )
    response = runner.run("token")

    assert len(response) == 2
    assert response[0] == [sample_todo.title]
    assert response[1] == []


def test_click_install(tmp_path):
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(install)

        assert "Installing" in result.output
        assert "New pre-push hook installed!" in result.output
