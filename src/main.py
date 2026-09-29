"""Tkinter GUI for the VFS shell emulator (Stage 1)."""

import tkinter as tk

from src.emulator import VFS_NAME, execute_command


def handle_command(event=None):
    """Process the command entered by the user."""
    command_line = command_entry.get()
    command_entry.delete(0, tk.END)

    if not command_line.strip():
        return

    output.insert(tk.END, f"$ {command_line}\n")

    result = execute_command(command_line)

    if result == "EXIT":
        root.destroy()
        return

    if result:
        tag = "error" if result.startswith("Error:") else "normal"
        output.insert(tk.END, f"{result}\n", tag)

    output.see(tk.END)


def main():
    """Start the GUI event loop."""
    global root, output, command_entry

    root = tk.Tk()
    root.title(f"{VFS_NAME} Emulator")
    root.geometry("700x500")

    output = tk.Text(
        root, bg="#1e1e1e", fg="#d4d4d4", insertbackground="#d4d4d4"
    )
    output.tag_configure("error", foreground="#f48771")
    output.pack(fill=tk.BOTH, expand=True)

    command_entry = tk.Entry(root)
    command_entry.pack(fill=tk.X)
    command_entry.bind("<Return>", handle_command)
    command_entry.focus()

    root.mainloop()


if __name__ == "__main__":
    main()