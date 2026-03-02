---
name: sql_analyst
version: 1.0.0
description: "SQL analysis — schema design review, query optimization, explain plan interpretation, and index recommendations."
author: platform-team
tags: [sql, database, optimization, schema]
emoji: "🗄️"
always: false
requires: {}
---

# SQL Analyst

Analyze SQL schemas, optimize queries, and review database design. Apply when working with databases, reviewing migrations, or debugging slow queries.

## Schema Review

### Table Design
- Primary keys: prefer UUIDs or auto-increment integers, never business data
- Foreign keys: always define them, with appropriate ON DELETE behavior
- Timestamps: always include `created_at`, add `updated_at` for mutable rows
- NOT NULL by default — make nullable only when there's a real reason
- Avoid `TEXT` for everything — use appropriate types (INTEGER, BOOLEAN, TIMESTAMP)

### Naming Conventions
- Tables: `snake_case`, plural (`users`, `run_events`)
- Columns: `snake_case`, singular (`user_id`, `created_at`)
- Indexes: `idx_{table}_{columns}` (`idx_runs_agent_id`)
- Foreign keys: `{referenced_table}_id` (`agent_id`, `user_id`)

### Normalization
- 1NF: No repeating groups (use a join table instead of comma-separated values)
- 2NF: Every non-key column depends on the whole key
- 3NF: No transitive dependencies
- Denormalize only with measured evidence of read performance need

## Query Optimization

### Index Strategy
```sql
-- Index columns that appear in:
WHERE clause          → Single-column index
JOIN conditions       → Foreign key index (usually automatic)
ORDER BY              → Composite index matching sort order
WHERE + ORDER BY      → Composite index (filter cols first, sort cols last)
```

### Common Anti-Patterns
```sql
-- ❌ Function on indexed column (can't use index)
WHERE LOWER(email) = 'user@example.com'
-- ✅ Store normalized, index normalized
WHERE email_lower = 'user@example.com'

-- ❌ SELECT * (fetches unnecessary data)
SELECT * FROM runs WHERE agent_id = ?
-- ✅ Select only needed columns
SELECT id, status, created_at FROM runs WHERE agent_id = ?

-- ❌ N+1 queries (loop with individual SELECTs)
-- ✅ JOIN or batch IN clause

-- ❌ OFFSET for deep pagination (scans all skipped rows)
WHERE id > last_seen_id ORDER BY id LIMIT 20
-- ✅ Keyset pagination
```

### EXPLAIN Plan Reading
| Key indicator | Meaning |
|---|---|
| `Seq Scan` | Full table scan — add an index |
| `Index Scan` | Using index — good |
| `Index Only Scan` | Covered index — best |
| `Hash Join` | Joining via hash table — OK for large joins |
| `Nested Loop` | Joining row-by-row — bad for large tables |
| `Sort` | Sorting in memory — check if index can provide order |
| `rows=` estimate | If wildly off, run ANALYZE to update statistics |

## Output Format
```markdown
## Schema Review: [table/migration]
- ✅ Good: [what's correct]
- ⚠️ Issue: [problem + fix]
- 📊 Index suggestion: [column + rationale]
- ⏱️ Query optimization: [before/after with explanation]
```
