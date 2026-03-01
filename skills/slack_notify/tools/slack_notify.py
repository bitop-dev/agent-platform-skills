#!/usr/bin/env python3
"""Post a message to Slack via incoming webhook."""

import json
import sys
import urllib.request

def main():
    raw = json.load(sys.stdin)
    args = raw.get("args", raw)
    
    webhook_url = args.get("webhook_url", "")
    text = args.get("text", "")
    
    if not webhook_url:
        print(json.dumps({"error": "webhook_url is required"}))
        return
    if not text:
        print(json.dumps({"error": "text is required"}))
        return
    
    payload = {"text": text}
    if args.get("channel"):
        payload["channel"] = args["channel"]
    if args.get("username"):
        payload["username"] = args["username"]
    
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        webhook_url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            body = resp.read().decode("utf-8")
            print(json.dumps({"status": "sent", "response": body}))
    except Exception as e:
        print(json.dumps({"error": str(e)}))

if __name__ == "__main__":
    main()
