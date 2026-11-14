"""Integration tests: emulator commands with a real VFS (Stage 3)."""

import os
import tempfile
import zipfile

from src.emulator import execute_command
from src.vfs import VFS


def _make_zip(entries):
    """Create a temporary zip with the given {name: bytes} entries.

    Returns the path to the zip file. Caller must delete it.
    """
    handle = tempfile.NamedTemporaryFile(
        suffix=".zip", delete=False
    )
    handle.close()
    with zipfile.ZipFile(handle.name, "w") as archive:
        for name, data in entries.items():
            archive.writestr(name, data)
    return handle.name


def _sample_vfs():
    """Create a small fixed VFS for integration tests."""
    path = _make_zip(
        {
            "home/user/file.txt": b"hello",
            "tmp/log.txt": b"data",
        }
    )
    vfs, error = VFS.from_zip(path)
    os.unlink(path)
    assert error is None
    return vfs


def test_ls_root_with_vfs():
    vfs = _sample_vfs()
    result = execute_command("ls /", vfs)
    assert result == "home\ntmp"


def test_ls_subdir_with_vfs():
    vfs = _sample_vfs()
    result = execute_command("ls /home", vfs)
    assert result == "user"


def test_ls_file_with_vfs():
    vfs = _sample_vfs()
    result = execute_command("ls /home/user/file.txt", vfs)
    assert result == "file.txt"


def test_ls_missing_with_vfs():
    vfs = _sample_vfs()
    result = execute_command("ls /nope", vfs)
    assert result.startswith("Error:")
    assert "no such" in result


def test_ls_current_dir_with_vfs():
    vfs = _sample_vfs()
    vfs.cwd = "/home"
    result = execute_command("ls", vfs)
    assert result == "user"


def test_cd_success_with_vfs():
    vfs = _sample_vfs()
    result = execute_command("cd /home", vfs)
    assert result == ""
    assert vfs.cwd == "/home"


def test_cd_no_args_goes_to_root():
    vfs = _sample_vfs()
    vfs.cwd = "/home/user"
    result = execute_command("cd", vfs)
    assert result == ""
    assert vfs.cwd == "/"


def test_cd_missing_with_vfs():
    vfs = _sample_vfs()
    result = execute_command("cd /nope", vfs)
    assert result.startswith("Error:")
    assert "no such" in result
    assert vfs.cwd == "/"


def test_cd_parent_with_vfs():
    vfs = _sample_vfs()
    vfs.cwd = "/home/user"
    result = execute_command("cd ..", vfs)
    assert result == ""
    assert vfs.cwd == "/home"


def test_stub_without_vfs_still_works():
    assert execute_command("ls") == "ls"
    assert execute_command("ls /home") == "ls /home"
    assert execute_command("cd /tmp") == "cd /tmp"


def test_unknown_command_with_vfs():
    vfs = _sample_vfs()
    result = execute_command("echo hello", vfs)
    assert result == "Error: unknown command: echo"


def test_exit_with_vfs():
    vfs = _sample_vfs()
    result = execute_command("exit", vfs)
    assert result == "EXIT"
