# agent-platform-skills

Community skill registry for [agent-core](https://github.com/bitop-dev/agent-core).

Skills are installable packages that extend agent capabilities with instructions and/or sandboxed tools.

> **Status**: 10 skills — 4 WASM tool skills + 6 instruction-only skills. All tool skills compile to WebAssembly.

---

## How It Works

**All tool skills are compiled to WebAssembly (WASM)** and executed inside [Wazero](https://wazero.io/)'s sandbox runtime. This means:

- **Zero dependencies** — no Python, no pip, no npm, no shell scripts to install
- **Install and run** — `agent-core skill install web_search` and it works immediately
- **Sandboxed** — tools can only access resources explicitly granted (filesystem paths, network hosts)
- **Portable** — `.wasm` binaries run on any OS/arch where agent-core runs
- **Fast** — ~530ms first call, ~3ms cached (160× speedup via SHA-256 module cache)

Instruction-only skills are plain markdown injected into the agent's system prompt — no executable, no runtime.

---

## Skills

### Tool Skills (WASM Sandboxed)

| Skill | Version | Description | Network Access | WASM Size |
|-------|---------|-------------|----------------|-----------|
| 🔍 `web_search` | 2.0.0 | Search the web via DuckDuckGo HTML | `html.duckduckgo.com` | 3.4 MB |
| 🌐 `web_fetch` | 2.0.0 | Fetch URL, extract readable content | Target URL host | 3.8 MB |
| 🐙 `github` | 2.0.0 | GitHub issues & PRs via REST API | `api.github.com` | 3.2 MB × 2 |
| 💬 `slack_notify` | 2.0.0 | Post to Slack via incoming webhook | `hooks.slack.com` | 3.2 MB |

### Instruction-Only Skills

| Skill | Version | Description |
|-------|---------|-------------|
| 📝 `summarize` | 0.1.0 | Summarize long text into concise output |
| 📊 `report` | 0.1.0 | Structure output into formatted markdown reports |
| 🔍 `code_review` | 1.0.0 | Systematic code review with actionable feedback |
| 📋 `data_extract` | 1.0.0 | Extract structured data from unstructured text |
| 📖 `write_doc` | 1.0.0 | Write clear technical documentation |
| 🐛 `debug_assist` | 1.0.0 | Systematic debugging methodology |

---

## Installation

```bash
# Install a skill
agent-core skill install web_search

# List installed skills
agent-core skill list

# Update a skill
agent-core skill update web_search

# Show skill info
agent-core skill show web_search

# Remove a skill
agent-core skill remove web_search
```

---

## Using Skills in Agent Config

### WASM Skill (web search)

```yaml
name: researcher
model: gpt-4o
skills:
  - web_search
  - web_fetch
  - summarize

sandbox:
  mode: wasm
  allowed_hosts:
    - html.duckduckgo.com
    - "*"                    # web_fetch needs any host
  max_timeout_sec: 30
```

### GitHub + Slack (authenticated WASM)

```yaml
name: standup-bot
model: claude-sonnet-4-20250514
skills:
  - github
  - slack_notify
  - report

sandbox:
  mode: wasm
  allowed_hosts:
    - api.github.com
    - hooks.slack.com
  env_vars:
    GITHUB_TOKEN: ${GITHUB_TOKEN}
    SLACK_WEBHOOK_URL: ${SLACK_WEBHOOK_URL}
```

### Instruction-Only (no sandbox needed)

```yaml
name: writer
model: gpt-4o
skills:
  - summarize
  - write_doc
  - code_review
# No sandbox block needed — instruction skills have no tools
```

---

## Skill Structure

```
skills/web_search/
├── SKILL.md                    # Metadata (frontmatter) + instructions (body)
├── tools/
│   ├── web_search.json         # Tool schema (name, description, parameters)
│   └── web_search.wasm         # Compiled WASM module (Go → wasip1)
└── tests/                      # Optional test fixtures
    ├── web_search.basic.json
    └── web_search.basic.expected.json
```

### SKILL.md Frontmatter

```yaml
---
name: web_search
version: 2.0.0
description: "Search the web via DuckDuckGo"
author: platform-team
tags: [web, search]
emoji: "🔍"
runtime: wasm
config:
  max_results:
    type: integer
    default: 10
---

# Instructions (injected into system prompt)

Search the web using DuckDuckGo and return titles, URLs, and snippets...
```

---

## Building WASM Tool Skills

Tools are written in Go and compiled to WebAssembly. They read JSON from stdin and write JSON to stdout.

### 1. Write the tool

```go
package main

import (
    "encoding/json"
    "os"
    "github.com/bitop-dev/agent-core/pkg/hostcall"
)

func main() {
    var input struct {
        Name      string          `json:"name"`
        Arguments json.RawMessage `json:"arguments"`
    }
    json.NewDecoder(os.Stdin).Decode(&input)

    var args struct {
        Query string `json:"query"`
    }
    json.Unmarshal(input.Arguments, &args)

    // HTTP via host function (enforces AllowedHosts)
    body, status := hostcall.HTTPGet("https://example.com/search?q=" + args.Query)

    // Or with custom headers (authenticated APIs)
    body, status = hostcall.HTTPRequestWithHeaders(
        "GET", "https://api.github.com/repos/golang/go",
        "Authorization: Bearer token\nAccept: application/json",
        "",
    )

    json.NewEncoder(os.Stdout).Encode(map[string]any{
        "results": string(body),
        "status":  status,
    })
}
```

### 2. Compile to WASM

```bash
GOOS=wasip1 GOARCH=wasm go build -o tools/my_tool.wasm .
```

### 3. Create the tool schema

```json
{
  "name": "my_tool",
  "description": "Does something useful",
  "parameters": {
    "type": "object",
    "properties": {
      "query": { "type": "string", "description": "Search query" }
    },
    "required": ["query"]
  }
}
```

### 4. Create SKILL.md

```yaml
---
name: my_tool
version: 1.0.0
runtime: wasm
---
# My Tool
Instructions for the LLM on how to use this tool.
```

### Host Functions Available

| Function | Description |
|---|---|
| `hostcall.HTTPGet(url)` | HTTP GET, returns `(body, status)` |
| `hostcall.HTTPPost(url, body)` | HTTP POST, returns `(body, status)` |
| `hostcall.HTTPRequestWithHeaders(method, url, headers, body)` | Full HTTP with custom headers |

Headers are passed as `Key: Value\n` pairs. The host enforces `AllowedHosts` — if the sandbox config doesn't permit the target host, the request is denied.

---

## Building Container Tool Skills

For tools that need full OS access (heavy computation, native binaries, etc.):

### 1. Write a tool that reads JSON stdin, writes JSON stdout

```go
package main

import (
    "encoding/json"
    "os"
)

func main() {
    var input struct {
        Name      string          `json:"name"`
        Arguments json.RawMessage `json:"arguments"`
    }
    json.NewDecoder(os.Stdin).Decode(&input)

    // Full OS access — network, filesystem, anything
    result := doHeavyWork(input.Arguments)

    json.NewEncoder(os.Stdout).Encode(result)
}
```

### 2. Build a Docker image

```dockerfile
FROM golang:1.23-alpine AS builder
WORKDIR /app
COPY . .
RUN go build -ldflags="-s -w" -o tool .

FROM alpine:3.21
COPY --from=builder /app/tool /usr/local/bin/tool
ENTRYPOINT ["tool"]
```

### 3. Create SKILL.md with container runtime

```yaml
---
name: heavy_compute
version: 1.0.0
runtime: container
image: myregistry/heavy-compute:latest
---
```

Container tools run with security hardening by default:
- `--read-only` root filesystem
- `--no-new-privileges`
- `--memory=256m --cpus=1`
- `--network=none` (enabled if `AllowedHosts` set)
- `--rm` (ephemeral, destroyed after each call)

---

## Registry Format

`registry.json` lists all available skills:

```json
{
  "version": "2.0.0",
  "skills": [
    {
      "name": "web_search",
      "version": "2.0.0",
      "runtime": "wasm",
      "has_tools": true,
      "requires_bins": [],
      "requires_env": []
    }
  ]
}
```

### Using as a Skill Source

Any GitHub repository with a `registry.json` and `skills/` directory can be used as a skill source:

```bash
# In the web portal — add custom source
POST /api/v1/skill-sources
{"url": "github.com/your-org/custom-skills", "label": "Internal"}

# In agent-core CLI
agent-core skill install my_skill --source github.com/your-org/custom-skills
```

---

## Part of the Agent Platform

| Repo | Purpose | Status |
|---|---|---|
| [agent-core](https://github.com/bitop-dev/agent-core) | Standalone CLI + Go library | ✅ 171 tests, 45 commits |
| [agent-platform-api](https://github.com/bitop-dev/agent-platform-api) | Go Fiber REST API | ✅ 22 tests, 24 commits |
| [agent-platform-web](https://github.com/bitop-dev/agent-platform-web) | React web portal | ✅ 14 pages, 18 commits |
| **agent-platform-skills** (this repo) | Community skill registry | ✅ 10 skills (4 WASM + 6 instruction) |
| [agent-platform-docs](https://github.com/bitop-dev/agent-platform-docs) | Architecture & planning | ✅ Comprehensive |

---

## License

MIT
