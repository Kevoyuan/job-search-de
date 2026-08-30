#!/usr/bin/env python3
"""Check for job-search-de updates from GitHub."""

import sys
import urllib.request
from pathlib import Path

VERSION_FILE = Path(__file__).resolve().parent.parent / "VERSION"
CURRENT_VERSION = VERSION_FILE.read_text().strip() if VERSION_FILE.exists() else "1.1.0"
REMOTE_VERSION_URL = "https://raw.githubusercontent.com/Kevoyuan/job-search-de/main/VERSION"


def check_update():
    try:
        req = urllib.request.Request(
            REMOTE_VERSION_URL,
            headers={"User-Agent": "job-search-de-cli", "Cache-Control": "no-cache"}
        )
        with urllib.request.urlopen(req, timeout=3) as resp:
            remote = resp.read().decode("utf-8").strip()
            if remote and remote != CURRENT_VERSION:
                print(f"✨ [job-search-de] New version available: v{remote} (Current: v{CURRENT_VERSION})")
                print("👉 Update with: /update-skill  OR  npx skills update job-search-de -g\n")
                return True
    except Exception:
        pass
    return False


if __name__ == "__main__":
    check_update()
