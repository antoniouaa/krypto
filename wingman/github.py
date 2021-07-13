import os
import pathlib
import platform
import subprocess
from typing import List

import requests

from wingman.todo import Todo

BASE_URL = "https://api.github.com"


class GithubError(Exception):
    ...


def get_basename() -> str:
    plat = platform.system()
    if plat == "Windows":
        basename = subprocess.run(
            ["powershell.exe", "git remote get-url origin"], capture_output=True
        )
    else:
        basename = subprocess.run(["git remote get-url origin"], capture_output=True)
    path = pathlib.Path(basename.stdout.decode().strip()[: -len(".git")])
    username, repo_name = path.parts[-2:]
    return username, repo_name


# TODO: Check if issue already exists to prevent duplication
# If the issue does already exist then update its body with the new body


def create_issues(todos: List[Todo], token: str) -> int:
    if not todos:
        print("No todos to create!")
        return

    token = os.getenv("GITHUB_PERSONAL_TOKEN")
    username, repo_name = get_basename()
    url = f"{BASE_URL}/repos/{username}/{repo_name}/issues"
    print(url)
    failed = []
    print("Creating issues...")

    with requests.Session() as session:
        session.headers.update({"authorization": f"token {token}"})
        for todo in todos:
            print(f"> Issue {todo.title}")
            body = {
                "title": todo.title,
                "body": f"{todo.body}\n\nLine: {todo.line_no} in [{todo.origin}]({todo.origin})",
            }
            response = session.post(url, json=body)
            if response.status_code != 201:
                print(f"Error: {response.json()['message']}")
                failed.append(todo)
                continue
            number = response.json()["number"]
            link = response.json()["url"]
            print(f"Created: Issue#{number} at {link}")
    return failed