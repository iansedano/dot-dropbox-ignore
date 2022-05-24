# Standard library imports
import argparse
from importlib import resources
from pathlib import Path

# dropboxignore imports
from dropboxignore import paths_to_ignore, shell


def ask_to_proceed():
    while True:
        user_input = input("proceed? y/n\n")

        if user_input in "yY":
            return True
        elif user_input in "nN":
            return False
        else:
            print("invalid input")


def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "path",
        help="Path to ignore (default working directory)",
        default=Path.cwd(),
        nargs="?",
    )
    parser.add_argument(
        "-i",
        help="The specific ignore file (has own default)",
        default=resources.path("dropboxignore", ".dropboxignore"),
    )
    args = parser.parse_args()

    globs = paths_to_ignore.read_ignore_file(Path(args.i))

    parsed_paths: list[Path] = paths_to_ignore.get_paths_to_ignore(
        Path(args.path), globs
    )

    print("PATHS TO IGNORE:\n")
    for path in parsed_paths:
        print(f"- {path.relative_to(Path.cwd())}")
    print("\n")
    proceed = ask_to_proceed()

    if proceed is False:
        exit
    elif proceed is True:
        db_shell = shell.init_shell()
        db_shell.ignore_folders(parsed_paths)
        exit
