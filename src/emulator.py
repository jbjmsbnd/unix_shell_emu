"""Command parser and executor for the VFS shell emulator (Stage 1)."""

import os
import shlex

# Name of the virtual file system shown in the window title.
VFS_NAME = "myVFS"

# Per-command maximum number of arguments.
MAX_ARGUMENTS = {
    "ls": 1,
    "cd": 1,
    "exit": 0,
}


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


def execute_ls(args):
    """Stub for ls: echo the command and its arguments."""
    return format_command("ls", args)


def execute_cd(args):
    """Stub for cd: echo the command and its arguments."""
    return format_command("cd", args)


def execute_exit(args):
    """Signal the REPL to terminate."""
    return "EXIT"


COMMANDS = {
    "ls": execute_ls,
    "cd": execute_cd,
    "exit": execute_exit,
}


def execute_command(command_line):
    """Execute a single emulator command line.

    Returns the text to print, the sentinel "EXIT" to stop the REPL,
    or an empty string for blank input.
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

    return handler(args)