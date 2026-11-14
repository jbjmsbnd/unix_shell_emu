@echo off
rem Run emulator with the deep test VFS.
cd /d "%~dp0.."
python scripts\make_vfs.py
python -m src.main --vfs scripts\vfs\deep.zip --script scripts\start_deep.emu
