import re
from dataclasses import dataclass, field
from typing import List, Tuple
import pathlib

TODO_PREFIX = "# TODO"
TODO_PREFIX_BODY = "#"
SEPARATORS = r"[\s?,-/~#\\\s\s?]+"
PATTERN = rf"# TODO(\[([a-zA-Z{SEPARATORS}]*)?\])?:(.*)"


class TODOError(Exception):
    ...


@dataclass
class Todo:
    title: str
    body: str
    line_no: int
    origin: pathlib.Path
    labels: List[str] = field(default_factory=list)

    def __str__(self) -> str:
        _labels = ""
        if self.labels:
            _labels = "[" + ", ".join(self.labels) + "]"
        return f"TODO:\n{self.title} {_labels}:\n{self.body}\nIn {self.origin} - line {self.line_no}"


def extract_title_info(pattern: str, title_line: str) -> Tuple[str, List[str]]:
    match = re.search(pattern, title_line)
    if match is None:
        raise TODOError("TODO structure is malformed")
    _, labels, title = match.groups()
    title = title.strip()
    if labels:
        # labels = labels.split(",")
        labels = re.split(SEPARATORS, labels)
        return title, [label.strip() for label in labels]
    return title, []


def process_raw_todo(todo_lines: List[Tuple[int, str]], path: str = __file__) -> Todo:
    line_no, title = todo_lines[0]
    if len(todo_lines) > 1:
        body = " ".join([line[2:] for _, line in todo_lines[1:]])
    else:
        body = ""
    title, labels = extract_title_info(PATTERN, title)
    if not title:
        raise TODOError("TODOs require a title")
    return Todo(title=title, body=body, line_no=line_no, origin=path, labels=labels)


def parse(raw_source: str, path: str = __file__) -> List[Todo]:
    result: List[Todo] = []

    if not raw_source:
        return []

    lines = raw_source.split("\n")
    normalised_lines = [line.strip() for line in lines]

    possible = []
    start = False
    for index, line in enumerate(normalised_lines, start=1):
        if not start and line.startswith(TODO_PREFIX):
            start = True
            possible.append((index, line))
        elif start and line.startswith(TODO_PREFIX):
            start = False
            todo = process_raw_todo(possible)
            result.append(todo)
            todo = process_raw_todo([(index, line)])
            result.append(todo)
        elif start and line.startswith(TODO_PREFIX_BODY):
            possible.append((index, line))
        elif start and not line.startswith(TODO_PREFIX_BODY):
            start = False
            todo = process_raw_todo(possible, path)
            result.append(todo)
            possible = []

    return result
