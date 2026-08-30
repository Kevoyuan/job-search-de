#!/bin/bash
# Build a styled HTML report from a configured Markdown report.
# Usage: scripts/build_html.sh <workdir> [theme] [markdown-file]
set -u
WD="$1"
THEME="${2:-modern}"
INPUT="${3:-report_zh.md}"
if [ -z "$THEME" ]; then THEME=modern; fi
SKILL_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
BUN_DIR="$WD/.buntmp"; BUN_INSTALL_DIR="$WD/.buninstall"; mkdir -p "$BUN_DIR" "$BUN_INSTALL_DIR"
export BUN_TMPDIR="$BUN_DIR" BUN_INSTALL="$BUN_INSTALL_DIR" TMPDIR="$BUN_DIR"
if command -v bun >/dev/null 2>&1; then BUN_BIN="$(command -v bun)"; else BUN_BIN="npx -y bun"; fi
MDTOHTML="$SKILL_ROOT/../baoyu-markdown-to-html/scripts/main.ts"
( cd "$WD" && "$BUN_BIN" "$MDTOHTML" "$INPUT" --theme "$THEME" 2>&1 | tail -1 )
OUTPUT="${INPUT%.*}.html"
python3 "$SKILL_ROOT/scripts/fix_html.py" "$WD/$OUTPUT"
