"""In-memory virtual file system backed by a ZIP archive (Stage 3)."""

import posixpath
import zipfile
import os

ROOT = "/"

SEP = "/"


class VFS:
    """Virtual file system loaded entirely into memory from a ZIP."""

    def __init__(self, name, files, dirs):
        """Store the parsed file system and reset the working dir."""
        self.name = name
        self.files = files
        self.dirs = dirs
        self.cwd = ROOT

    @classmethod
    def from_zip(cls, path):
        """Load a VFS from a ZIP archive.

        Returns a tuple (vfs, error). On success error is None.
        """
        try:
            archive = zipfile.ZipFile(path, "r")
        except FileNotFoundError:
            return None, f"Error: VFS file not found: {path}"
        except zipfile.BadZipFile:
            return None, f"Error: invalid VFS archive: {path}"

        with archive:
            files, dirs = _read_archive(archive)

        name = posixpath.splitext(os.path.basename(path))[0]
        return cls(name, files, dirs), None

    def normalize(self, path):
        """Turn path into an absolute normalized VFS path."""
        if not path:
            return self.cwd
        if not path.startswith(SEP):
            path = posixpath.join(self.cwd, path)
        return posixpath.normpath(path)

    def is_dir(self, path):
        """Return True if path is an existing directory."""
        return self.normalize(path) in self.dirs

    def ls(self, path):
        """List the contents of a directory, or echo a file name.

        Returns a tuple (lines, error). On success error is None.
        """
        target = self.normalize(path)
        if target in self.files:
            return [posixpath.basename(target)], None
        if target not in self.dirs:
            return [], f"Error: ls: no such file or directory: {path}"
        prefix = target.rstrip(SEP) + SEP if target != ROOT else SEP
        names = set()
        for candidate in list(self.files) + list(self.dirs):
            if candidate == target or not candidate.startswith(prefix):
                continue
            rest = candidate[len(prefix):]
            if rest:
                names.add(rest.split(SEP, 1)[0])
        return sorted(names), None

    def cd(self, path):
        """Change the working directory.

        Returns None on success or an error string.
        """
        target = self.normalize(path)
        if target in self.dirs:
            self.cwd = target
            return None
        return f"Error: cd: no such directory: {path}"


def _read_archive(archive):
    """Parse a ZIP archive into files and directories dictionaries."""
    files = {}
    dirs = {ROOT}
    for name in archive.namelist():
        normalized = SEP + name.replace("\\", SEP).lstrip(SEP)
        if name.endswith(SEP):
            _add_with_parents(normalized.rstrip(SEP), dirs)
            continue
        files[normalized] = archive.read(name)
        parent = posixpath.dirname(normalized)
        _add_with_parents(parent, dirs)
    return files, dirs


def _add_with_parents(path, dirs):
    """Add path and all its parent directories to the dirs set."""
    current = path
    while current and current not in dirs:
        dirs.add(current)
        parent = posixpath.dirname(current)
        if parent == current:
            break
        current = parent
