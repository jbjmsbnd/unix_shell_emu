"""Generate test VFS archives for the shell emulator (Stage 3).

The archives are intentionally not committed to git: the
repository must not contain binary files or archives. This
script recreates them on demand.
"""

import os
import zipfile

# Directory where the generated archives will be stored.
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "vfs")

# Minimal VFS: a single file in the root.
MINIMAL_FILES = {
    "README.txt": b"This is a minimal VFS.\n",
}

# Several files spread across different directories.
SEVERAL_FILES = {
    "README.txt": b"Several files VFS.\n",
    "etc/config.ini": b"[main]\nkey=value\n",
    "home/user/notes.txt": b"Notes for the user.\n",
    "var/log/app.log": b"started\nstopped\n",
}

# Deep VFS: at least three levels of nesting.
DEEP_FILES = {
    "a/b/c/file1.txt": b"deep one\n",
    "a/b/c/d/file2.txt": b"deep two\n",
    "a/b/c/d/e/file3.txt": b"deep three\n",
    "a/b/other.txt": b"side file\n",
}


def _write_archive(name, entries):
    """Write one zip archive with the given files."""
    path = os.path.join(OUTPUT_DIR, name)
    with zipfile.ZipFile(path, "w") as archive:
        for filename, content in entries.items():
            archive.writestr(filename, content)
    print(f"created {path}")


def main():
    """Generate all test VFS archives."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    _write_archive("minimal.zip", MINIMAL_FILES)
    _write_archive("several.zip", SEVERAL_FILES)
    _write_archive("deep.zip", DEEP_FILES)


if __name__ == "__main__":
    main()
