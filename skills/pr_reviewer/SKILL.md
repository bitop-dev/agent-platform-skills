---
name: pr_reviewer
version: 1.0.0
description: "Structured pull request review with severity levels, file-grouped feedback, and suggested fixes. Use when reviewing PRs or diffs."
author: platform-team
tags: [code-review, pull-request, github, quality]
emoji: "👀"
always: false
requires: {}
---

# PR Reviewer

Structured pull request review methodology. Use when reviewing code changes, diffs, or PRs.

## Review Process

1. **Understand the purpose** — Read the PR title, description, and linked issue first
2. **Check the big picture** — Does the approach make sense? Is there a simpler way?
3. **Review file by file** — Group feedback by file for clarity
4. **Categorize findings** — Use severity levels so the author knows what's blocking

## Severity Levels

| Level | Emoji | Meaning | Blocks merge? |
|---|---|---|---|
| **Critical** | 🔴 | Bug, security issue, data loss risk | Yes |
| **Warning** | 🟡 | Logic concern, missing edge case, performance issue | Usually |
| **Suggestion** | 🔵 | Better approach, cleaner pattern, readability | No |
| **Nit** | ⚪ | Style, naming, formatting preference | No |
| **Praise** | 🟢 | Good pattern, clever solution, well-tested | No |

## What to Look For

### Correctness
- Does the logic handle all cases?
- Are error conditions handled? (not just happy path)
- Are there off-by-one errors, nil pointer risks, race conditions?

### Design
- Does this follow existing patterns in the codebase?
- Is the abstraction level right? (not too much, not too little)
- Are new dependencies justified?

### Testing
- Are new code paths tested?
- Do tests cover edge cases, not just happy path?
- Are tests readable and maintainable?

### Security
- User input validated/sanitized?
- No secrets in code?
- Auth checks in place?

## Output Format

```markdown
## PR Review: [title]

**Overall**: [approve / request changes / comment]
**Summary**: [1-2 sentence assessment]

### file.go
- 🔴 **L42**: Nil pointer dereference — `user` can be nil when `err != nil`
  ```go
  // suggested fix
  if err != nil { return nil, err }
  ```
- 🔵 **L78**: Consider extracting this into a helper function — it's duplicated in handler.go L55
- 🟢 **L90**: Nice use of table-driven tests

### Overall Suggestions
- [ ] Add error handling for the new API call
- [ ] Consider adding a migration for the schema change
```
