#!/usr/bin/env python3
"""Check for job-search-de updates from GitHub.

Reusable from other scripts (``build_workbench.py`` imports ``check_update``)
and runnable as a CLI:

    python3 scripts/check_update.py            # human-readable reminder
    python3 scripts/check_update.py --json     # machine-readable payload
    python3 scripts/check_update.py --offline  # never touch the network
"""

import argparse
import json
import re
import sys
import urllib.request
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parent.parent
VERSION_FILE = SKILL_ROOT / "VERSION"

REPO = "Kevoyuan/job-search-de"
REPO_URL = f"https://github.com/{REPO}"
REMOTE_VERSION_URL = f"https://raw.githubusercontent.com/{REPO}/main/VERSION"
SLASH_COMMAND = "/update-skill"
UPDATE_COMMAND = "npx skills update job-search-de -g"

DEFAULT_TIMEOUT = 3.0

_VERSION_RE = re.compile(r"^\s*v?(\d+)\.(\d+)\.(\d+)")


def get_current_version() -> str:
    """Read the locally installed version, never raising."""
    try:
        if VERSION_FILE.exists():
            return VERSION_FILE.read_text(encoding="utf-8").strip()
    except Exception:
        pass
    return "0.0.0"


def parse_version(value):
    """Parse ``v1.2.3`` (or ``1.2.3``) into a comparable tuple, else ``None``."""
    if not isinstance(value, str):
        return None
    match = _VERSION_RE.match(value)
    if not match:
        return None
    return tuple(int(part) for part in match.groups())


def is_newer(remote: str, current: str) -> bool:
    """True only when ``remote`` is a strictly greater semantic version."""
    remote_parts = parse_version(remote)
    current_parts = parse_version(current)
    if remote_parts is None or current_parts is None:
        return False
    return remote_parts > current_parts


def fetch_remote_version(timeout: float = DEFAULT_TIMEOUT):
    """Return the published version string, or ``None`` when unreachable."""
    try:
        request = urllib.request.Request(
            REMOTE_VERSION_URL,
            headers={"User-Agent": "job-search-de-cli", "Cache-Control": "no-cache"},
        )
        with urllib.request.urlopen(request, timeout=timeout) as response:
            remote = response.read().decode("utf-8").strip()
            return remote or None
    except Exception:
        return None


def check_update(timeout: float = DEFAULT_TIMEOUT, offline: bool = False) -> dict:
    """Collect the full update state as a plain dict (safe to JSON-serialize)."""
    current = get_current_version()
    remote = None if offline else fetch_remote_version(timeout=timeout)
    return {
        "current": current,
        "remote": remote or current,
        "updateAvailable": bool(remote and is_newer(remote, current)),
        "checked": remote is not None,
        "repo": REPO_URL,
        "slashCommand": SLASH_COMMAND,
        "command": UPDATE_COMMAND,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Check for job-search-de updates from GitHub.")
    parser.add_argument("--json", action="store_true", help="Emit a machine-readable JSON payload")
    parser.add_argument("--timeout", type=float, default=DEFAULT_TIMEOUT, help="Network timeout in seconds")
    parser.add_argument("--offline", action="store_true", help="Skip the network check entirely")
    args = parser.parse_args()

    result = check_update(timeout=args.timeout, offline=args.offline)

    if args.json:
        print(json.dumps(result, ensure_ascii=False))
        return 0

    if result["updateAvailable"]:
        print(f"💡 job-search-de update available (v{result['remote']}). Type /update-skill to upgrade.")
        print(f"   Or run: {result['command']}")
    elif not result["checked"]:
        print(f"ℹ️ job-search-de v{result['current']} (update server unreachable; skipped)")
    else:
        print(f"✅ job-search-de is up to date (v{result['current']})")

    return 0


if __name__ == "__main__":
    sys.exit(main())
