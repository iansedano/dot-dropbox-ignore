import os
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
	system = platform.system()
	if system == SYSTEMS.LINUX:
		return Bash_shell()
	elif system == SYSTEMS.WINDOWS:
		return Pwsh_shell()
		
class Shell(ABC):
	@abstractmethod
	def ignore_folders(self, paths: list(Path)):
		pass

class Pwsh_shell(Shell):
	def run(self, cmd):
		completed_process = subprocess.run(["pwsh", "-Command", cmd], capture_output=True)
		return completed_process
	
	def run_with_output(self, cmd):
		process = self.run(cmd)
		print(process.stdout.decode(), process.stderr.decode())
		return process
	
	def send_ignore_command(self, path: Path):
		command = f"Set-Content -Path '{str(path)}' -Stream com.dropbox.ignored -Value 1"
		return self.run_with_output(command)
		
	def get_ignored_value(self, path: Path):
		command = f"Get-Content -Path '{str(path)}' -Stream com.dropbox.ignored"
		return self.run_with_output(command)
	
	def ignore_folders(self, paths: list(Path)):
		for path in paths:
			self.send_ignore_command(path)

class Bash_shell(Shell):

	def run(self, cmd):
		completed_process = subprocess.run([cmd], capture_output=True)
		return completed_process
	
	def run_with_output(self, cmd):
		process = self.run(cmd)
		print(process.stdout.decode(), process.stderr.decode())
		return process
	
	def get_exclude_list(self):
		exclude_list = self.run_with_output("dropbox exclude list")
	
	def ignore_folders(self, paths: list(Path)):
		exclude_list = self.get_exclude_list()
		print(exclude_list)
		command = f"drobox exclude {' '.join([str(path) for path in paths])}"
		return self.run_with_output(command)
	
	# "list" prints a list of directories currently excluded from syncing.
	# "add" adds one or more directories to the exclusion list, then
	# resynchronizes Dropbox.
	# "remove" removes one or more directories from the exclusion list, then
	# resynchronizes Dropbox.
