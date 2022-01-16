from pathlib import Path
import shell
import folders_to_ignore


def test_should_instantiate_pwsh_shell():
	shell.Pwsh_shell()

def test_should_instantiate_bash_shell():
	shell.Bash_shell()
	

	