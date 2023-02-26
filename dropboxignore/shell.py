"""Defines the different shells required for ignore operations
"""

# Standard library imports
import platform
import textwrap
from abc import ABC, abstractmethod
from pathlib import Path
from subprocess import DEVNULL, run


def init_shell():
    """Detect OS and initlialize appropriate shell"""
    print("initializing shell")
    system = platform.system()
    print(f"{system} detected")
    if system == "Linux":
        return Bash_shell()
    elif system == "Windows":
        return Pwsh_shell()
    elif system == "Darwin":
        raise Bash_shell()


class Shell(ABC):
    """Interface for shells"""

    @abstractmethod
    def ignore_folders(self, paths: list[Path]):
        """Should get Dropbox to ignore all paths provided"""
        pass


class Pwsh_shell(Shell):
    """Powershell Core ignore runner"""

    def __init__(self):
        try:
            run(["pwsh", "-V"], stdout=DEVNULL, stderr=DEVNULL)
            self.shell = "pwsh"
        except FileNotFoundError:
            print("Powershell Core not installed, falling back to Windows PowerShell")
            self.shell = "powershell"

    @staticmethod
    def _make_string_path_list(paths: list[Path]):
        """Joins list of paths into one long string to pass into pwsh"""
        return "', '".join([str(path).replace("'", "`'") for path in paths])

    def ignore_folders(self, paths: list[Path]):
        """Sends ignore command"""
        path_list = self._make_string_path_list(paths)
        command = (
            f"Set-Content -Path '{path_list}' -Stream com.dropbox.ignored -Value 1"
        )
        run([self.shell, "-NoProfile", "-Command", command], check=True)
        print("Done!")


class Bash_shell(Shell):
    @staticmethod
    def _make_string_path_list(paths: list[Path]):
        """Joins list of paths into one long string to pass into bash"""
        return "' '".join([str(path).replace("'", "\\'") for path in paths])

    def get_ignored_status(self, paths: list[Path]):
        """Query the Dropbox ignored status"""
        path_list = self._make_string_path_list(paths)

        command = textwrap.dedent(
            f"""\
            for f in '{path_list}'
            do
                if  (attr -q -g com.dropbox.ignored $f)
                then
                    echo "$f"
                fi
            done"""
        )
        run(["sh", "-c", command])

    def ignore_folders(self, paths: list[Path]):
        """Sends the ignore command to bash"""
        path_list = self._make_string_path_list(paths)
        command = (
            f"for f in '{path_list}'\ndo\nattr -s com.dropbox.ignored -V 1 $f\ndone"
        )
        run(["bash", "-c", command], check=True)
        print("Done!")
