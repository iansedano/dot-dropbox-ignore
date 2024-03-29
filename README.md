# DotDropboxIgnore

A cross-platform module to facilitate ignoring files and folders in a Dropbox folder.

Tested on Windows and Linux (Fedora).

## Installation

Installation not strictly required, Python 3.9+.

To make it easier to call the utility, clone this repository and then install it with pip:

```bash
python -m pip install dot-dropbox-ignore
```

Now you can call either:

```bash
$ python -m dropboxignore

or

$ dbignore
```

From anywhere you have access to your Python installation.

If managing multiple versions of Python can be useful to install with [pipx](https://github.com/pypa/pipx).

```bash
pipx install dot-dropbox-ignore
```

## Usage

The default command without any arguments will search for all files and folders recursively from the current working directory that match the default `.dropboxignore` file in the current working directory.

You can also pass in explicit arguments for the path to use as root and a custom `.dropboxignore` file.

```powershell
dbignore C:\Dropbox C:\Dropbox\.dropboxignore
```

Just beware that trying to scan a whole Dropbox will take considerable time.
