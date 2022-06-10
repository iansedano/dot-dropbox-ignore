# Standard library imports
import platform
from subprocess import run, DEVNULL
from abc import ABC, abstractmethod
from pathlib import Path


def init_shell():
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
    @abstractmethod
    def ignore_folders(self, paths: list[Path]):
        pass


class Pwsh_shell(Shell):
    def __init__(self):
        try:
            run(["pwsh", "-V"], stdout=DEVNULL, stderr=DEVNULL)
            self.shell = "pwsh"
        except FileNotFoundError as exc:
            print("Powershell Core not installed, falling back to PowerShell")
            self.shell = "powershell"

    def _make_string_path_list(self, paths: list[Path]):
        return "', '".join([str(path).replace("'", "`'") for path in paths])

    def ignore_folders(self, paths: list[Path]):
        path_list = self._make_string_path_list(paths)
        command = (
            f"Set-Content -Path '{path_list}' -Stream com.dropbox.ignored -Value 1"
        )
        run([self.shell, "-NoProfile", "-Command", command], check=True)
        print("Done!")


class Bash_shell(Shell):
    def _make_string_path_list(self, paths: list[Path]):
        return "' '".join([str(path).replace("'", "\\'") for path in paths])

    def get_ignored_status(self, paths: list[Path]):
        path_list = self._make_string_path_list(paths)

        command = f"""for f in '{path_list}'
do
    if  (attr -q -g com.dropbox.ignored $f)
    then
        echo "$f"
    fi
done
"""
        run(["sh", "-c", command])

    def ignore_folders(self, paths: list[Path]):
        path_list = self._make_string_path_list(paths)
        command = (
            f"for f in '{path_list}'\n do\n attr -s com.dropbox.ignored -V 1 $f\ndone"
        )
        run(["bash", "-c", command], check=True)
        print("Done!")
