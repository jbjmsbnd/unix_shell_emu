"""Tkinter GUI for the VFS shell emulator (Stage 2)."""

import tkinter as tk

from src.emulator import EXIT_SENTINEL, execute_command

# Colour scheme of the output area.
BG_COLOR = "#1e1e1e"
FG_COLOR = "#d4d4d4"
ERROR_COLOR = "#f48771"

# Delay before auto-playing a start script, milliseconds.
AUTOPLAY_DELAY_MS = 100


class ShellWindow:
    """Interactive Tk window bound to the emulator REPL."""

    def __init__(self, title, initial_lines=None):
        """Create the window and build the widgets."""
        self.root = tk.Tk()
        self.root.title(f"{title} Emulator")
        self.root.geometry("700x500")
        self._build_widgets()
        self._initial_lines = list(initial_lines or [])

    def _build_widgets(self):
        """Create output area and command entry."""
        self.output = tk.Text(
            self.root,
            bg=BG_COLOR,
            fg=FG_COLOR,
            insertbackground=FG_COLOR,
        )
        self.output.tag_configure("error", foreground=ERROR_COLOR)
        self.output.pack(fill=tk.BOTH, expand=True)

        self.entry = tk.Entry(self.root)
        self.entry.pack(fill=tk.X)
        self.entry.bind("<Return>", self._on_enter)
        self.entry.focus()

    def _on_enter(self, event=None):
        """Read the entry, run the command, clear the entry."""
        line = self.entry.get()
        self.entry.delete(0, tk.END)
        if line.strip():
            self._execute(line)

    def _execute(self, line):
        """Run one command line and print its output."""
        self._write(f"$ {line}")
        result = execute_command(line)
        if result == EXIT_SENTINEL:
            self.root.destroy()
            return
        if result:
            self._write(result)
        self.output.see(tk.END)

    def _write(self, text):
        """Append a line to the output area with error colouring."""
        tag = "error" if text.startswith("Error:") else None
        self.output.insert(tk.END, f"{text}\n", tag)

    def _autoplay(self):
        """Play initial lines as if the user typed them."""
        if not self._initial_lines:
            return
        line = self._initial_lines.pop(0)
        if line.strip() and not line.lstrip().startswith("#"):
            self._execute(line)
        self.root.after(AUTOPLAY_DELAY_MS, self._autoplay)

    def run(self):
        """Start the Tk event loop."""
        if self._initial_lines:
            self.root.after(AUTOPLAY_DELAY_MS, self._autoplay)
        self.root.mainloop()


def run_gui(title, initial_lines=None):
    """Open the shell window and run it until closed."""
    window = ShellWindow(title, initial_lines)
    window.run()
