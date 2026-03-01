---
name: slack_notify
version: 2.0.0
description: "Post messages to Slack via incoming webhook. Use when the user asks to notify, alert, or send a message to a Slack channel."
author: platform-team
tags: [slack, notification, webhook, messaging]
emoji: "💬"
always: false
runtime: wasm
---

# Slack Notify

Send messages to Slack channels using incoming webhooks.

Runs as a sandboxed WebAssembly module — no Python, no curl, no external dependencies.
Uses the sandbox HTTP host function to POST to Slack's webhook URL.

## Usage

When the user asks you to notify, alert, or send a message to Slack:
1. Use the `slack_notify` tool with the webhook URL and message text
2. Format messages using Slack's mrkdwn syntax:
   - `*bold*`, `_italic_`, `~strikethrough~`
   - `>` for block quotes
   - `` `code` `` for inline code
   - Lists with `•` or `-`
3. Keep messages concise — Slack has a 40K character limit per message

## Best Practices

- Lead with the most important information
- Use emoji for status: ✅ success, ❌ failure, ⚠️ warning, ℹ️ info
- Include timestamps and links when relevant
- For reports, summarize key findings in 3-5 bullet points

## Sandbox Requirements

- **Network**: `hooks.slack.com` must be in AllowedHosts
- **Filesystem**: none required
- **Dependencies**: none — single .wasm binary
