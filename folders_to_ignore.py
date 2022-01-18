from pathlib import Path
from pprint import pp

def read_ignore_file(path: Path):
	text = [l.strip() for l in path.read_text(encoding="UTF-8").strip().split("\n")]
	return list(filter(lambda s: s != "", text))

def get_paths_to_ignore(root: Path, globs: list[str]):
	paths_to_ignore = []
	for glob_pattern in globs:
		folders = root.glob(glob_pattern)
		paths_to_ignore.extend(folders)
	return paths_to_ignore
		