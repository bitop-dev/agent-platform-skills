---
name: architect
version: 1.0.0
description: "System architecture analysis — component diagrams, trade-off evaluation, scalability patterns, and Architecture Decision Records (ADR)."
author: platform-team
tags: [architecture, design, scalability, adr]
emoji: "🏗️"
always: false
requires: {}
---

# Architect

System architecture analysis and design. Apply when evaluating technical approaches, designing systems, or documenting architectural decisions.

## Architecture Decision Record (ADR)

Use this format for any significant technical decision:

```markdown
# ADR-001: [Decision Title]

## Status
[Proposed | Accepted | Deprecated | Superseded by ADR-XXX]

## Context
[What is the problem? What constraints exist? What triggered this decision?]

## Decision
[What did we decide? Be specific about the chosen approach.]

## Alternatives Considered
1. **[Alternative A]** — [pros] / [cons] / [why rejected]
2. **[Alternative B]** — [pros] / [cons] / [why rejected]

## Consequences
- ✅ [positive outcome]
- ⚠️ [trade-off or risk]
- 📋 [follow-up work needed]
```

## Design Evaluation Framework

### 1. Functional Requirements
- Does it solve the stated problem?
- Does it handle all user-facing scenarios?
- Are edge cases addressed?

### 2. Non-Functional Requirements
| Attribute | Questions |
|---|---|
| **Scalability** | What's the bottleneck? Where does it break at 10x load? |
| **Reliability** | What happens when [component] fails? Is there a fallback? |
| **Performance** | What's the p99 latency? Where are the hot paths? |
| **Security** | What's the threat model? What's the blast radius? |
| **Operability** | How do we deploy? Monitor? Rollback? Debug in production? |
| **Cost** | What's the infrastructure cost at current and 10x scale? |

### 3. Simplicity Check
- Can you explain it to a new team member in 5 minutes?
- How many moving parts? Can any be removed?
- Are you building for today's problems or imagined future ones?

## Common Patterns

| Pattern | When to use | Trade-off |
|---|---|---|
| **Monolith** | Early stage, small team, fast iteration | Harder to scale individual components |
| **Microservices** | Clear domain boundaries, independent scaling needs | Operational complexity, network latency |
| **Event-driven** | Async workflows, decoupled producers/consumers | Eventual consistency, harder debugging |
| **CQRS** | Read-heavy with different read/write models | Complexity, stale reads |
| **Saga** | Distributed transactions across services | Compensating actions, partial failure |
| **Circuit breaker** | External dependency protection | Needs tuning, can mask real issues |

## Diagramming

When describing architecture, use text diagrams:

```
┌──────────┐     HTTP      ┌──────────┐     SQL      ┌──────────┐
│  Client  │───────────────│   API    │──────────────│    DB    │
└──────────┘               └────┬─────┘              └──────────┘
                                │
                           WebSocket
                                │
                           ┌────▼─────┐
                           │  Runner  │──── WASM Sandbox
                           └──────────┘
```

## Red Flags
- 🚩 "We might need this later" — YAGNI
- 🚩 Shared mutable state without synchronization
- 🚩 No health checks or monitoring
- 🚩 Single point of failure with no fallback
- 🚩 Circular dependencies between services
- 🚩 Configuration that requires redeployment to change
