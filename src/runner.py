"""Start script runner for the VFS shell emulator (Stage 2)."""

from src.emulator import EXIT_SENTINEL, execute_command

# Prefix of a comment line in a start script.
COMMENT_PREFIX = "#"


class ScriptResult:
    """Summary of running a start script."""

    def __init__(self):
        """Initialize an empty result."""
        self.total = 0
        self.executed = 0
        self.failed = 0
        self.exited = False


def read_script(path):
    """Read a start script from disk.

    Returns a tuple (lines, error). On success error is None.
    """
    try:
        with open(path, "r", encoding="utf-8") as handle:
            return handle.read().splitlines(), None
    except OSError as error:
        return [], f"Error: cannot read script: {error}"


def is_skippable(line):
    """Return True for blank lines and comment lines."""
    stripped = line.strip()
    return not stripped or stripped.startswith(COMMENT_PREFIX)


def run_script(lines, write):
    """Run start script lines, calling write() for each output line.

    Blank and comment lines are skipped. A failing command is
    reported but does not stop the script. The script stops when
    the emulator returns the EXIT sentinel.
    """
    result = ScriptResult()
    for line in lines:
        if is_skippable(line):
            continue
        result.total += 1
        write(f"$ {line}")
        output = execute_command(line)
        if output == EXIT_SENTINEL:
            result.exited = True
            break
        if output:
            write(output)
            if output.startswith("Error:"):
                result.failed += 1
        result.executed += 1
    return result