---
name: jira
version: 1.0.0
description: "Jira Cloud issue management — list, create, and update issues via REST API. Use when the user asks about Jira tickets, needs to file bugs, or track work."
author: platform-team
tags: [jira, project-management, issues, tracking]
emoji: "📋"
always: false
runtime: wasm
requires: {}
---

# Jira

Manage Jira Cloud issues via the REST API. Runs as a sandboxed WASM module.

## Tools
- **jira_list_issues** — Search issues with JQL
- **jira_create_issue** — Create a new issue
- **jira_update_issue** — Update an existing issue (status, assignee, fields)

## Required Credentials
- `JIRA_API_TOKEN` — Jira API token (generate at https://id.atlassian.com/manage-profile/security/api-tokens)
- `JIRA_BASE_URL` — Your Jira instance URL (e.g. `https://yourteam.atlassian.net`)
- `JIRA_EMAIL` — Email associated with the API token
