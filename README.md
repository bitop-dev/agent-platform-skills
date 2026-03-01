# agent-platform-skills

Community skill registry for [agent-core](https://github.com/bitop-dev/agent-core).

Skills are installable packages that extend agent capabilities with instructions and/or tools.

## Architecture

**All tool-bearing skills are compiled to WebAssembly (WASM)** and executed inside Wazero's sandbox runtime. This means:

- **Zero dependencies** — no Python, no pip, no npm, no shell scripts to manage
- **Install and run** — clone the skill directory, it works immediately
- **Sandboxed execution** — tools can only access resources explicitly granted by the agent's capability policy (filesystem paths, network hosts)
- **Portable** — .wasm binaries run on any OS where agent-core runs

Instruction-only skills (no executable tools) are plain markdown that gets injected into the agent's system prompt.

## Skills

### Tool Skills (WASM Sandboxed)

| Skill | Version | Description | Network Access |
|-------|---------|-------------|----------------|
| 🔍 `web_search` | 2.0.0 | Search the web via DuckDuckGo | `html.duckduckgo.com` |
| 🌐 `web_fetch` | 2.0.0 | Fetch URL, extract readable markdown | Target URL host |
| 🐙 `github` | 2.0.0 | GitHub issues & PRs via REST API | `api.github.com` |
| 💬 `slack_notify` | 2.0.0 | Post to Slack via webhook | `hooks.slack.com` |

### Instruction-Only Skills

| Skill | Version | Description |
|-------|---------|-------------|
| 📝 `summarize` | 0.1.0 | Summarize long text into concise output |
| 📊 `report` | 0.1.0 | Structure output into formatted markdown reports |
| 🔍 `code_review` | 1.0.0 | Systematic code review with actionable feedback |
| 📋 `data_extract` | 1.0.0 | Extract structured data from unstructured text |
| 📖 `write_doc` | 1.0.0 | Write clear technical documentation |
| 🐛 `debug_assist` | 1.0.0 | Systematic debugging methodology |

## Installation

```bash
# Install a skill
agent-core skill install web_search

# List installed skills
agent-core skill list

# Update a skill
agent-core skill update web_search
```

## Using Skills in Agent Config

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
    - "*"   # or restrict to specific hosts
```

## Skill Structure

```
skills/web_search/
├── SKILL.md                    # Metadata (frontmatter) + instructions (body)
├── tools/
│   ├── web_search.json         # Tool schema (name, description, parameters)
│   └── web_search.wasm         # Compiled WASM module
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
runtime: wasm          # wasm | container | subprocess (legacy)
config:
  max_results:
    type: integer
    default: 10
---
```

### Runtime Types

| Runtime | Description | Dependencies | Sandboxing |
|---------|-------------|-------------|------------|
| `wasm` | WebAssembly module via Wazero | None | Capability-based (fs, network) |
| `container` | Docker/Podman OCI container | Docker/Podman | Full isolation |
| `subprocess` | Raw OS process (legacy) | Language runtime (Python, etc.) | Minimal |
| *(empty)* | Instruction-only skill | None | N/A |

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) (coming soon).

### Building WASM Tools

Tools are written in Go and compiled to WASM:

```bash
cd tools/web_search/
GOOS=wasip1 GOARCH=wasm go build -o web_search.wasm .
```

Tools use the `hostcall` package from agent-core for network access:

```go
import "github.com/bitop-dev/agent-core/internal/sandbox/testdata/hostcall"

body, err := hostcall.HTTPGet("https://example.com")
```

The host enforces `AllowedHosts` — if the agent's sandbox config doesn't permit the target host, the request is denied.

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

Any GitHub repository with a `registry.json` and `skills/` directory can be used as a skill source:

```yaml
skill_sources:
  - github.com/bitop-dev/agent-platform-skills
  - github.com/your-org/custom-skills
```

## License

MIT
