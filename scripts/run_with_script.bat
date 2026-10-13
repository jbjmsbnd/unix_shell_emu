@echo off
rem Run the emulator with VFS and a start script (GUI).
cd /d "%~dp0.."
python -m src.main --vfs some.zip --script scripts\start_simple.emu
