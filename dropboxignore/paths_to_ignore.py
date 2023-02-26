"""Handles reading ignore files and generating a list of paths based on them
"""

# Standard library imports
from pathlib import Path
import os
import platform

import igittigitt

SEPARATOR = "\\" if platform.system() == "Windows" else "/"
TERMINAL_SIZE = os.get_terminal_size().columns


def read_ignore_files(path, base_dir=None):
    if base_dir is None:
        base_dir = Path.cwd()
    parser = igittigitt.IgnoreParser()
    parser.parse_rule_files(base_dir, filename=".dropboxignore")
    return parser


def get_paths_to_ignore(root: Path, parser: igittigitt.IgnoreParser):
    def helper(root: str):
        for item in os.listdir(root):
            if parser.match(item):
                yield Path(f"{root}{SEPARATOR}{item}")
            else:
                try:
                    new_path = f"{root}{SEPARATOR}{item}"
                    yield from helper(new_path)

                    terminal_msg = f"Scanning: {new_path[:TERMINAL_SIZE - 10]}"
                    padding = (TERMINAL_SIZE - len(terminal_msg)) * " "
                    print(f"{terminal_msg}{padding}", end="\r")
                except (NotADirectoryError, FileNotFoundError):
                    continue

    if root.is_absolute():
        yield from helper(str(root))
    else:
        raise TypeError
