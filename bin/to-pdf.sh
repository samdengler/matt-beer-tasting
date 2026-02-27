#!/bin/bash
# Usage: bin/to-pdf.sh input.html [output.pdf]
# Requires: brew install pango, uv sync
set -e
INPUT="${1:?Usage: bin/to-pdf.sh input.html [output.pdf]}"
OUTPUT="${2:-${INPUT%.html}.pdf}"
PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
VENV_PYTHON="$PROJECT_DIR/.venv/bin/python"

if [ ! -f "$VENV_PYTHON" ]; then
    echo "Error: .venv not found. Run 'uv sync' first." >&2
    exit 1
fi

# macOS SIP strips DYLD_* env vars from 'uv run' (protected binary).
# Calling .venv/bin/python directly avoids SIP since it's in userspace.
DYLD_FALLBACK_LIBRARY_PATH=/opt/homebrew/lib \
    "$VENV_PYTHON" -c "
import sys
from weasyprint import HTML
HTML(sys.argv[1]).write_pdf(sys.argv[2])
" "$INPUT" "$OUTPUT"
echo "Created $OUTPUT"
