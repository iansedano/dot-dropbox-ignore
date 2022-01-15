from pathlib import Path

p = Path("C:/Dropbox/git_projects")

git_folders_glob = p.glob("**/.git")
print([str(fo) for fo in git_folders_glob])

globs = [
	"**/.git",
	"**/node_modules",
	"**/venv",
	"**/__pycache__"
]