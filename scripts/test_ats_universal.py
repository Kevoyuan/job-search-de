#!/usr/bin/env python3
"""Automated tests for job-search-de universal ATS parsing & worker pool download."""

import json
import os
import shutil
import subprocess
import sys
import tempfile

SKILL_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PARSE_ATS_SCRIPT = os.path.join(SKILL_ROOT, "scripts", "parse_ats.py")
DOWNLOAD_SCRIPT = os.path.join(SKILL_ROOT, "scripts", "download.sh")


def test_non_ai_parsing():
    """Test that parse_ats.py works for non-AI professions (e.g. Product Management) and doesn't drop them."""
    tmpdir = tempfile.mkdtemp(prefix="job_test_")
    try:
        config_dir = os.path.join(tmpdir, ".job-search")
        os.makedirs(config_dir, exist_ok=True)
        raw_dir = os.path.join(tmpdir, "ats_raw")
        os.makedirs(raw_dir, exist_ok=True)

        # 1. Write non-AI keywords
        kw_content = """# Custom Product Management Keywords
STRONG: product manager, technical product manager, lead product manager
WEAK: product, pm, roadmap
EXCLUDE_TITLES: intern, internship, werkstudent
ROLE_FAMILY_PRODUCT_OPS: technical product manager, product operations
ROLE_FAMILY_CORE_PRODUCT: product manager, lead product manager
"""
        with open(os.path.join(config_dir, "keywords.txt"), "w") as f:
            f.write(kw_content)

        # 2. Write settings.ini with priority location
        settings_content = """[search]
country_query = germany
fresh_days = 30

[locations]
priority_1 = berlin, munich, remote
"""
        with open(os.path.join(config_dir, "settings.ini"), "w") as f:
            f.write(settings_content)

        # 3. Create mock greenhouse payload with a pure Product Manager role (NO AI words whatsoever)
        gh_payload = {
            "jobs": [
                {
                    "title": "Senior Technical Product Manager",
                    "company_name": "SaaS Corp",
                    "location": {"name": "Berlin, Germany"},
                    "content": "Lead customer discovery, sprint planning, backlog grooming, and product metrics.",
                    "updated_at": "2026-08-25T10:00:00Z",
                    "absolute_url": "https://boards.greenhouse.io/saascorp/jobs/101"
                },
                {
                    # Weak title match: "Associate PM" has "pm" (WEAK), description has "product manager" (STRONG)
                    "title": "Associate PM",
                    "company_name": "Fintech AG",
                    "location": {"name": "Remote Germany"},
                    "content": "Collaborate with product manager on user research and analytics.",
                    "updated_at": "2026-08-26T10:00:00Z",
                    "absolute_url": "https://boards.greenhouse.io/fintech/jobs/102"
                },
                {
                    # Unrelated title and description
                    "title": "Office Administrator",
                    "company_name": "OldCorp",
                    "location": {"name": "Berlin"},
                    "content": "Manage office supplies and events.",
                    "updated_at": "2026-08-20T10:00:00Z",
                    "absolute_url": "https://boards.greenhouse.io/oldcorp/jobs/103"
                }
            ]
        }
        with open(os.path.join(raw_dir, "gh_saascorp.json"), "w") as f:
            json.dump(gh_payload, f)

        # 4. Run parse_ats.py
        cmd = [
            sys.executable, PARSE_ATS_SCRIPT,
            "--today", "2026-09-01",
            "--workdir", tmpdir,
            "--config-dir", config_dir
        ]
        res = subprocess.run(cmd, capture_output=True, text=True)
        assert res.returncode == 0, f"parse_ats.py failed:\n{res.stderr}"

        # 5. Verify output ats_results.json
        out_file = os.path.join(tmpdir, "ats_results.json")
        assert os.path.exists(out_file), "ats_results.json was not generated"

        with open(out_file) as f:
            jobs = json.load(f)

        assert len(jobs) == 2, f"Expected 2 product jobs, got {len(jobs)}"
        titles = [j["title"] for j in jobs]
        assert "Senior Technical Product Manager" in titles
        assert "Associate PM" in titles
        assert "Office Administrator" not in titles

        # Verify roleType was inferred from custom family, not hardcoded applied_ai
        pm_job = next(j for j in jobs if j["title"] == "Senior Technical Product Manager")
        assert pm_job["roleType"] == "product_ops", f"Expected 'product_ops', got '{pm_job['roleType']}'"

        assoc_pm = next(j for j in jobs if j["title"] == "Associate PM")
        assert assoc_pm["roleType"] in ["core_product", "product_ops", "general_match"], f"Unexpected roleType: {assoc_pm['roleType']}"

        print("✅ test_non_ai_parsing PASSED: Non-AI roles are retained with custom role families.")
    finally:
        shutil.rmtree(tmpdir)


