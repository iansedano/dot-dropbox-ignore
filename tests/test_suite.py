# Standard library imports
from pathlib import Path

# dropboxignore imports
from dropboxignore import folders_to_ignore, shell


def test_should_instantiate_pwsh_shell():
	shell.Pwsh_shell()

def test_should_instantiate_bash_shell():
	shell.Bash_shell()
	

