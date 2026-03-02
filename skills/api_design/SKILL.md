---
name: api_design
version: 1.0.0
description: "REST and GraphQL API design patterns — resource modeling, endpoint naming, status codes, pagination, and OpenAPI spec generation."
author: platform-team
tags: [api, rest, graphql, openapi, design]
emoji: "🔌"
always: false
requires: {}
---

# API Design

Design well-structured APIs. Apply these patterns when designing endpoints, reviewing API code, or generating OpenAPI specs.

## REST Resource Design

### URL Structure
```
GET    /api/v1/resources          → List (paginated)
POST   /api/v1/resources          → Create
GET    /api/v1/resources/:id      → Get one
PUT    /api/v1/resources/:id      → Full update
PATCH  /api/v1/resources/:id      → Partial update
DELETE /api/v1/resources/:id      → Delete
```

### Naming Rules
- **Plural nouns**: `/users` not `/user`
- **Kebab-case**: `/api-keys` not `/apiKeys`
- **No verbs in URLs**: `POST /runs` not `POST /create-run`
- **Nest for relationships**: `/agents/:id/skills` not `/agent-skills?agent_id=`
- **Actions as sub-resources**: `POST /runs/:id/cancel` (when CRUD doesn't fit)

### Status Codes
| Code | When |
|---|---|
| `200` | Success (GET, PUT, PATCH) |
| `201` | Created (POST that creates) |
| `204` | No content (DELETE) |
| `400` | Bad request (validation error) |
| `401` | Unauthorized (no/invalid token) |
| `403` | Forbidden (valid token, wrong permissions) |
| `404` | Not found |
| `409` | Conflict (duplicate, version mismatch) |
| `422` | Unprocessable (valid JSON but semantic error) |
| `429` | Rate limited |
| `500` | Server error (never leak internals) |

### Pagination
```json
{
  "data": [...],
  "meta": {
    "page": 1,
    "per_page": 20,
    "total": 145,
    "total_pages": 8
  }
}
```
Use `?page=2&per_page=20` query params. Always return total count.

### Filtering & Sorting
```
GET /runs?status=running&agent_id=abc           → Filter
GET /runs?sort=-created_at                      → Sort (- for desc)
GET /runs?status=running&sort=-created_at&page=2 → Combined
```

### Error Response Format
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Name is required",
    "details": [
      {"field": "name", "message": "must not be empty"}
    ]
  }
}
```

### Versioning
- URL path: `/api/v1/...` (simplest, most explicit)
- Bump major version only for breaking changes
- Support old version for at least 6 months after deprecation

## Security Checklist
- [ ] Auth on all non-public endpoints
- [ ] Rate limiting per IP and per user
- [ ] Request ID header for tracing
- [ ] Input validation before processing
- [ ] No internal details in error messages
- [ ] CORS configured per environment
