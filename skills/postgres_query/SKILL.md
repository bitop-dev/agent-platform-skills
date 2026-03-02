---
name: postgres_query
version: 1.0.0
description: "Run read-only SQL queries against PostgreSQL for data analysis. Inspect schemas, run SELECT queries, analyze data."
author: platform-team
tags: [postgres, sql, database, analytics]
emoji: "🐘"
always: false
runtime: wasm
requires: {}
---
# PostgreSQL Query
Run read-only SQL queries against PostgreSQL databases for data analysis. Inspect schemas, run SELECT queries.

**Safety**: All queries are executed as read-only (SET TRANSACTION READ ONLY).

## Required Credentials
- `POSTGRES_URL` — PostgreSQL connection string (e.g. postgres://user:pass@host:5432/dbname)
