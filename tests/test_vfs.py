"""Tests for the in-memory VFS (Stage 3)."""

import os
import tempfile
import zipfile

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
    """Create a VFS with a small fixed tree for tests."""
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


def test_from_zip_success():
    vfs = _sample_vfs()
    assert vfs.name.startswith("tmp")
    assert "/home/user/file.txt" in vfs.files
    assert "/tmp/log.txt" in vfs.files
    assert "/" in vfs.dirs
    assert "/home" in vfs.dirs
    assert "/home/user" in vfs.dirs
    assert "/tmp" in vfs.dirs
    assert vfs.cwd == "/"


def test_from_zip_missing_file():
    vfs, error = VFS.from_zip("no_such_file_12345.zip")
    assert vfs is None
    assert error is not None
    assert "not found" in error


def test_from_zip_invalid_archive():
    handle = tempfile.NamedTemporaryFile(
        suffix=".zip", delete=False
    )
    handle.write(b"this is not a zip")
    handle.close()
    try:
        vfs, error = VFS.from_zip(handle.name)
        assert vfs is None
        assert error is not None
        assert "invalid" in error
    finally:
        os.unlink(handle.name)


def test_normalize_absolute():
    vfs = _sample_vfs()
    assert vfs.normalize("/home/user") == "/home/user"


def test_normalize_relative():
    vfs = _sample_vfs()
    vfs.cwd = "/home"
    assert vfs.normalize("user") == "/home/user"


def test_normalize_parent():
    vfs = _sample_vfs()
    vfs.cwd = "/home/user"
    assert vfs.normalize("..") == "/home"


def test_normalize_dot():
    vfs = _sample_vfs()
    vfs.cwd = "/home"
    assert vfs.normalize(".") == "/home"


def test_normalize_parent_from_root():
    vfs = _sample_vfs()
    assert vfs.normalize("..") == "/"


def test_is_dir_true():
    vfs = _sample_vfs()
    assert vfs.is_dir("/home") is True
    assert vfs.is_dir("/") is True


def test_is_dir_file():
    vfs = _sample_vfs()
    assert vfs.is_dir("/home/user/file.txt") is False


def test_is_dir_missing():
    vfs = _sample_vfs()
    assert vfs.is_dir("/nope") is False


def test_ls_root():
    vfs = _sample_vfs()
    lines, error = vfs.ls("/")
    assert error is None
    assert lines == ["home", "tmp"]


def test_ls_subdir():
    vfs = _sample_vfs()
    lines, error = vfs.ls("/home")
    assert error is None
    assert lines == ["user"]


def test_ls_file():
    vfs = _sample_vfs()
    lines, error = vfs.ls("/home/user/file.txt")
    assert error is None
    assert lines == ["file.txt"]


def test_ls_missing():
    vfs = _sample_vfs()
    lines, error = vfs.ls("/nope")
    assert lines == []
    assert error is not None
    assert "no such" in error


def test_cd_success():
    vfs = _sample_vfs()
    error = vfs.cd("/home")
    assert error is None
    assert vfs.cwd == "/home"


def test_cd_missing():
    vfs = _sample_vfs()
    error = vfs.cd("/nope")
    assert error is not None
    assert "no such" in error
    assert vfs.cwd == "/"


def test_cd_parent():
    vfs = _sample_vfs()
    vfs.cwd = "/home/user"
    error = vfs.cd("..")
    assert error is None
    assert vfs.cwd == "/home"


def test_cd_parent_from_root():
    vfs = _sample_vfs()
    error = vfs.cd("..")
    assert error is None
    assert vfs.cwd == "/"
