@echo off
rem Run all stage 1-3 commands in the console with a VFS.
cd /d "%~dp0.."
python scripts\make_vfs.py
python -m src.main --vfs scripts\vfs\deep.zip --script scripts\start_all_commands.emu --no-gui
