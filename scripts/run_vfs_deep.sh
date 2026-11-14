#!/usr/bin/env bash
# Run emulator with the deep test VFS.
set -euo pipefail
cd "$(dirname "$0")/.."
python scripts/make_vfs.py
python -m src.main --vfs scripts/vfs/deep.zip \
    --script scripts/start_deep.emu
