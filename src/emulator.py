"""Command parser and executor for the VFS shell emulator."""

import os
import shlex

# Name of the virtual file system shown in the window title.
VFS_NAME = "myVFS"

# Sentinel returned by execute_command to stop the REPL.
EXIT_SENTINEL = "EXIT"

# Per-command maximum number of arguments.
MAX_ARGUMENTS = {
    "ls": 1,
    "cd": 1,
    "head": 1,
    "tac": 1,
    "wc": 1,
    "exit": 0,
}

# Default path for cd without arguments (root of the VFS).
ROOT_PATH = "/"

# Number of lines printed by head when no count is given.
HEAD_DEFAULT_LINES = 10


def parse_command(command_line):
    """Parse a command line into a command and its arguments.

    Environment variables of the host OS are expanded (e.g. $HOME).
    Returns a tuple (command, args, error).
    """
    command_line = os.path.expandvars(command_line)

    try:
        parts = shlex.split(command_line)
    except ValueError as error:
        return None, [], f"Error: {error}"

    if not parts:
        return None, [], None

    return parts[0], parts[1:], None


def format_command(command, args):
    """Format a command and its arguments for stub output."""
    if args:
        return f"{command} {' '.join(args)}"
    return command


def check_arity(command, args):
    """Return an error message for wrong argument count, else None."""
    limit = MAX_ARGUMENTS.get(command)
    if limit is None or len(args) <= limit:
        return None
    if limit == 0:
        return f"Error: {command}: no arguments expected"
    return f"Error: {command}: invalid number of arguments"


def execute_ls(args, vfs):
    """List a directory in the VFS, or echo the stub command."""
    if vfs is None:
        return format_command("ls", args)
    path = args[0] if args else vfs.cwd
    lines, error = vfs.ls(path)
    if error:
        return error
    return "\n".join(lines)


def execute_cd(args, vfs):
    """Change the current directory in the VFS, or echo the stub."""
    if vfs is None:
        return format_command("cd", args)
    path = args[0] if args else ROOT_PATH
    return vfs.cd(path) or ""


def execute_head(args, vfs):
    """Print the first lines of a VFS file."""
    if vfs is None:
        return format_command("head", args)
    if not args:
        return "Error: head: missing file operand"
    data, error = vfs.read_file(args[0])
    if error:
        return error
    lines = data.decode("utf-8", errors="replace").splitlines()
    return "\n".join(lines[:HEAD_DEFAULT_LINES])


def execute_tac(args, vfs):
    """Print the lines of a VFS file in reverse order."""
    if vfs is None:
        return format_command("tac", args)
    if not args:
        return "Error: tac: missing file operand"
    data, error = vfs.read_file(args[0])
    if error:
        return error
    lines = data.decode("utf-8", errors="replace").splitlines()
    return "\n".join(reversed(lines))


def execute_wc(args, vfs):
    """Count lines, words and bytes in a VFS file."""
    if vfs is None:
        return format_command("wc", args)
    if not args:
        return "Error: wc: missing file operand"
    data, error = vfs.read_file(args[0])
    if error:
        return error
    lines = data.count(b"\n")
    words = len(data.split())
    return f"{lines} {words} {len(data)}"


def execute_exit(args, vfs):
    """Signal the REPL to terminate."""
    return EXIT_SENTINEL


COMMANDS = {
    "ls": execute_ls,
    "cd": execute_cd,
    "head": execute_head,
    "tac": execute_tac,
    "wc": execute_wc,
    "exit": execute_exit,
}


def execute_command(command_line, vfs=None):
    """Execute a single emulator command line.

    When vfs is None, ls, cd, head, tac and wc behave as stubs.
    Returns the text to print, the sentinel "EXIT" to stop the
    REPL, or an empty string for blank input.
    """
    command, args, error = parse_command(command_line)
    if error:
        return error

    if command is None:
        return ""

    handler = COMMANDS.get(command)
    if handler is None:
        return f"Error: unknown command: {command}"

    arity_error = check_arity(command, args)
    if arity_error:
        return arity_error

    return handler(args, vfs)
