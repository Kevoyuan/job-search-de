#!/bin/bash
# Auto-update job-search-de skill to latest version from GitHub

set -e

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "🔄 Checking for updates for job-search-de in $SKILL_DIR..."

if [ -d "$SKILL_DIR/.git" ]; then
    echo "📦 Pulling latest changes from git remote..."
    git -C "$SKILL_DIR" pull --ff-only origin main || {
        echo "⚠️ Git fast-forward pull failed. Fetching and resetting to origin/main..."
        git -C "$SKILL_DIR" fetch origin main
        git -C "$SKILL_DIR" reset --hard origin/main
    }
fi

if command -v npx &>/dev/null; then
    echo "✨ Running npx skills update check..."
    npx skills update job-search-de -g -y 2>/dev/null || true
fi

# Automatically sync/rebuild active workbench HTML files so the user's workspace is upgraded instantly
echo "🔨 Synchronizing active workbench HTML files..."
python3 "$SKILL_DIR/scripts/bump_version.py" sync 2>/dev/null || true

echo "✅ job-search-de is fully updated to $(cat "$SKILL_DIR/VERSION" 2>/dev/null || echo 'latest')!"
