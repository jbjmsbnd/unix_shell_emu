"""Tests for head, tac and wc commands over the VFS (Stage 4)."""

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
    """Create a small fixed VFS for tests."""
    path = _make_zip(
        {
            "text.txt": b"line1\nline2\nline3\nline4\nline5\n",
            "empty.txt": b"",
            "dir/inside.txt": b"a b c\n",
        }
    )
    vfs, error = VFS.from_zip(path)
    os.unlink(path)
    assert error is None
    return vfs


def test_head_default():
    vfs = _sample_vfs()
    result = execute_command("head /text.txt", vfs)
    assert result == "line1\nline2\nline3\nline4\nline5"


def test_head_missing_file():
    vfs = _sample_vfs()
    result = execute_command("head /nope.txt", vfs)
    assert result.startswith("Error:")


def test_head_no_args():
    vfs = _sample_vfs()
    result = execute_command("head", vfs)
    assert result.startswith("Error:")


def test_head_on_directory():
    vfs = _sample_vfs()
    result = execute_command("head /dir", vfs)
    assert result.startswith("Error:")


def test_head_stub_without_vfs():
    assert execute_command("head /x") == "head /x"


def test_tac_reverses_lines():
    vfs = _sample_vfs()
    result = execute_command("tac /text.txt", vfs)
    assert result == "line5\nline4\nline3\nline2\nline1"


def test_tac_empty_file():
    vfs = _sample_vfs()
    result = execute_command("tac /empty.txt", vfs)
    assert result == ""


def test_tac_missing_file():
    vfs = _sample_vfs()
    result = execute_command("tac /nope.txt", vfs)
    assert result.startswith("Error:")


def test_tac_no_args():
    vfs = _sample_vfs()
    result = execute_command("tac", vfs)
    assert result.startswith("Error:")


def test_tac_stub_without_vfs():
    assert execute_command("tac /x") == "tac /x"


def test_wc_counts():
    vfs = _sample_vfs()
    result = execute_command("wc /text.txt", vfs)
    assert result == "5 5 30"


def test_wc_empty_file():
    vfs = _sample_vfs()
    result = execute_command("wc /empty.txt", vfs)
    assert result == "0 0 0"


def test_wc_missing_file():
    vfs = _sample_vfs()
    result = execute_command("wc /nope.txt", vfs)
    assert result.startswith("Error:")


def test_wc_no_args():
    vfs = _sample_vfs()
    result = execute_command("wc", vfs)
    assert result.startswith("Error:")


def test_wc_stub_without_vfs():
    assert execute_command("wc /x") == "wc /x"


def test_wc_relative_path():
    vfs = _sample_vfs()
    vfs.cwd = "/dir"
    result = execute_command("wc inside.txt", vfs)
    assert result == "1 3 6"
