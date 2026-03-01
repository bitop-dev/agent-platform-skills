---
name: slack_notify
version: 1.0.0
description: Post messages to Slack via incoming webhook
tier: community
tags: slack, notification, webhook, messaging
tools:
  - name: slack_notify
    description: Post a message to a Slack channel via webhook URL
    parameters: |
      {
        "type": "object",
        "properties": {
          "webhook_url": {
            "type": "string",
            "description": "Slack incoming webhook URL"
          },
          "text": {
            "type": "string",
            "description": "Message text (supports Slack mrkdwn)"
          },
          "channel": {
            "type": "string",
            "description": "Override channel (optional)"
          },
          "username": {
            "type": "string",
            "description": "Override bot username (optional)"
          }
        },
        "required": ["webhook_url", "text"]
      }
---

# Slack Notify

Send messages to Slack channels using incoming webhooks.

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
