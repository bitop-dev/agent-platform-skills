---
name: security_audit
version: 1.0.0
description: "OWASP-informed security review — authentication, injection, secrets, dependencies, CORS, headers. Use when reviewing code for security vulnerabilities or hardening a system."
author: platform-team
tags: [security, audit, owasp, vulnerabilities]
emoji: "🔒"
always: false
requires: {}
---

# Security Audit

Systematic security review methodology. Apply these guidelines when auditing code, configs, or infrastructure for vulnerabilities.

## Audit Checklist

### 1. Authentication & Authorization
- [ ] Passwords hashed with bcrypt/scrypt/argon2 (never MD5/SHA1)
- [ ] JWT secrets are strong (≥256 bits), tokens expire, refresh tokens rotate
- [ ] OAuth state parameter validated (CSRF protection)
- [ ] Authorization checks on every endpoint, not just UI
- [ ] No privilege escalation via parameter tampering (IDOR)
- [ ] Rate limiting on auth endpoints (login, register, password reset)

### 2. Injection
- [ ] SQL: parameterized queries everywhere, no string concatenation
- [ ] XSS: output encoding, Content-Security-Policy header
- [ ] Command injection: no shell exec with user input, use exec with args array
- [ ] Path traversal: validate file paths, no `../` in user input
- [ ] SSRF: validate/allowlist URLs before fetching

### 3. Secrets & Configuration
- [ ] No secrets in source code, env files committed, or logs
- [ ] API keys encrypted at rest (AES-256-GCM or similar)
- [ ] `.env` files in `.gitignore`
- [ ] Different secrets per environment (dev/staging/prod)
- [ ] Secrets rotatable without redeployment

### 4. Dependencies
- [ ] No known CVEs in dependencies (`npm audit`, `go vuln`, `pip audit`)
- [ ] Lock files committed (go.sum, package-lock.json, requirements.txt)
- [ ] Minimal dependency tree — fewer deps = smaller attack surface
- [ ] Dependencies from trusted sources only

### 5. Transport & Headers
- [ ] HTTPS everywhere (HSTS header)
- [ ] CORS configured to specific origins (not `*` in production)
- [ ] Security headers: `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`
- [ ] Cookies: `HttpOnly`, `Secure`, `SameSite=Strict`

### 6. Data Protection
- [ ] PII encrypted at rest and in transit
- [ ] Logs don't contain passwords, tokens, or PII
- [ ] Database backups encrypted
- [ ] Data retention policy implemented

## Output Format

```markdown
## Security Audit Report

**Scope**: [what was reviewed]
**Date**: [date]
**Severity Summary**: X critical, Y high, Z medium, W low

### Critical Findings
1. **[TITLE]** — [file:line]
   - Risk: [what could happen]
   - Fix: [specific remediation]

### Recommendations
- [prioritized list]
```
