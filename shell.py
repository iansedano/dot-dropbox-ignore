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
	print(system)
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
		completed_process = subprocess.run(["pwsh", "-Command", cmd], capture_output=True)
		return completed_process
	
	def _run_with_output(self, cmd):
		process = self._run(cmd)
		print(process.stdout.decode(), process.stderr.decode())
		return process
	
	def _send_ignore_command(self, path: Path):
		command = f"Set-Content -Path '{str(path)}' -Stream com.dropbox.ignored -Value 1"
		return self._run_with_output(command)
		
	def _get_ignored_value(self, path: Path):
		command = f"Get-Content -Path '{str(path)}' -Stream com.dropbox.ignored"
		return self._run_with_output(command)
	
	def ignore_folders(self, paths: list[Path]):
		for path in paths:
			self._send_ignore_command(path)
	
	# "list" prints a list of directories currently excluded from syncing.
	# "add" adds one or more directories to the exclusion list, then
	# resynchronizes Dropbox.
	# "remove" removes one or more directories from the exclusion list, then
	# resynchronizes Dropbox.

class Bash_shell(Shell):
	
	# https://help.dropbox.com/files-folders/restore-delete/ignored-files

	def _run(self, cmd):
		completed_process = subprocess.run([cmd], capture_output=True)
		return completed_process
	
	def _run_with_output(self, cmd):
		process = self._run(cmd)
		print(process.stdout.decode(), process.stderr.decode())
		return process
	
	def _init_exclude_list(self):
		exclude_list = self._run_with_output("dropbox exclude list")
		"""
		Excluded: 
		../../../Dropbox/0 JPA
		../../../Dropbox/0 Music
		../../../Dropbox/0 Projects
		"""
		
	def _send_ignore_command(self):	
		pass
	
	def ignore_folders(self, paths: list[Path]):
		exclude_list = self._get_exclude_list()
		print(exclude_list)
		command = f"drobox exclude {' '.join([str(path) for path in paths])}"
		return self._run_with_output(command)
	
	
