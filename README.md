# DotDropboxIgnore

A cross-platform module to facilitate ignoring files and folders in a Dropbox folder.

Tested on Windows and Linux (Fedora).

## Installation

Installation not strictly required, Python 3.9+.

To make it easier to call the utility, clone this repository and then install it with pip:

```bash
python -m pip install -e .
```

Now you can call:

```bash
python -m dropboxignore
```

From anywhere.

If managing multiple version of Python can be useful to install with [pipx](https://github.com/pypa/pipx).

```bash
pipx install . # from within folder
```

So you can call:

```bash
dbignore
```

From anywhere.

## Usage

Assuming that you have installed with pipx:

```bash
dropboxignore
```

Will search for all files and folders recursively from the current working directory that match the default `.dropboxignore` file in the module, which includes:

```
**/.git
**/node_modules
**/venv
**/env
**/__pycache__*
**/.pytest_cache*

**/*.manifest
**/*.spec
**/build
**/dist
**/*.egg-info*
```

Which you can modify yourself if you want to customize it, just note that they need to be valid glob patterns.

You can also pass in explicit arguments for the path to use as root and a custom `.dropboxignore` file.

```powershell
dropboxignore C:\Dropbox C:\Dropbox\.dropboxignore
```
