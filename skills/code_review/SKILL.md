---
name: code_review
version: 1.0.0
description: Systematic code review with actionable feedback
tier: community
tags: code, review, quality, security
---

# Code Review

You are performing a systematic code review. Follow this structured approach:

## Review Checklist

### 1. Correctness
- Does the code do what it claims?
- Are there edge cases not handled?
- Are error paths covered?

### 2. Security
- Input validation present?
- SQL injection, XSS, command injection risks?
- Secrets or credentials hardcoded?
- Proper authentication/authorization checks?

### 3. Performance
- Unnecessary allocations or copies?
- N+1 query patterns?
- Missing indexes implied by queries?
- Unbounded loops or recursion?

### 4. Readability
- Clear variable and function names?
- Comments explain *why*, not *what*?
- Consistent style with the codebase?
- Functions doing one thing?

### 5. Testing
- Are there tests for the changes?
- Do tests cover edge cases?
- Are mocks appropriate or overused?

## Output Format

For each issue found, provide:
- **File and line** (if applicable)
- **Severity**: 🔴 Critical, 🟡 Warning, 🟢 Suggestion
- **Issue**: What's wrong
- **Fix**: How to fix it

End with a **Summary** section: overall quality score (1-10) and top 3 priorities.
