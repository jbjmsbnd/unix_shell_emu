"""Tests for the cp command over the VFS (Stage 5)."""

import os
import tempfile
import zipfile

from src.emulator import execute_command
from src.vfs import VFS


def _make_zip(entries):
    """Create a temporary zip with the given {name: bytes} entries."""
    handle = tempfile.NamedTemporaryFile(
        suffix=".zip", delete=False
    )
    handle.close()
    with zipfile.ZipFile(handle.name, "w") as archive:
        for name, data in entries.items():
            archive.writestr(name, data)
    return handle.name


def _sample_vfs():
    """Create a small fixed VFS for cp tests."""
    path = _make_zip(
        {
            "a.txt": b"alpha\n",
            "dir/b.txt": b"beta\n",
        }
    )
    vfs, error = VFS.from_zip(path)
    os.unlink(path)
    assert error is None
    return vfs


def test_cp_basic():
    vfs = _sample_vfs()
    result = execute_command("cp /a.txt /c.txt", vfs)
    assert result == ""
    assert vfs.files["/c.txt"] == b"alpha\n"


def test_cp_source_unchanged():
    vfs = _sample_vfs()
    execute_command("cp /a.txt /c.txt", vfs)
    assert vfs.files["/a.txt"] == b"alpha\n"


def test_cp_to_directory_keeps_name():
    vfs = _sample_vfs()
    result = execute_command("cp /a.txt /dir", vfs)
    assert result == ""
    assert vfs.files["/dir/a.txt"] == b"alpha\n"


def test_cp_to_nonexistent_parent_fails():
    vfs = _sample_vfs()
    result = execute_command("cp /a.txt /new/sub/c.txt", vfs)
    assert result.startswith("Error:")
    assert "no such directory" in result
    assert "/new/sub/c.txt" not in vfs.files


def test_cp_relative_paths():
    vfs = _sample_vfs()
    vfs.cwd = "/dir"
    result = execute_command("cp b.txt copy.txt", vfs)
    assert result == ""
    assert vfs.files["/dir/copy.txt"] == b"beta\n"


def test_cp_missing_source():
    vfs = _sample_vfs()
    result = execute_command("cp /nope.txt /x.txt", vfs)
    assert result.startswith("Error:")
    assert "/x.txt" not in vfs.files


def test_cp_source_is_directory():
    vfs = _sample_vfs()
    result = execute_command("cp /dir /x.txt", vfs)
    assert result.startswith("Error:")


def test_cp_target_is_directory():
    vfs = _sample_vfs()
    result = execute_command("cp /a.txt /dir", vfs)
    assert result == ""


def test_cp_missing_args():
    vfs = _sample_vfs()
    result = execute_command("cp /a.txt", vfs)
    assert result.startswith("Error:")


def test_cp_no_args():
    vfs = _sample_vfs()
    result = execute_command("cp", vfs)
    assert result.startswith("Error:")


def test_cp_too_many_args():
    vfs = _sample_vfs()
    result = execute_command("cp a b c", vfs)
    assert result.startswith("Error:")
    assert "invalid number" in result


def test_cp_stub_without_vfs():
    assert execute_command("cp a b") == "cp a b"
