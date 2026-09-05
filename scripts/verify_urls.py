#!/usr/bin/env python3
"""Robust URL verification & Schema.org JSON-LD extractor for job-search-de.
Usage:
    python3 scripts/verify_urls.py urls.txt
    cat urls.txt | python3 scripts/verify_urls.py
"""

import json
import re
import sys
import urllib.error
import urllib.request
from html.parser import HTMLParser
from typing import Dict, List, Optional


class JSONLDParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title = ""
        self.in_title = False
        self.json_ld_blocks: List[str] = []
        self.in_json_ld = False
        self.meta_tags: Dict[str, str] = {}

    def handle_starttag(self, tag, attrs):
        attrs_dict = {k.lower(): v for k, v in attrs if v is not None}
        if tag == "title" and not self.title:
            self.in_title = True
        elif tag == "script" and attrs_dict.get("type") == "application/ld+json":
            self.in_json_ld = True
        elif tag == "meta":
            prop = attrs_dict.get("property") or attrs_dict.get("name")
            content = attrs_dict.get("content")
            if prop and content:
                self.meta_tags[prop.lower()] = content

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False
        elif tag == "script" and self.in_json_ld:
            self.in_json_ld = False

    def handle_data(self, data):
        if self.in_title:
            self.title += data
        elif self.in_json_ld:
            self.json_ld_blocks.append(data)


def clean_date(val: Optional[str]) -> Optional[str]:
    if not val or not isinstance(val, str):
        return None
    val = val.strip().replace("Z", "").replace("z", "")
    if "T" in val:
        val = val.split("T")[0]
    elif " " in val:
        val = val.split(" ")[0]
    m = re.match(r"(\d{4}-\d{2}-\d{2})", val)
    return m.group(1) if m else None


def extract_schema_fields(data) -> Dict[str, Optional[str]]:
    fields = {"datePosted": None, "datePublished": None, "validThrough": None, "title": None}

    def walk(node):
        if isinstance(node, dict):
            # Check for fields directly
            for k in ["datePosted", "datePublished", "validThrough"]:
                if k in node and not fields[k]:
                    fields[k] = clean_date(str(node[k]))
            if "title" in node and not fields["title"]:
                fields["title"] = str(node["title"]).strip()
            for v in node.values():
                walk(v)
        elif isinstance(node, list):
            for item in node:
                walk(item)

    walk(data)
    return fields


def verify_url(url: str, timeout: int = 15) -> str:
    url = url.strip()
    if not url or url.startswith("#"):
        return ""

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    }
    req = urllib.request.Request(url, headers=headers)

    http_code = 0
    html_content = ""
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            http_code = resp.getcode()
            charset = resp.headers.get_content_charset() or "utf-8"
            html_content = resp.read().decode(charset, errors="replace")
    except urllib.error.HTTPError as e:
        http_code = e.code
    except Exception as e:
        return f"[000] FAIL :: {type(e).__name__} :: {url}"

    parser = JSONLDParser()
    try:
        parser.feed(html_content)
    except Exception:
        pass

    title = parser.title.strip().replace("\n", " ").replace("\r", " ")
    title = re.sub(r"\s+", " ", title)[:60]
    if not title:
        title = parser.meta_tags.get("og:title", "")[:60]

    schema_info = {"datePosted": None, "datePublished": None, "validThrough": None}
    for block in parser.json_ld_blocks:
        try:
            parsed = json.loads(block)
            fields = extract_schema_fields(parsed)
            for k in schema_info:
                if not schema_info[k] and fields[k]:
                    schema_info[k] = fields[k]
        except Exception:
            continue

    # Fallback to meta tags if datePublished is missing
    if not schema_info["datePublished"]:
        pub = parser.meta_tags.get("article:published_time") or parser.meta_tags.get("publication_date")
        schema_info["datePublished"] = clean_date(pub)

    d_str = f'"datePosted": "{schema_info["datePosted"]}"' if schema_info["datePosted"] else ""
    d2_str = f'"datePublished": "{schema_info["datePublished"]}"' if schema_info["datePublished"] else ""
    vt_str = f'"validThrough": "{schema_info["validThrough"]}"' if schema_info["validThrough"] else ""

    dates_part = " ".join(filter(None, [d_str, d2_str, vt_str]))
    return f"[{http_code}] {dates_part} :: {title} :: {url}"


def main():
    lines = []
    if len(sys.argv) > 1 and sys.argv[1] != "-":
        with open(sys.argv[1], encoding="utf-8") as f:
            lines = f.readlines()
    else:
        lines = sys.stdin.readlines()

    for line in lines:
        u = line.strip()
        if not u or u.startswith("#"):
            continue
        result = verify_url(u)
        if result:
            print(result)


if __name__ == "__main__":
    main()
