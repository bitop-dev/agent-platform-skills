---
name: release_notes
version: 1.0.0
description: "User-facing release notes — feature descriptions, migration guides, breaking change callouts, and audience-aware tone."
author: platform-team
tags: [release, documentation, communication, product]
emoji: "📢"
always: false
requires: {}
---

# Release Notes

Write user-facing release notes that are clear, complete, and audience-appropriate. Use when preparing releases, communicating changes, or writing update announcements.

## Structure

```markdown
# Release v1.5.0

> One-line summary of the most exciting change.

## 🎉 What's New

### AI Teams — Multi-Agent Workflows
Chain multiple agents together into automated pipelines. Each step's output
feeds into the next agent's mission. Build research-to-report flows,
bug triage pipelines, and more.

[Screenshot or diagram if applicable]

**How to use**: Navigate to AI Teams → New Workflow → add steps → Run.

### Skill Credentials
Store API keys for third-party services (GitHub, Slack, Jira) securely.
Credentials are encrypted at rest and automatically injected into skill
tools when your agents run.

## 🔧 Improvements
- Agent creation now supports custom model names — type any model ID
- API keys can be edited (label, base URL, rotation) without re-creating
- Credentials page dynamically shows what each skill needs

## 🐛 Bug Fixes
- Fixed crash when opening credential form (Radix UI empty value)
- Fixed NullString serialization in workflow API responses

## ⚠️ Breaking Changes
- `POST /api/v1/runs` now requires `user_id` field (was optional)
  **Migration**: Add the authenticated user's ID to run requests.

## 📋 Migration Guide
[Only if there are breaking changes or required manual steps]

1. Update your API client to include `user_id` in run requests
2. Re-sync skill sources to pick up `requires_env` metadata
```

## Writing Guidelines

### Audience Awareness
| Audience | Tone | Detail level |
|---|---|---|
| End users | Friendly, benefit-focused | What it does, how to use it |
| Developers | Technical, precise | API changes, code examples, migration steps |
| Ops/SRE | Infrastructure-focused | Config changes, deployment notes, monitoring |

### Do's
- ✅ Lead with the most impactful change
- ✅ Use screenshots/GIFs for visual features
- ✅ Include "how to use" for new features
- ✅ Link to docs for details
- ✅ Call out breaking changes prominently
- ✅ Thank contributors

### Don'ts
- ❌ Internal implementation details ("refactored the DAG executor")
- ❌ Jargon without explanation
- ❌ Burying breaking changes at the bottom
- ❌ "Various bug fixes" — be specific
- ❌ Changes without context ("Updated config handling" — why?)
