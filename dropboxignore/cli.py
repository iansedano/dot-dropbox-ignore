"""Command Line Interface for DotDropboxIgnore"""

# Standard library imports
import argparse
import itertools
from importlib import resources
from pathlib import Path

# DotDropboxIgnore imports
from dropboxignore.paths_to_ignore import get_paths_to_ignore, read_ignore_files
from dropboxignore.shell import init_shell


def cli():
    """CLI entry point"""
    args = get_args()
    ignore_parser = read_ignore_files(args.path)
    parsed_paths = tuple(get_paths_to_ignore(args.path, ignore_parser))

    print("\nPATHS TO IGNORE:\n")
    for path in parsed_paths:
        print(f"  - {path.relative_to(Path.cwd())}")
    print()

    if ask_to_proceed():
        shell = init_shell()
        shell.ignore_folders(parsed_paths)

    raise SystemExit


def get_args():
    """Get the command line arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "path",
        help="Path to ignore (default working directory)",
        default=Path.cwd(),
        nargs="?",
        type=Path,
    )
    parser.add_argument(
        "-f",
        "--file",
        help="The specific ignore file (has own default)",
        default=get_ignore_file(),
    )
    return parser.parse_args()


def get_ignore_file():
    """Get the ignore file in the CWD or uses the package default"""
    return next(
        file
        for file in itertools.chain(
            Path.cwd().iterdir(), resources.files(__package__).iterdir()
        )
        if file.name == ".dropboxignore"
    )


def ask_to_proceed():
    """Asks user to proceed with operation"""
    while True:
        user_input = input("proceed? y/n\n")

        if user_input in "yY":
            return True
        elif user_input in "nN":
            return False
        else:
            print("invalid input")