def test_ai_backward_compatibility():
    """Test that default configs still parse AI/ML roles properly."""
    tmpdir = tempfile.mkdtemp(prefix="job_test_ai_")
    try:
        raw_dir = os.path.join(tmpdir, "ats_raw")
        os.makedirs(raw_dir, exist_ok=True)

        gh_payload = {
            "jobs": [
                {
                    "title": "Senior AI Agent Engineer",
                    "company_name": "AI Lab",
                    "location": {"name": "Frankfurt am Main"},
                    "content": "Building multi-agent LLM systems and RAG pipelines.",
                    "updated_at": "2026-08-25T10:00:00Z",
                    "absolute_url": "https://boards.greenhouse.io/ailab/jobs/201"
                }
            ]
        }
        with open(os.path.join(raw_dir, "gh_ailab.json"), "w") as f:
            json.dump(gh_payload, f)

        cmd = [
            sys.executable, PARSE_ATS_SCRIPT,
            "--today", "2026-09-01",
            "--workdir", tmpdir
        ]
        res = subprocess.run(cmd, capture_output=True, text=True)
        assert res.returncode == 0, f"parse_ats.py failed:\n{res.stderr}"

        with open(os.path.join(tmpdir, "ats_results.json")) as f:
            jobs = json.load(f)

        assert len(jobs) == 1
        assert jobs[0]["title"] == "Senior AI Agent Engineer"
        assert jobs[0]["roleType"] in ["ai_ml", "agentic_ai_engineering"]
        print("✅ test_ai_backward_compatibility PASSED: Default AI roles maintain expected classifications.")
    finally:
        shutil.rmtree(tmpdir)


def test_download_script_syntax_and_worker_pool():
    """Test download.sh syntax and worker pool execution."""
    tmpdir = tempfile.mkdtemp(prefix="job_download_")
    try:
        config_dir = os.path.join(tmpdir, ".job-search")
        os.makedirs(config_dir, exist_ok=True)

        # Empty boards file so it does not make real external network calls
        with open(os.path.join(config_dir, "boards.txt"), "w") as f:
            f.write("# empty boards for dry test\n")

        with open(os.path.join(config_dir, "keywords.txt"), "w") as f:
            f.write("STRONG: Marketing Lead, Growth Manager\n")

        cmd = [
            "/bin/bash", DOWNLOAD_SCRIPT,
            "--workdir", tmpdir,
            "--config-dir", config_dir
        ]
        env = os.environ.copy()
        env["GSTACK_DOWNLOAD_CONCURRENCY"] = "4"
        res = subprocess.run(cmd, env=env, capture_output=True, text=True)

        assert res.returncode == 0, f"download.sh failed with code {res.returncode}:\n{res.stderr}"
        assert "ALL_DONE" in res.stdout
        assert "concurrency=4" in res.stdout
        print("✅ test_download_script_syntax_and_worker_pool PASSED: Concurrency pool & dynamic keywords execute cleanly.")
    finally:
        shutil.rmtree(tmpdir)


