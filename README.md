# agent-platform-skills

Community skill registry for [agent-core](https://github.com/bitop-dev/agent-core). Skills add capabilities to agents — web search, GitHub integration, document formatting, and more.

## Quick Start

```bash
# Install a skill
agent-core skill install github.com/bitop-dev/agent-platform-skills/web_search

# Use in an agent config
skills:
  - web_search
  - github

# Or install by cloning the whole registry
git clone https://github.com/bitop-dev/agent-platform-skills.git ~/.agent-core/skills
```

## Available Skills

| Skill | Description | Dependencies | Tier |
|---|---|---|---|
| [web_search](./skills/web_search/) | Search the web via DuckDuckGo (pluggable backend) | `python3`, `duckduckgo-search` | community |
| [web_fetch](./skills/web_fetch/) | Fetch a URL, extract readable content as markdown | `python3`, `beautifulsoup4` | community |
| [github](./skills/github/) | GitHub issues, PRs, CI via `gh` CLI | `gh` | community |
| [summarize](./skills/summarize/) | Summarize long text (instruction-only, no tools) | none | community |
| [report](./skills/report/) | Structure output as formatted markdown reports | none | community |

## Architecture

This is a **git-native registry** (like Homebrew). No hosted service — `agent-core` clones/pulls skills directly from this repo.

```
agent-platform-skills/
├── registry.json          ← Index of all skills (name, version, path)
├── skills/
│   ├── web_search/
│   │   ├── SKILL.md       ← Frontmatter + agent instructions
│   │   ├── tools/         ← Tool schemas (.json) + implementations (.py/.sh)
│   │   └── tests/         ← Test fixtures
│   ├── github/
│   ├── web_fetch/
│   ├── summarize/
│   └── report/
├── CONTRIBUTING.md
└── LICENSE
```

### How Skills Work

1. **SKILL.md** — Metadata (name, version, tags) in YAML frontmatter + markdown instructions injected into the agent's system prompt
2. **Tool schemas** (`tools/*.json`) — JSON schemas registered as available tools for the LLM
3. **Tool implementations** (`tools/*.py` or `tools/*.sh`) — Subprocess executables that read JSON from stdin and write JSON to stdout
4. **Instruction-only skills** (like `summarize`, `report`) — No tools, just instructions that shape agent behavior

### Skill Types

- **Tool skills**: Include executable tools the agent can call (web_search, github)
- **Instruction skills**: Teach the agent techniques through system prompt injection (summarize, report)
- **Hybrid skills**: Both tools and behavioral instructions

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md) for the full guide. Quick version:

1. Fork this repo
2. Create `skills/your_skill/SKILL.md` with frontmatter + instructions
3. Add tool schemas and implementations in `skills/your_skill/tools/`
4. Add test fixtures in `skills/your_skill/tests/`
5. Submit a PR

## License

MIT
