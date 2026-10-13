"""Tests for the start script runner (Stage 2)."""

import os
import tempfile

from src.runner import (
    ScriptResult,
    is_skippable,
    read_script,
    run_script,
)


def test_is_skippable_blank():
    assert is_skippable("") is True
    assert is_skippable("   ") is True


def test_is_skippable_comment():
    assert is_skippable("# this is a comment") is True
    assert is_skippable("   # indented comment") is True


def test_is_skippable_command():
    assert is_skippable("ls") is False
    assert is_skippable("  ls -la  ") is False


def test_read_script_success():
    with tempfile.NamedTemporaryFile(
        "w", suffix=".emu", delete=False, encoding="utf-8"
    ) as handle:
        handle.write("ls\n# comment\ncd /tmp\n")
        path = handle.name

    try:
        lines, error = read_script(path)
        assert error is None
        assert lines == ["ls", "# comment", "cd /tmp"]
    finally:
        os.unlink(path)


def test_read_script_missing_file():
    lines, error = read_script("no_such_file_12345.emu")
    assert lines == []
    assert error is not None
    assert error.startswith("Error:")


def test_run_script_collects_output():
    output = []
    result = run_script(["ls", "cd /tmp"], output.append)
    assert output == ["$ ls", "ls", "$ cd /tmp", "cd /tmp"]
    assert isinstance(result, ScriptResult)
    assert result.total == 2
    assert result.executed == 2
    assert result.failed == 0
    assert result.exited is False


def test_run_script_skips_blank_and_comments():
    output = []
    lines = ["", "# comment", "ls", "   ", "# another"]
    result = run_script(lines, output.append)
    assert output == ["$ ls", "ls"]
    assert result.total == 1
    assert result.executed == 1


def test_run_script_reports_errors_without_stopping():
    output = []
    lines = ["ls", "echo hi", "cd /tmp"]
    result = run_script(lines, output.append)
    assert output == [
        "$ ls",
        "ls",
        "$ echo hi",
        "Error: unknown command: echo",
        "$ cd /tmp",
        "cd /tmp",
    ]
    assert result.total == 3
    assert result.executed == 3
    assert result.failed == 1


def test_run_script_stops_on_exit():
    output = []
    lines = ["ls", "exit", "cd /tmp"]
    result = run_script(lines, output.append)
    assert output == ["$ ls", "ls", "$ exit"]
    assert result.total == 2
    assert result.executed == 1
    assert result.exited is True


def test_run_script_empty():
    output = []
    result = run_script([], output.append)
    assert output == []
    assert result.total == 0
    assert result.executed == 0
    assert result.failed == 0
    assert result.exited is False