def test_jsonld_verification():
    """Test verify_urls.py with local HTTP server serving multiline and @graph JSON-LD."""
    import http.server
    import threading

    tmpdir = tempfile.mkdtemp(prefix="job_verify_")
    try:
        # 1. Prepare HTML test files
        page1 = """<!DOCTYPE html>
<html>
<head>
  <title>Senior Frontend Engineer - Acme Inc</title>
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "JobPosting",
    "title": "Senior Frontend Engineer",
    "datePosted": "2026-08-15T09:00:00Z",
    "validThrough": "2026-10-01"
  }
  </script>
</head>
<body><h1>Job Page 1</h1></body>
</html>"""
        with open(os.path.join(tmpdir, "page1.html"), "w") as f:
            f.write(page1)

        page2 = """<!DOCTYPE html>
<html>
<head>
  <title>DevOps Specialist</title>
  <script type="application/ld+json">
  {
    "@graph": [
      {
        "@type": "Organization",
        "name": "Cloud AG"
      },
      {
        "@type": "JobPosting",
        "title": "DevOps Specialist",
        "datePosted": "\\n  2026-08-20  \\n"
      }
    ]
  }
  </script>
</head>
<body><h1>Job Page 2</h1></body>
</html>"""
        with open(os.path.join(tmpdir, "page2.html"), "w") as f:
            f.write(page2)

        # 2. Start local HTTP server on an ephemeral port
        class QuietHandler(http.server.SimpleHTTPRequestHandler):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, directory=tmpdir, **kwargs)
            def log_message(self, format, *args):
                pass

        server = http.server.HTTPServer(("127.0.0.1", 0), QuietHandler)
        port = server.server_address[1]
        server_thread = threading.Thread(target=server.serve_forever)
        server_thread.daemon = True
        server_thread.start()

        # 3. Create urls.txt
        urls_file = os.path.join(tmpdir, "urls.txt")
        with open(urls_file, "w") as f:
            f.write(f"http://127.0.0.1:{port}/page1.html\n")
            f.write(f"http://127.0.0.1:{port}/page2.html\n")

        # 4. Run verify_urls.py
        verify_script = os.path.join(SKILL_ROOT, "scripts", "verify_urls.py")
        res = subprocess.run([sys.executable, verify_script, urls_file], capture_output=True, text=True)
        assert res.returncode == 0, f"verify_urls.py failed:\n{res.stderr}"

        output = res.stdout
        assert "[200]" in output
        assert '"datePosted": "2026-08-15"' in output
        assert '"validThrough": "2026-10-01"' in output
        assert '"datePosted": "2026-08-20"' in output
        assert "Senior Frontend Engineer" in output
        assert "DevOps Specialist" in output

        # 5. Also verify scripts/verify.sh wrapper
        sh_script = os.path.join(SKILL_ROOT, "scripts", "verify.sh")
        sh_res = subprocess.run(["/bin/bash", sh_script, urls_file], capture_output=True, text=True)
        assert sh_res.returncode == 0, f"verify.sh wrapper failed:\n{sh_res.stderr}"
        assert "[200]" in sh_res.stdout
        assert '"datePosted": "2026-08-15"' in sh_res.stdout

        server.shutdown()
        print("✅ test_jsonld_verification PASSED: Multiline JSON-LD, @graph, and verify.sh wrapper succeed.")
    finally:
        shutil.rmtree(tmpdir)


def test_bump_version_decoupled():
    """Test bump_version.py sync runs cleanly without personal path errors."""
    bump_script = os.path.join(SKILL_ROOT, "scripts", "bump_version.py")
    res = subprocess.run([sys.executable, bump_script, "sync"], capture_output=True, text=True)
    assert res.returncode == 0, f"bump_version.py sync failed:\n{res.stderr}"
    assert "Synced version" in res.stdout
    print("✅ test_bump_version_decoupled PASSED: Version sync runs cleanly with decoupled paths.")


if __name__ == "__main__":
    print("🚀 Running job-search-de comprehensive verification tests...\n")
    test_non_ai_parsing()
    test_ai_backward_compatibility()
    test_download_script_syntax_and_worker_pool()
    test_jsonld_verification()
    test_bump_version_decoupled()
    print("\n🎉 ALL TESTS PASSED SUCCESSFULLY!")
