---
name: web_search
version: 2.0.0
description: "Search the web for information. Use when: you need current facts, recent events, documentation, tutorials, or any knowledge you're unsure about. NOT for: questions you can confidently answer from training data, file contents already available locally, or GitHub/GitLab operations (use those skills instead)."
author: platform-team
tags: [web, search, research]
emoji: "🔍"
always: false
runtime: wasm

config:
  max_results:
    type: integer
    default: 10
    description: "Default max results when not specified by the agent"
---

# Web Search

Search the web via DuckDuckGo and return titles, URLs, and snippets for a query.

Runs as a sandboxed WebAssembly module — no Python, no pip, no external dependencies.
Network access is gated by the sandbox's AllowedHosts policy (`html.duckduckgo.com`).

## When to Use

✅ **USE this skill when:**
- You need current or recent information (news, events, releases)
- You're unsure about a fact and want to verify it
- The user asks about something outside your training data
- You need documentation, tutorials, or API references
- You need to find specific websites or resources

❌ **DON'T use this skill when:**
- You can confidently answer from your training knowledge
- The information is already available in local files (use `read_file`)
- The user is asking about their own codebase (use file tools)
- You need to interact with GitHub/GitLab (use those skills)
- You already have search results that answer the question

## How to Search Well

1. **Be specific** — "Go 1.22 error handling changes" beats "Go errors"
2. **Include key terms** — Use the most distinctive words from the user's question
3. **Don't over-search** — One good query is better than five vague ones
4. **Use time context** — If the user wants recent info, include the year in the query
5. **Read the snippets first** — Often the snippet answers the question without needing to fetch the full page
6. **Follow up selectively** — Only use `web_fetch` on results whose snippets look genuinely relevant

## Result Format

Results come back as a numbered list:

```
1. Title of the first result
   https://example.com/page
   Snippet text showing a preview of the page content...

2. Title of the second result
   https://another.com/article
   Another snippet with relevant information...
```

## Sandbox Requirements

- **Network**: `html.duckduckgo.com` must be in AllowedHosts
- **Filesystem**: none required
- **Dependencies**: none — single .wasm binary
