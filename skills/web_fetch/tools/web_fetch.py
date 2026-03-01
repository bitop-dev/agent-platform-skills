#!/usr/bin/env python3
"""
web_fetch tool — Fetch a URL and extract readable content as markdown.

Subprocess protocol:
  stdin:  JSON with arguments.url, arguments.max_chars, config.max_chars
  stdout: JSON with content (markdown text) and is_error flag

Dependencies: beautifulsoup4 (pip install beautifulsoup4)
"""

import json
import sys
import urllib.request
import urllib.error
import re


def html_to_markdown(html: str, include_links: bool = True) -> str:
    """Convert HTML to readable markdown. Uses BeautifulSoup if available, falls back to regex."""
    try:
        from bs4 import BeautifulSoup

        soup = BeautifulSoup(html, "html.parser")

        # Remove non-content elements
        for tag in soup(["script", "style", "nav", "footer", "header", "aside",
                         "noscript", "iframe", "svg", "form"]):
            tag.decompose()

        # Try to find main content area
        main = (
            soup.find("main")
            or soup.find("article")
            or soup.find(attrs={"role": "main"})
            or soup.find(id=re.compile(r"content|main|article", re.I))
            or soup.find(class_=re.compile(r"content|main|article|post", re.I))
            or soup.body
            or soup
        )

        lines = []
        for el in main.descendants:
            if el.name in ("h1", "h2", "h3", "h4", "h5", "h6"):
                level = int(el.name[1])
                text = el.get_text(strip=True)
                if text:
                    lines.append(f"\n{'#' * level} {text}\n")
            elif el.name == "p":
                text = el.get_text(strip=True)
                if text:
                    lines.append(f"\n{text}\n")
            elif el.name == "li":
                text = el.get_text(strip=True)
                if text:
                    lines.append(f"- {text}")
            elif el.name == "a" and include_links:
                href = el.get("href", "")
                text = el.get_text(strip=True)
                if text and href and href.startswith("http"):
                    lines.append(f"[{text}]({href})")
            elif el.name == "pre" or el.name == "code":
                text = el.get_text()
                if text.strip():
                    lines.append(f"\n```\n{text.strip()}\n```\n")

        text = "\n".join(lines)
    except ImportError:
        # Fallback: regex-based extraction
        text = re.sub(r"<script[^>]*>.*?</script>", "", html, flags=re.DOTALL | re.I)
        text = re.sub(r"<style[^>]*>.*?</style>", "", text, flags=re.DOTALL | re.I)
        text = re.sub(r"<[^>]+>", " ", text)
        text = re.sub(r"\s+", " ", text).strip()

    # Clean up whitespace
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def main():
    try:
        inp = json.load(sys.stdin)
    except json.JSONDecodeError as e:
        print(json.dumps({"content": f"Invalid input JSON: {e}", "is_error": True}))
        return

    args = inp.get("arguments", {})
    config = inp.get("config", {})

    url = args.get("url", "").strip()
    if not url:
        print(json.dumps({"content": "Error: url is required", "is_error": True}))
        return

    if not url.startswith(("http://", "https://")):
        print(json.dumps({"content": f"Error: invalid URL scheme. Must start with http:// or https://", "is_error": True}))
        return

    max_chars = args.get("max_chars") or config.get("max_chars", 20000)
    max_chars = int(max_chars)
    include_links = config.get("include_links", True)

    try:
        req = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0 (compatible; agent-core/1.0; +https://github.com/bitop-dev/agent-core)",
            "Accept": "text/html,application/xhtml+xml,*/*",
        })
        with urllib.request.urlopen(req, timeout=30) as resp:
            content_type = resp.headers.get("Content-Type", "")
            if "html" not in content_type and "text" not in content_type:
                print(json.dumps({
                    "content": f"Error: URL returned non-HTML content type: {content_type}",
                    "is_error": True,
                }))
                return

            html = resp.read().decode("utf-8", errors="replace")

        markdown = html_to_markdown(html, include_links=include_links)

        if len(markdown) > max_chars:
            markdown = markdown[:max_chars] + f"\n\n[Truncated at {max_chars} characters]"

        if not markdown.strip():
            print(json.dumps({"content": "Page returned no readable content.", "is_error": False}))
        else:
            print(json.dumps({"content": markdown, "is_error": False}))

    except urllib.error.HTTPError as e:
        print(json.dumps({"content": f"HTTP error {e.code}: {e.reason}", "is_error": True}))
    except urllib.error.URLError as e:
        print(json.dumps({"content": f"URL error: {e.reason}", "is_error": True}))
    except Exception as e:
        print(json.dumps({"content": f"Fetch error: {e}", "is_error": True}))


if __name__ == "__main__":
    main()
