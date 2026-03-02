---
name: changelog
version: 1.0.0
description: "Generate changelogs from git history, commit messages, and PR descriptions. Semver-aware, grouped by type (feat/fix/breaking)."
author: platform-team
tags: [changelog, release, git, semver]
emoji: "📋"
always: false
requires: {}
---

# Changelog

Generate structured changelogs from commit history, PR titles, or release notes. Apply conventional commit parsing and semver-aware grouping.

## Conventional Commits

Parse commits in the format: `type(scope): description`

| Prefix | Category | Semver bump |
|---|---|---|
| `feat:` | ✨ Features | Minor |
| `fix:` | 🐛 Bug Fixes | Patch |
| `perf:` | ⚡ Performance | Patch |
| `docs:` | 📚 Documentation | None |
| `refactor:` | ♻️ Refactoring | None |
| `test:` | 🧪 Tests | None |
| `ci:` | 🔧 CI/CD | None |
| `chore:` | 🧹 Chores | None |
| `BREAKING CHANGE:` | 💥 Breaking Changes | Major |

## Output Format

```markdown
# Changelog

## [1.5.0] - 2026-03-01

### 💥 Breaking Changes
- **api**: Removed deprecated `/v1/legacy` endpoint (#234)

### ✨ Features
- **agents**: Added AI Teams workflow builder (#220)
- **credentials**: Per-user encrypted skill credentials (#215)

### 🐛 Bug Fixes
- **runner**: Fixed race condition in concurrent run dispatch (#218)
- **ui**: Fixed SelectItem empty value crash (#222)

### ⚡ Performance
- **wasm**: Module caching reduces cold start from 530ms to 3ms (#210)

### 📚 Documentation
- Updated README with accurate endpoint counts (#225)
```

## Guidelines

1. **Group by type** — Features first, then fixes, then everything else
2. **Include PR/issue numbers** when available — linkable references
3. **Scope in bold** — helps scanning (`**agents**: Added...`)
4. **User-facing language** — "Added AI Teams" not "Implemented workflow orchestrator DAG engine"
5. **Breaking changes always first** — most important for consumers
6. **Date format**: ISO 8601 (YYYY-MM-DD)
7. **Version**: Follow semver — breaking=major, feature=minor, fix=patch
