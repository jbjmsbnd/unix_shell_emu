"""Entry point for the VFS shell emulator (Stage 2)."""

import argparse

from src.emulator import VFS_NAME
from src.gui import run_gui
from src.runner import read_script, run_script


def build_parser():
    """Create the command line argument parser."""
    parser = argparse.ArgumentParser(
        prog="unix-shell-emu",
        description="UNIX-like shell emulator with a VFS.",
    )
    parser.add_argument(
        "--vfs",
        metavar="PATH",
        help="path to the VFS archive",
    )
    parser.add_argument(
        "--script",
        metavar="PATH",
        help="path to the start script",
    )
    parser.add_argument(
        "--no-gui",
        action="store_true",
        help="run the start script in the console",
    )
    return parser


def print_debug(args):
    """Print all user-supplied parameters for debugging."""
    print("[debug] vfs    =", args.vfs)
    print("[debug] script =", args.script)
    print("[debug] no_gui =", args.no_gui)


def load_script_lines(path):
    """Read the start script and warn on failure."""
    if not path:
        return []
    lines, error = read_script(path)
    if error:
        print(error)
        return []
    return lines


def run_console(lines):
    """Run start script lines in the console."""
    result = run_script(lines, print)
    print(
        f"[script] total={result.total} "
        f"executed={result.executed} "
        f"failed={result.failed} "
        f"exited={result.exited}"
    )


def main():
    """Parse arguments and start the emulator."""
    parser = build_parser()
    args = parser.parse_args()
    print_debug(args)

    lines = load_script_lines(args.script)
    if args.no_gui:
        run_console(lines)
        return

    run_gui(VFS_NAME, initial_lines=lines)


if __name__ == "__main__":
    main()
