#!/usr/bin/env bash
# gh_issues tool — List GitHub issues via gh CLI
# Subprocess protocol: stdin=JSON, stdout=JSON

set -euo pipefail

INPUT=$(cat)
REPO=$(echo "$INPUT" | python3 -c "import json,sys; d=json.load(sys.stdin).get('arguments',{}); print(d.get('repo',''))")
STATE=$(echo "$INPUT" | python3 -c "import json,sys; d=json.load(sys.stdin).get('arguments',{}); print(d.get('state','open'))")
LABEL=$(echo "$INPUT" | python3 -c "import json,sys; d=json.load(sys.stdin).get('arguments',{}); print(d.get('label',''))")
LIMIT=$(echo "$INPUT" | python3 -c "import json,sys; d=json.load(sys.stdin).get('arguments',{}); print(d.get('limit',20))")

if [ -z "$REPO" ]; then
  echo '{"content":"Error: repo is required (format: owner/repo)","is_error":true}'
  exit 0
fi

if ! command -v gh &>/dev/null; then
  echo '{"content":"Error: gh CLI not installed. Run: brew install gh","is_error":true}'
  exit 0
fi

CMD="gh issue list --repo $REPO --state $STATE --limit $LIMIT --json number,title,state,assignees,labels,createdAt,author"
if [ -n "$LABEL" ]; then
  CMD="$CMD --label $LABEL"
fi

if OUTPUT=$(eval "$CMD" 2>&1); then
  # Format as readable text
  FORMATTED=$(echo "$OUTPUT" | python3 -c "
import json, sys
issues = json.load(sys.stdin)
if not issues:
    print('No issues found.')
else:
    for i in issues:
        num = i.get('number','')
        title = i.get('title','')
        state = i.get('state','')
        author = i.get('author',{}).get('login','')
        labels = ', '.join(l.get('name','') for l in i.get('labels',[]))
        assignees = ', '.join(a.get('login','') for a in i.get('assignees',[]))
        line = f'#{num} [{state}] {title}'
        if author: line += f' (by @{author})'
        if labels: line += f' [{labels}]'
        if assignees: line += f' -> {assignees}'
        print(line)
")
  echo "{\"content\":$(echo "$FORMATTED" | python3 -c 'import json,sys; print(json.dumps(sys.stdin.read()))'),\"is_error\":false}"
else
  echo "{\"content\":$(echo "gh error: $OUTPUT" | python3 -c 'import json,sys; print(json.dumps(sys.stdin.read()))'),\"is_error\":true}"
fi
