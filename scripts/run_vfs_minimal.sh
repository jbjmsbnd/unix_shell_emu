#!/usr/bin/env bash
# Run emulator with the minimal test VFS.
set -euo pipefail
cd "$(dirname "$0")/.."
python scripts/make_vfs.py
python -m src.main --vfs scripts/vfs/minimal.zip \
    --script scripts/start_minimal.emu
