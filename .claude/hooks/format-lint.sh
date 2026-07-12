#!/usr/bin/env bash
# PostToolUse hook — format + lint the file that was just written.
set -euo pipefail

payload="$(cat)"
file="$(echo "$payload" | python -c 'import json,sys;print(json.load(sys.stdin).get("tool_input",{}).get("file_path",""))' 2>/dev/null || true)"

case "$file" in
  *.py)
    ruff format "$file" >/dev/null 2>&1 || true
    ruff check "$file" --fix >/dev/null 2>&1 || true
    ;;
  *.ts|*.tsx|*.js|*.jsx)
    yarn --cwd "$(dirname "$file")" prettier --write "$file" >/dev/null 2>&1 || true
    ;;
esac
exit 0
