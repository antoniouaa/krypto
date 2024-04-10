import responses

from krypto.github import (
    construct_url,
    patch_issue,
    post_issue,
    prepare_body,
    get_basename,
    filter_issues,
)

from tests.conftest import username, repository, headers, todo_from_json, url


def test_request_body_all_fields(sample_todo):
    body = prepare_body(sample_todo, username=username, repository=repository)
    assert isinstance(body, dict)
    assert body["title"] == sample_todo.title
    assert body["labels"] == sample_todo.labels
    assert str(sample_todo.origin).replace("\\", "/") in body["body"]


def test_request_body_no_body(sample_todo):
    sample_todo.body = ""
    body = prepare_body(sample_todo, username=username, repository=repository)
    assert isinstance(body, dict)
    assert body["title"] == sample_todo.title
    assert body["labels"] == sample_todo.labels
    assert (
        "Autogenerated by [antoniouaa/krypto](https://github.com/antoniouaa/krypto)"
        in body["body"]
    )


def test_basename():
    username, repository = get_basename()

    assert username == "antoniouaa"
    assert repository == "krypto"


def test_construct_url():
    url = construct_url(username, repository)

    assert url == "https://api.github.com/repos/antoniouaa/krypto/issues"


def test_filter_issues(sample_todo):
    with responses.RequestsMock() as mock_requests:
        mock_requests.add(
            responses.GET,
            f"{url}?state=all",
            json=todo_from_json,
            status=200,
        )
        response = filter_issues(url, headers=headers, todos=[sample_todo])

        assert response == [sample_todo]


def test_post_issue(sample_todo):
    json = prepare_body(sample_todo, username=username, repository=repository)
    response_json = {**json, "number": 1}
    with responses.RequestsMock() as mock_requests:
        mock_requests.add(
            responses.POST,
            url,
            json=response_json,
            status=201,
        )
        response = post_issue(url, headers=headers, json=json)
        assert response == (json["title"], True, 1)


def test_patch_issue(sample_todo):
    json = prepare_body(sample_todo, username=username, repository=repository)
    issue_no = 1
    with responses.RequestsMock() as mock_requests:
        mock_requests.add(
            responses.PATCH,
            f"{url}/{issue_no}",
            json=json,
            status=200,
        )
        response = patch_issue(url, headers=headers, json=json, issue_no=issue_no)
        assert response == (json["title"], True)
