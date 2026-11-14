#!/usr/bin/env bash
# Run emulator with the several-files test VFS.
set -euo pipefail
cd "$(dirname "$0")/.."
python scripts/make_vfs.py
python -m src.main --vfs scripts/vfs/several.zip \
    --script scripts/start_several.emu
