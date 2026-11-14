#!/usr/bin/env bash
# Run all stage 1-3 commands in the console with a VFS.
set -euo pipefail
cd "$(dirname "$0")/.."
python scripts/make_vfs.py
python -m src.main --vfs scripts/vfs/deep.zip \
    --script scripts/start_all_commands.emu --no-gui
