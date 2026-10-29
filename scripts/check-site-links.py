#!/usr/bin/env python3
import argparse
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit


class Page(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.ids = set()
        self.links = []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.add(attrs["id"])
        if tag == "a" and attrs.get("name"):
            self.ids.add(attrs["name"])
        if tag in ("a", "area", "link") and attrs.get("href"):
            self.links.append(attrs["href"])
        if tag in ("img", "script", "iframe", "audio", "video", "source"):
            if attrs.get("src"):
                self.links.append(attrs["src"])
        if tag == "video" and attrs.get("poster"):
            self.links.append(attrs["poster"])


def check_site(output, base_url):
    base_url = base_url.rstrip("/") + "/"
    site = urlsplit(base_url)
    prefix = unquote(site.path).rstrip("/")
    pages = {
        path.relative_to(output).as_posix(): Page(path.read_text(encoding="utf-8"))
        for path in output.rglob("*.html")
    }
    if not pages:
        return [(str(output), "", "no generated HTML files")]

    errors = set()
    for source, page in pages.items():
        for href in page.links:
            raw = urlsplit(href)
            if raw.scheme and raw.scheme not in ("http", "https"):
                continue
            target = urlsplit(urljoin(base_url + source, href))
            if target.netloc != site.netloc:
                continue
            path = unquote(target.path)
            if path != prefix and not path.startswith(prefix + "/"):
                if not raw.scheme and not raw.netloc:
                    errors.add((source, href, "link escapes the site base path"))
                continue
            relative = path[len(prefix):].lstrip("/")
            candidates = [relative]
            if not relative.endswith("/"):
                candidates.append(relative + ".html")
            candidates.append(relative.rstrip("/") + "/index.html" if relative else "index.html")
            destination = next(
                (name for name in candidates if (output / name).is_file()), None
            )
            if destination is None:
                errors.add((source, href, "target file not found"))
            elif target.fragment and destination in pages:
                if unquote(target.fragment) not in pages[destination].ids:
                    errors.add((source, href, "anchor not found"))
    return sorted(errors)


def main():
    parser = argparse.ArgumentParser(description="Check local links and anchors in a Quartz build")
    parser.add_argument("output", nargs="?", default="public", type=Path)
    parser.add_argument("--base-url")
    args = parser.parse_args()
    base_url = args.base_url
    if base_url is None:
        config = Path(__file__).resolve().parents[1] / "quartz.config.ts"
        match = re.search(r'\bbaseUrl:\s*["\x27]([^"\x27]+)["\x27]', config.read_text())
        if not match:
            parser.error("pass --base-url when baseUrl is not a literal string in quartz.config.ts")
        base_url = "https://" + match[1]
    errors = check_site(args.output, base_url)
    for source, href, reason in errors:
        print(f"BROKEN  {source}  ->  {href}  ({reason})")
    if errors:
        print(f"\n{len(errors)} broken generated link(s)")
        return 1
    print("OK: no broken local links or anchors in generated HTML")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
