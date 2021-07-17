import shlex
import pathlib
import platform
import subprocess
from typing import List, Tuple

import requests

from krypto.todo import Todo

BASE_URL = "https://api.github.com"
ISSUES_URL = "/repos/{}/{}/issues"
ACCEPT = {"Accept": "application/vnd.github.v3+json"}
ALL_ISSUES = {"state": "all"}


def get_basename() -> Tuple[str, str]:
    plat = platform.system()
    if plat == "Windows":
        basename = subprocess.run(
            shlex.split("powershell.exe git remote get-url origin"), capture_output=True
        )
    else:
        basename = subprocess.run(
            shlex.split("git remote get-url origin"), capture_output=True
        )
    path = pathlib.Path(basename.stdout.decode().strip(" \n.git"))
    *_, username, repository = path.parts
    return username, repository


def prepare_body(todo: Todo, username: str, repository: str) -> dict:
    if todo.body:
        issue_body = f"{todo.body}"
    else:
        issue_body = (
            "Autogenerated by [antoniouaa/krypto](https://github.com/antoniouaa/krypto)"
        )
    normalised_origin = str(todo.origin).replace("\\", "/")
    return {
        "title": todo.title,
        "body": issue_body
        + f"\n\nLine: {todo.line_no} in [`{todo.origin}`](https://github.com/{username}/{repository}/blob/master/{normalised_origin}#L{todo.line_no})",
        "labels": todo.labels,
    }


def construct_url(username: str, repository: str) -> str:
    return BASE_URL + ISSUES_URL.format(username, repository)


def post_issue(url: str, headers: dict, json: dict) -> Tuple[str, bool]:
    response = requests.post(url, headers=headers, json=json)
    return json["title"], response.status_code == 201


def patch_issue(url: str, headers: dict, json: dict, issue_no: int) -> Tuple[str, bool]:
    url = f"{url}/{issue_no}"
    response = requests.patch(url, headers=headers, json=json)
    return json["title"], response.status_code == 200


def filter_issues(
    url: str,
    headers: dict,
    todos: List[Todo],
    issue_state: dict = ALL_ISSUES,
) -> List[Todo]:
    response = requests.get(url, headers=headers, params=issue_state)
    existing = {
        issue["title"].lower(): issue
        for issue in response.json()
        if issue["state"] != "closed"
    }
    filtered = []
    for todo in todos:
        title = todo.title.lower()
        if title in existing:
            todo.issue_no = existing[title]["number"]
            labels = [label["name"] for label in existing[title]["labels"]]
            todo.labels = list(set(todo.labels + labels))
            filtered.append(todo)
        else:
            filtered.append(todo)
    return filtered


def make_requests(
    token: str, todos: List[Todo], config=dict
) -> Tuple[List[str], List[str]]:
    username = config["username"]
    repository = config["repository"]
    url = construct_url(username, repository)
    print(f"Posting to: {url}\n")

    successful = []
    failed = []
    headers = {**ACCEPT, "Authorization": f"token {token}"}
    todos = filter_issues(url, headers, todos, issue_state=ALL_ISSUES)

    for todo in todos:
        json = prepare_body(todo, username, repository)
        if not todo.issue_no:
            title, success = post_issue(
                url,
                headers,
                json=json,
            )
        else:
            title, success = patch_issue(
                url,
                headers,
                json=json,
                issue_no=todo.issue_no,
            )
        if success:
            successful.append(title)
        else:
            failed.append(title)
    return successful, failed


# TODO[Enhancement]: Add issue number to TODO in code
# It would be useful to have the assigned issue number from github
# attached to the TODO in code so you can immediateyl identify the TODOs
