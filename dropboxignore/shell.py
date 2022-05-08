# Standard library imports
import platform
import subprocess
from abc import ABC, abstractmethod
from enum import Enum
from pathlib import Path


class SYSTEMS(Enum):
    LINUX = "Linux"
    WINDOWS = "Windows"
    MAC = "Darwin"


def init_shell():
    print("initializing shell")
    system = platform.system()
    print(f"{system} detected")
    if system == SYSTEMS.LINUX.value:
        return Bash_shell()
    elif system == SYSTEMS.WINDOWS.value:
        return Pwsh_shell()


class Shell(ABC):
    @abstractmethod
    def ignore_folders(self, paths: list[Path]):
        pass


class Pwsh_shell(Shell):
    def _run(self, cmd):
        completed_process = subprocess.run(["pwsh", "-Command", cmd])
        return completed_process

    def _run_with_output(self, cmd):
        process = self._run(cmd)
        # print(process.stdout.decode(), process.stderr.decode())
        return process

    def _get_ignored_value(self, path: Path):
        command = f"Get-Content -Path '{str(path)}' -Stream com.dropbox.ignored"
        return self._run_with_output(command)

    def ignore_folders(self, paths: list[Path]):
        path_list = "', '".join([str(path).replace("'", "`'") for path in paths])
        command = (
            f"Set-Content -Path '{path_list}' -Stream com.dropbox.ignored -Value 1"
        )
        return self._run_with_output(command)

    # "list" prints a list of directories currently excluded from syncing.
    # "add" adds one or more directories to the exclusion list, then
    # resynchronizes Dropbox.
    # "remove" removes one or more directories from the exclusion list, then
    # resynchronizes Dropbox.


class Bash_shell(Shell):

    # https://help.dropbox.com/files-folders/restore-delete/ignored-files

    def make_string_path_list(self, paths: list[Path]):
        return "' '".join([str(path).replace("'", "\\'") for path in paths])

    def get_ignored_status(self, paths: list[Path]):
        path_list = self.make_string_path_list(paths)

        command = f"""for f in '{path_list}'
do
    if  (attr -q -g com.dropbox.ignored $f)
    then
        echo "$f"
    fi
done
"""
        subprocess.run(["sh", "-c", command])

    def ignore_folders(self, paths: list[Path]):
        path_list = self.make_string_path_list(paths)
        command = (
            f"for f in '{path_list}'\n do\n attr -s com.dropbox.ignored -V 1 $f\ndone"
        )
        subprocess.run(["sh", "-c", command])
