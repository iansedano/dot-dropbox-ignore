"""Handles reading ignore files and generating a list of paths based on them
"""

# Standard library imports
from pathlib import Path


def read_ignore_file(path: Path):
    """Parse an ignore file of glob patterns"""
    return [
        stripped
        for line in path.read_text(encoding="UTF-8").strip().split("\n")
        if (stripped := line.strip())
    ]


def get_paths_to_ignore(root: Path, globs: list[str]):
    """Provide list of files that match any of the glob patterns"""
    paths_to_ignore = []
    for glob_pattern in globs:
        folders = root.glob(glob_pattern)

        for folder in folders:
            skip = any(
                ignored_path in folder.parents for ignored_path in paths_to_ignore
            )
            if skip:
                continue
            else:
                paths_to_ignore.append(folder)
    return paths_to_ignore
