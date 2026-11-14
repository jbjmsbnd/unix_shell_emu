@echo off
rem Run emulator with the several-files test VFS.
cd /d "%~dp0.."
python scripts\make_vfs.py
python -m src.main --vfs scripts\vfs\several.zip --script scripts\start_several.emu
