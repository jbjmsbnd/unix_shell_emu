#!/usr/bin/env bash
# Run the start script in the console (no GUI).
set -euo pipefail
cd "$(dirname "$0")/.."
python -m src.main --vfs some.zip --script scripts/start_with_errors.emu --no-gui
