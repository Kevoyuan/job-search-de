#!/usr/bin/env python3
"""Build an interactive, modern Job Hunt Workbench HTML with local candidate config editing support."""

import argparse
import json
import math
import sys
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

try:
    from check_update import REMOTE_VERSION_URL, check_update as run_update_check
except Exception:  # pragma: no cover - degrade to "no update info" when unavailable
    run_update_check = None
    REMOTE_VERSION_URL = "https://raw.githubusercontent.com/Kevoyuan/job-search-de/main/VERSION"

FALLBACK_UPDATE_META = {
    "repo": "https://github.com/Kevoyuan/job-search-de",
    "slashCommand": "/update-skill",
    "command": "npx skills update job-search-de -g",
}


def load_file_content(path: Path) -> str:
    if path.exists():
        try:
            return path.read_text(encoding="utf-8")
        except Exception:
            return ""
    return ""


def safe_json_for_script(data) -> str:
    """Serialize JSON safely for embedding inside an HTML <script> block."""
    raw = json.dumps(data, ensure_ascii=False)
    return raw.replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")


def normalize_job(job):
    """Adapt legacy report rows without modifying their stored evidence or IDs.

    Canonical fields win when present (including an explicit null score).
    Missing/invalid scores stay unknown; this adapter never calculates fit.
    """
    result = dict(job)
    aliases = {
        "score": "fit", "company": "co", "location": "loc",
        "workModel": "mode", "datePosted": "date", "salary": "sal",
    }
    for canonical, legacy in aliases.items():
        if canonical not in result and legacy in job:
            result[canonical] = job[legacy]
    score = result.get("score")
    if isinstance(score, bool) or not isinstance(score, (int, float, str)):
        score = None
    else:
        try:
            score = float(score)
            if not math.isfinite(score) or not 0 <= score <= 100:
                score = None
            elif score.is_integer():
                score = int(score)
        except ValueError:
            score = None
    result["score"] = score
    return result


def main():
    parser = argparse.ArgumentParser(description="Generate job-hunt-workbench.html")
    parser.add_argument("--workdir", default=".", help="Working directory containing .job-search and job files")
    parser.add_argument("--jobs-file", default=None, help="Path to verified_jobs.json")
    parser.add_argument("--output", default=None, help="Output HTML file path (default: <workdir>/job-hunt-workbench.html)")
    parser.add_argument("--lang", default="en", choices=["zh", "en", "de"], help="Workbench UI language")
    parser.add_argument("--no-update-check", action="store_true",
                        help="Skip the GitHub version lookup and bake in the local version only")
    parser.add_argument("--update-timeout", type=float, default=2.0,
                        help="Version lookup timeout in seconds (default: 2.0)")
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

    jobs_data = [normalize_job(job) for job in jobs_data]

    # 3. Read Version and resolve the remote release (best-effort, never blocking)
    version_file = SKILL_ROOT / "VERSION"
    current_version = version_file.read_text().strip() if version_file.exists() else "1.1.1"

    update_meta = dict(FALLBACK_UPDATE_META)
    update_meta.update({
        "current": current_version,
        "remote": current_version,
        "updateAvailable": False,
        "checked": False,
    })
    if run_update_check is not None and not args.no_update_check:
        try:
            detected = run_update_check(timeout=args.update_timeout)
            update_meta.update(detected)
        except Exception as exc:  # pragma: no cover - network failures must not break builds
            print(f"⚠️ Warning: version check skipped ({exc})", file=sys.stderr)

    # 4. Read Template
    template_file = SKILL_ROOT / "templates" / "workbench_template.html"
    if not template_file.exists():
        print(f"❌ Error: Template not found at {template_file}", file=sys.stderr)
        sys.exit(1)

    template_html = template_file.read_text(encoding="utf-8")

    # 4b. Inject the optional theme refresh pack (scoped to the non-default themes).
    theme_refresh_file = SKILL_ROOT / "templates" / "theme-refresh.css"
    if theme_refresh_file.exists():
        theme_css = theme_refresh_file.read_text(encoding="utf-8")
        template_html = template_html.replace(
            "</style>",
            "/* theme refresh pack */\n" + theme_css + "\n</style>",
            1,
        )

    # 5. Inject Values
    title_map = {
        "zh": "德国岗位求职工作台",
        "en": "Germany Job Hunt Workbench",
        "de": "Deutschland Job-Suche Workbench"
    }
    title = title_map.get(args.lang, title_map["zh"])

    rendered_html = template_html.replace("__TITLE__", title)
    rendered_html = rendered_html.replace("__LANG__", args.lang)
    rendered_html = rendered_html.replace("__CURRENT_VERSION__", update_meta["current"])
    rendered_html = rendered_html.replace("__LATEST_VERSION__", update_meta["remote"])
    rendered_html = rendered_html.replace("__UPDATE_AVAILABLE__", "true" if update_meta["updateAvailable"] else "false")
    rendered_html = rendered_html.replace("__UPDATE_CHECKED__", "true" if update_meta["checked"] else "false")
    rendered_html = rendered_html.replace("__UPDATE_COMMAND__", safe_json_for_script(update_meta["command"]))
    rendered_html = rendered_html.replace("__SLASH_COMMAND__", safe_json_for_script(update_meta["slashCommand"]))
    rendered_html = rendered_html.replace("__REPO_URL__", safe_json_for_script(update_meta["repo"]))
    rendered_html = rendered_html.replace("__REPO_URL_RAW__", update_meta["repo"])
    rendered_html = rendered_html.replace("__VERSION_CHECK_URL__", safe_json_for_script(REMOTE_VERSION_URL))
    rendered_html = rendered_html.replace("__EMBEDDED_CONFIG_JSON__", safe_json_for_script(embedded_config))
    rendered_html = rendered_html.replace("__JOBS_JSON__", safe_json_for_script(jobs_data))

    # 6. Save Output
    output_path = Path(args.output).resolve() if args.output else (workdir / "job-hunt-workbench.html")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(rendered_html, encoding="utf-8")

    if update_meta["updateAvailable"]:
        status = f"update available → v{update_meta['remote']}"
    elif update_meta["checked"]:
        status = f"up to date (v{update_meta['current']})"
    else:
        status = f"update check skipped (v{update_meta['current']})"

    print(f"✨ Generated Workbench HTML: {output_path} ({len(jobs_data)} jobs loaded)")
    print(f"   ↳ skill version: {status}")


if __name__ == "__main__":
    main()
