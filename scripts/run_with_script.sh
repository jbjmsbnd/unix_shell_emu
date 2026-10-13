#!/usr/bin/env bash
# Run the emulator with VFS and a start script (GUI).
set -euo pipefail
cd "$(dirname "$0")/.."
python -m src.main --vfs some.zip --script scripts/start_simple.emu
