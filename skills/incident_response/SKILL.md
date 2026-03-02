---
name: incident_response
version: 1.0.0
description: "Incident management — severity classification, root cause analysis, timeline reconstruction, and blameless postmortem generation."
author: platform-team
tags: [incident, postmortem, on-call, sre]
emoji: "🚨"
always: false
requires: {}
---

# Incident Response

Structured incident management methodology. Use when triaging incidents, writing postmortems, or building runbooks.

## Severity Classification

| Severity | Impact | Response | Example |
|---|---|---|---|
| **SEV-1** | Service down, data loss, security breach | All hands, war room, 15min updates | API returning 500s for all users |
| **SEV-2** | Major feature broken, significant degradation | On-call + backup, 30min updates | Agent runs failing for 50% of users |
| **SEV-3** | Minor feature broken, workaround exists | On-call during business hours | Scheduled runs delayed by 5 minutes |
| **SEV-4** | Cosmetic, minor inconvenience | Next sprint | Dashboard shows wrong timezone |

## Incident Timeline

Build a timeline immediately. Include:

```markdown
| Time (UTC) | Event | Actor |
|---|---|---|
| 14:00 | Alert fired: API error rate > 5% | PagerDuty |
| 14:03 | On-call acknowledged | @engineer |
| 14:10 | Identified: DB connection pool exhausted | @engineer |
| 14:15 | Mitigation: Restarted API pods | @engineer |
| 14:18 | Error rate returned to normal | Monitoring |
| 14:30 | Root cause: Missing connection timeout in new migration | @engineer |
| 15:00 | Fix deployed: Added 30s connection timeout | @engineer |
```

## Root Cause Analysis (5 Whys)

```
1. Why did the API return 500s?
   → DB connection pool was exhausted

2. Why was the pool exhausted?
   → Connections were not being returned after use

3. Why weren't connections returned?
   → New migration held transactions open indefinitely

4. Why did the migration hold transactions?
   → Missing timeout on ALTER TABLE (locks table)

5. Why was there no timeout?
   → Migration template doesn't include timeout defaults
   → ROOT CAUSE: Missing safety defaults in migration tooling
```

## Blameless Postmortem Template

```markdown
# Incident Postmortem: [Title]

**Date**: [date]
**Duration**: [start to resolution]
**Severity**: [SEV-1/2/3/4]
**Author**: [name]

## Summary
[2-3 sentences: what happened, impact, resolution]

## Impact
- [X] users affected for [Y] minutes
- [Z] failed requests / lost data / etc.

## Timeline
[See timeline table above]

## Root Cause
[Clear, technical explanation. No blame.]

## What Went Well
- Alert fired within 3 minutes
- Runbook was accurate and up to date

## What Went Wrong
- Took 10 minutes to identify root cause
- No automated rollback for migrations

## Action Items
| Action | Owner | Priority | Due |
|---|---|---|---|
| Add connection timeout to migration template | @eng | P1 | This week |
| Add DB connection pool monitoring | @sre | P2 | Next sprint |
| Runbook: Add migration rollback steps | @eng | P2 | Next sprint |

## Lessons Learned
[What should the team internalize?]
```

## Key Principles
1. **Blameless** — Focus on systems, not people
2. **Timeline first** — Reconstruct what happened before analyzing why
3. **Action items with owners** — Every finding becomes a tracked task
4. **Share widely** — Postmortems are learning tools, not punishment
