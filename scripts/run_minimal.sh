#!/usr/bin/env bash
# Run the emulator with no CLI parameters (GUI only).
set -euo pipefail
cd "$(dirname "$0")/.."
python -m src.main
