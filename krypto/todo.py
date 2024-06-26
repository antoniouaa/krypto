import re
import pathlib
from typing import List, Optional, Tuple
from dataclasses import dataclass, field

from krypto.config import SYMBOLS

SEPARATORS = r"[\s?,-/~#\\\s\s?]+"
PATTERN = r"{}(\[([a-zA-Z{}]*)?\])?:(.*)"


# TODO[Enhancement]: Add functionality for multiline comments in js
# Will need to change the parser to deal with the new tokens


class TODOError(Exception): ...


@dataclass
class Todo:
    title: str
    body: str
    line_no: int
    origin: pathlib.Path
    labels: List[str] = field(default_factory=list)
    issue_no: Optional[int] = None

    def __str__(self) -> str:
        _labels = ""
        if self.labels:
            _labels = "[" + ", ".join(self.labels) + "]"
        return f"TODO:\n{self.title} {_labels}:\n{self.body}\nIn {self.origin} - line {self.line_no}"


def gather_todos(path: str, config: dict) -> List[Todo]:
    todos = []
    src = config["src"]
    for extension in SYMBOLS.keys():
        for file in pathlib.Path(path).glob(f"{src}/**/*.{extension}"):
            if "test" not in str(file):
                with open(file) as f:
                    lst = parse(
                        f.read(),
                        extension,
                        path=str(file),
                        todo_prefix=config["prefix"],
                    )
                    if lst:
                        todos.extend(lst)
    return todos


def extract_title_info(pattern: str, title_line: str) -> Tuple[str, List[str]]:
    match = re.search(pattern, title_line)
    if match is None:
        raise TODOError("TODO structure is malformed")
    _, labels, title = match.groups()
    title = title.strip()
    if labels:
        labels_ = re.split(SEPARATORS, labels)
        return title, [label.strip().capitalize() for label in labels_]
    return title, []


def process_raw_todo(
    todo_lines: List[Tuple[int, str]],
    prefix: str,
    path: str = __file__,
) -> Todo:
    line_no, title = todo_lines[0]
    if len(todo_lines) > 1:
        body = " ".join([line[2:].strip() for _, line in todo_lines[1:]]).strip()
    else:
        body = ""
    title, labels = extract_title_info(PATTERN.format(prefix, SEPARATORS), title)
    if not title:
        raise TODOError("TODOs require a title")
    return Todo(
        title=title,
        body=body,
        line_no=line_no,
        origin=pathlib.Path(path),
        labels=labels,
    )


def parse(
    raw_source: str,
    extension: str,
    path: str = __file__,
    todo_prefix: str = "TODO",
) -> List[Todo]:
    result: List[Todo] = []
    COMMENT_SYMBOL = SYMBOLS[extension]
    PREFIX = f"{COMMENT_SYMBOL} {todo_prefix}"

    if not raw_source:
        return []

    lines = raw_source.split("\n")
    normalised_lines = [line.strip() for line in lines]

    possible = []
    start = False
    for index, line in enumerate(normalised_lines, start=1):
        if not start and line.startswith(PREFIX):
            start = True
            possible.append((index, line))
        elif start and line.startswith(PREFIX):
            todo = process_raw_todo(possible, prefix=PREFIX)
            result.append(todo)
            possible = [(index, line)]
        elif start and line.startswith(COMMENT_SYMBOL):
            possible.append((index, line))
        elif start and not line.startswith(COMMENT_SYMBOL):
            start = False
            todo = process_raw_todo(possible, path=path, prefix=PREFIX)
            result.append(todo)
            possible = []

    return result
