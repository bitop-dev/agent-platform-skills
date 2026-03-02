---
name: test_writer
version: 1.0.0
description: "Generate unit, integration, and e2e tests with coverage patterns, edge cases, and mocking strategies. Use when the user asks to write tests or improve test coverage."
author: platform-team
tags: [testing, unit-tests, coverage, tdd]
emoji: "🧪"
always: false
requires: {}
---

# Test Writer

Generate comprehensive tests for code. Apply these patterns when writing tests in any language.

## Test Structure (Arrange-Act-Assert)

```
1. ARRANGE — Set up test data, mocks, preconditions
2. ACT     — Call the function/method under test
3. ASSERT  — Verify the result matches expectations
```

## What to Test

### Happy Path
- Normal input produces expected output
- All return fields are correct, not just the primary one

### Edge Cases
- Empty input (nil, "", 0, empty slice)
- Boundary values (max int, max length, exactly at limit)
- Single element collections
- Unicode/special characters in strings

### Error Cases
- Invalid input returns appropriate error
- Error messages are descriptive (not just "error occurred")
- Partial failure (some items succeed, some fail)
- Network/IO errors (timeouts, connection refused)

### Concurrency (if applicable)
- Race conditions (run with `-race` flag)
- Multiple goroutines/threads accessing shared state
- Deadlock scenarios

## Naming Convention

```
Test[Function]_[Scenario]_[ExpectedBehavior]

TestCreateUser_ValidInput_ReturnsUser
TestCreateUser_DuplicateEmail_ReturnsConflict
TestCreateUser_EmptyName_ReturnsValidationError
```

## Table-Driven Tests (Go)

```go
tests := []struct {
    name    string
    input   Input
    want    Output
    wantErr bool
}{
    {"valid input", validInput, expectedOutput, false},
    {"empty name", emptyNameInput, Output{}, true},
}
for _, tt := range tests {
    t.Run(tt.name, func(t *testing.T) {
        got, err := Function(tt.input)
        if (err != nil) != tt.wantErr { ... }
        if !tt.wantErr && got != tt.want { ... }
    })
}
```

## Mocking Guidelines
- Mock external dependencies (DB, HTTP, filesystem), not internal logic
- Use interfaces for mockable boundaries
- Verify mock interactions (was the right method called with the right args?)
- Don't over-mock — if you're mocking 5 things, the function does too much

## Coverage Targets
- **Unit tests**: 80%+ line coverage for business logic
- **Integration tests**: Cover all API endpoints and DB queries
- **E2E tests**: Cover critical user flows (happy path only is fine)
