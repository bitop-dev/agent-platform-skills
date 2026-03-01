#!/usr/bin/env bash
# gh_prs tool — List GitHub pull requests via gh CLI
# Subprocess protocol: stdin=JSON, stdout=JSON

set -euo pipefail

INPUT=$(cat)
REPO=$(echo "$INPUT" | python3 -c "import json,sys; d=json.load(sys.stdin).get('arguments',{}); print(d.get('repo',''))")
STATE=$(echo "$INPUT" | python3 -c "import json,sys; d=json.load(sys.stdin).get('arguments',{}); print(d.get('state','open'))")
LIMIT=$(echo "$INPUT" | python3 -c "import json,sys; d=json.load(sys.stdin).get('arguments',{}); print(d.get('limit',20))")

if [ -z "$REPO" ]; then
  echo '{"content":"Error: repo is required (format: owner/repo)","is_error":true}'
  exit 0
fi

if ! command -v gh &>/dev/null; then
  echo '{"content":"Error: gh CLI not installed. Run: brew install gh","is_error":true}'
  exit 0
fi

CMD="gh pr list --repo $REPO --state $STATE --limit $LIMIT --json number,title,state,author,reviewDecision,headRefName,createdAt"

if OUTPUT=$(eval "$CMD" 2>&1); then
  FORMATTED=$(echo "$OUTPUT" | python3 -c "
import json, sys
prs = json.load(sys.stdin)
if not prs:
    print('No pull requests found.')
else:
    for p in prs:
        num = p.get('number','')
        title = p.get('title','')
        state = p.get('state','')
        author = p.get('author',{}).get('login','')
        review = p.get('reviewDecision','')
        branch = p.get('headRefName','')
        line = f'#{num} [{state}] {title}'
        if author: line += f' (by @{author})'
        if branch: line += f' [{branch}]'
        if review: line += f' review:{review}'
        print(line)
")
  echo "{\"content\":$(echo "$FORMATTED" | python3 -c 'import json,sys; print(json.dumps(sys.stdin.read()))'),\"is_error\":false}"
else
  echo "{\"content\":$(echo "gh error: $OUTPUT" | python3 -c 'import json,sys; print(json.dumps(sys.stdin.read()))'),\"is_error\":true}"
fi
