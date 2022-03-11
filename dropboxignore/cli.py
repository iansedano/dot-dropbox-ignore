# Standard library imports
import argparse
import os
from pathlib import Path
from pprint import pp

# dropboxignore imports
from dropboxignore import folders_to_ignore, shell


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
	arg_parser = argparse.ArgumentParser()

	arg_parser.add_argument("root_path")
	arg_parser.add_argument("ignore_file")

	args = arg_parser.parse_args()
	
	globs = folders_to_ignore.read_ignore_file(Path(args.ignore_file))
	
	paths_to_ignore = folders_to_ignore.get_paths_to_ignore(Path(args.root_path), globs)
	
	print("PATHS TO IGNORE\n")
	pp(paths_to_ignore)
	proceed = ask_to_proceed()
	
	if proceed is False:
		exit
	elif proceed is True:
		db_shell = shell.init_shell()
		print(db_shell)
		db_shell.ignore_folders(paths_to_ignore)
		exit
