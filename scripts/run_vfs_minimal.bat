@echo off
rem Run emulator with the minimal test VFS.
cd /d "%~dp0.."
python scripts\make_vfs.py
python -m src.main --vfs scripts\vfs\minimal.zip --script scripts\start_minimal.emu
