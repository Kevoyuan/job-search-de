#!/usr/bin/env python3
"""Build an interactive, modern Job Hunt Workbench HTML with local candidate config editing support."""

import argparse
import json
import sys
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parent.parent


def load_file_content(path: Path) -> str:
    if path.exists():
        try:
            return path.read_text(encoding="utf-8")
        except Exception:
            return ""
    return ""


def main():
    parser = argparse.ArgumentParser(description="Generate job-hunt-workbench.html")
    parser.add_argument("--workdir", default=".", help="Working directory containing .job-search and job files")
    parser.add_argument("--jobs-file", default=None, help="Path to verified_jobs.json")
    parser.add_argument("--output", default=None, help="Output HTML file path (default: <workdir>/job-hunt-workbench.html)")
    parser.add_argument("--lang", default="zh", choices=["zh", "en", "de"], help="Workbench UI language")
    args = parser.parse_args()

    workdir = Path(args.workdir).resolve()
    config_dir = workdir / ".job-search"
    if not config_dir.exists():
        config_dir = SKILL_ROOT / "assets" / "config-template"

    # 1. Read Candidate Configs
    profile_content = load_file_content(config_dir / "profile.md")
    preferences_content = load_file_content(config_dir / "preferences.md")
    settings_content = load_file_content(config_dir / "settings.ini")

    embedded_config = {
        "profile": profile_content,
        "preferences": preferences_content,
        "settings": settings_content
    }

    # 2. Read Jobs Data
    jobs_file = Path(args.jobs_file).resolve() if args.jobs_file else (workdir / "verified_jobs.json")
    jobs_data = []
    if jobs_file.exists():
        try:
            with open(jobs_file, "r", encoding="utf-8") as f:
                loaded = json.load(f)
                if isinstance(loaded, list):
                    jobs_data = loaded
                elif isinstance(loaded, dict) and "jobs" in loaded:
                    jobs_data = loaded["jobs"]
        except Exception as e:
            print(f"⚠️ Warning: Failed to parse jobs from {jobs_file}: {e}", file=sys.stderr)

    # 3. Read Version
    version_file = SKILL_ROOT / "VERSION"
    current_version = version_file.read_text().strip() if version_file.exists() else "1.1.1"

    # 4. Read Template
    template_file = SKILL_ROOT / "templates" / "workbench_template.html"
    if not template_file.exists():
        print(f"❌ Error: Template not found at {template_file}", file=sys.stderr)
        sys.exit(1)

    template_html = template_file.read_text(encoding="utf-8")

    # 5. Inject Values
    title_map = {
        "zh": "德国岗位求职工作台",
        "en": "Germany Job Hunt Workbench",
        "de": "Deutschland Job-Suche Workbench"
    }
    title = title_map.get(args.lang, title_map["zh"])

    rendered_html = template_html.replace("__TITLE__", title)
    rendered_html = rendered_html.replace("__LANG__", args.lang)
    rendered_html = rendered_html.replace("__CURRENT_VERSION__", current_version)
    rendered_html = rendered_html.replace("__LATEST_VERSION__", current_version)
    rendered_html = rendered_html.replace("__EMBEDDED_CONFIG_JSON__", json.dumps(embedded_config, ensure_ascii=False))
    rendered_html = rendered_html.replace("__JOBS_JSON__", json.dumps(jobs_data, ensure_ascii=False))

    # 6. Save Output
    output_path = Path(args.output).resolve() if args.output else (workdir / "job-hunt-workbench.html")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(rendered_html, encoding="utf-8")

    print(f"✨ Generated Workbench HTML: {output_path} ({len(jobs_data)} jobs loaded)")


if __name__ == "__main__":
    main()
