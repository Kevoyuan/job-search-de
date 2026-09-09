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
MDTOHTML="$SKILL_ROOT/../baoyu-markdown-to-html/scripts/main.ts"
# NOTE: 不能把 "npx -y bun" 存进单个变量再 "$BUN_BIN" 展开（shell 会把它当成一个
# 名为 "npx -y bun" 的可执行文件，报 command not found）。此时转换步骤静默失败，
# 而下方 fix_html.py 仍会成功处理旧 HTML，导致误以为报告已更新（实际交付的是旧版）。
# 因此这里分两支显式调用，并在转换后校验产物时间戳。
BEFORE_TS=0
[ -f "$WD/${INPUT%.*}.html" ] && BEFORE_TS=$(stat -f %m "$WD/${INPUT%.*}.html" 2>/dev/null || stat -c %Y "$WD/${INPUT%.*}.html" 2>/dev/null || echo 0)
if command -v bun >/dev/null 2>&1; then
  ( cd "$WD" && bun "$MDTOHTML" "$INPUT" --theme "$THEME" 2>&1 | tail -1 )
else
  ( cd "$WD" && npx -y bun "$MDTOHTML" "$INPUT" --theme "$THEME" 2>&1 | tail -1 )
fi
OUTPUT="${INPUT%.*}.html"
AFTER_TS=$(stat -f %m "$WD/$OUTPUT" 2>/dev/null || stat -c %Y "$WD/$OUTPUT" 2>/dev/null || echo 0)
if [ "$AFTER_TS" -le "$BEFORE_TS" ]; then
  echo "ERROR: HTML 转换未产出新文件（$OUTPUT 未更新）。请检查 bun/npx 是否可用后重试。" >&2
  exit 1
fi
python3 "$SKILL_ROOT/scripts/fix_html.py" "$WD/$OUTPUT"
