#!/usr/bin/env bash
# PreToolUse hook — deny-list critical paths and warn on migrations.
# Claude Code passes the tool payload as JSON on stdin; we allow-list this
# codebase's Bash commands and block writes to protected files.
set -euo pipefail

payload="$(cat)"
tool_name="$(echo "$payload" | python -c 'import json,sys;print(json.load(sys.stdin).get("tool_name",""))' 2>/dev/null || true)"
tool_input="$(echo "$payload" | python -c 'import json,sys;print(json.dumps(json.load(sys.stdin).get("tool_input",{})))' 2>/dev/null || echo '{}')"

case "$tool_name" in
  Write|Edit)
    path=$(echo "$tool_input" | python -c 'import json,sys;print(json.load(sys.stdin).get("file_path",""))' 2>/dev/null || true)
    case "$path" in
      *.env|*/.env|*/backend/.env|*/infra/terraform/envs/prod/*)
        echo "BLOCKED: writing to $path requires operator confirmation." >&2
        exit 2 ;;
      */app/db/migrations/versions/*)
        echo "WARNING: editing an existing migration file. Prefer a follow-up revision." >&2
        ;;
    esac
    ;;
esac
exit 0
