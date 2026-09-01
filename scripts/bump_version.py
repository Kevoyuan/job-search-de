#!/usr/bin/env python3
"""Automatically bump semantic version and synchronize across all repository files."""

import sys
import re
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parent.parent
VERSION_FILE = SKILL_ROOT / "VERSION"
WORKBENCH_FILE = SKILL_ROOT / "job-hunt-workbench.html"
CWD_WORKBENCH = Path.cwd() / "job-hunt-workbench.html"
ACTIVE_WORKBENCH = Path("job-hunt-workbench.html")


def get_current_version() -> str:
    if VERSION_FILE.exists():
        return VERSION_FILE.read_text().strip()
    return "1.0.0"


def bump(part: str = "patch") -> str:
    curr = get_current_version()
    parts = curr.split(".")
    while len(parts) < 3:
        parts.append("0")

    major, minor, patch = int(parts[0]), int(parts[1]), int(parts[2])

    if part == "major":
        major += 1
        minor = 0
        patch = 0
    elif part == "minor":
        minor += 1
        patch = 0
    else:  # patch
        patch += 1

    new_ver = f"{major}.{minor}.{patch}"

    # 1. Update VERSION file
    VERSION_FILE.write_text(new_ver + "\n")
    print(f"📦 Bumped version: v{curr} ➔ v{new_ver}")

    # 2. Update workbench files if they exist
    for wb in set([WORKBENCH_FILE, CWD_WORKBENCH, ACTIVE_WORKBENCH]):
        if wb.exists():
            content = wb.read_text(encoding="utf-8")
            # Replace <span id="versionText">vX.X.X</span>
            content = re.sub(
                r'(<span id="versionText">)v?[0-9\.]+(</span>)',
                rf'\g<1>v{new_ver}\g<2>',
                content
            )
            # Replace const CURRENT_SKILL_VERSION = "X.X.X"; or fallback version string
            content = re.sub(
                r'(CURRENT_SKILL_VERSION\s*=\s*(?:\([^)]*\)\s*\?\s*[^:]+:\s*)?[\'"])[0-9\.]+([\'"])',
                rf'\g<1>{new_ver}\g<2>',
                content
            )
            wb.write_text(content, encoding="utf-8")
            print(f"  ✓ Synced version to {wb.name}")

    return new_ver


def sync_version():
    curr = get_current_version()
    for wb in set([WORKBENCH_FILE, CWD_WORKBENCH, ACTIVE_WORKBENCH]):
        if wb.exists():
            content = wb.read_text(encoding="utf-8")
            content = re.sub(
                r'(<span id="versionText">)v?[0-9\.]+(</span>)',
                rf'\g<1>v{curr}\g<2>',
                content
            )
            content = re.sub(
                r'(CURRENT_SKILL_VERSION\s*=\s*(?:\([^)]*\)\s*\?\s*[^:]+:\s*)?[\'"])[0-9\.]+([\'"])',
                rf'\g<1>{curr}\g<2>',
                content
            )
            wb.write_text(content, encoding="utf-8")
            print(f"  ✓ Synced version v{curr} to {wb.name}")


if __name__ == "__main__":
    part_to_bump = sys.argv[1] if len(sys.argv) > 1 else "patch"
    if part_to_bump == "sync":
        sync_version()
    else:
        bump(part_to_bump)
