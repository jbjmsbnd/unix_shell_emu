@echo off
rem Run the start script in the console (no GUI).
cd /d "%~dp0.."
python -m src.main --vfs some.zip --script scripts\start_with_errors.emu --no-gui
