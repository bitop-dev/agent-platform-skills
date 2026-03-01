---
name: github
version: 2.0.0
description: "GitHub operations via the GitHub REST API: issues and pull requests. Use when: checking PR status, listing issues, reviewing repo activity. NOT for: local git operations (use bash + git), non-GitHub repos, or cloning repos (use bash + git clone)."
author: platform-team
tags: [code, vcs, github]
emoji: "🐙"
always: false
runtime: wasm
---

# GitHub Skill

Query GitHub repositories, issues, and pull requests via the GitHub REST API.

Runs as a sandboxed WebAssembly module — no `gh` CLI required, no shell scripts, no Python.
Uses the GitHub REST API directly through the sandbox HTTP host function.

## When to Use

✅ **USE this skill when:**
- Listing open/closed issues for a repository
- Listing open/closed/merged pull requests
- Checking repository activity
- Filtering issues by label or state

❌ **DON'T use this skill when:**
- Local git operations (commit, push, pull, branch) → use `bash` + `git`
- Non-GitHub repos (GitLab, Bitbucket) → use other skills or bash
- Cloning repositories → use `bash` + `git clone`
- Reading local file contents → use `read_file`
- Creating issues/PRs (write operations not yet supported in WASM version)

## Tools

### gh_issues
List issues for a repository.

```json
{"repo": "owner/repo", "state": "open", "label": "bug", "limit": 20}
```

### gh_prs
List pull requests for a repository.

```json
{"repo": "owner/repo", "state": "open", "limit": 20}
```

## Output Format

```
Issues for owner/repo (open):

#142 [open] Fix memory leak in cache (by @author) [bug, priority:high] → @assignee
#139 [open] Add dark mode support (by @author) [enhancement]
```

## Authentication

For public repositories, no authentication is needed. For private repositories, set `GITHUB_TOKEN` in the agent's environment variables:

```yaml
sandbox:
  allowed_hosts:
    - api.github.com
```

> **Note**: The WASM version currently supports read-only operations (list issues, list PRs). For write operations (create, close, comment), use the `bash` tool with `gh` CLI or `curl`.

## Sandbox Requirements

- **Network**: `api.github.com` must be in AllowedHosts
- **Filesystem**: none required
- **Dependencies**: none — single .wasm binary
