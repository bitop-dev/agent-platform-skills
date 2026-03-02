---
name: email_send
version: 1.0.0
description: "Send emails via Resend API. Use when the user asks to email a report, notify someone, or send results."
author: platform-team
tags: [email, notification, resend]
emoji: "✉️"
always: false
runtime: wasm
requires: {}
---
# Email Send
Send emails via the Resend API. Supports plain text and markdown body (converted to HTML).

## Required Credentials
- `RESEND_API_KEY` — Resend API key (https://resend.com/api-keys)
