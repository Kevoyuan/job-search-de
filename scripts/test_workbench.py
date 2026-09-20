#!/usr/bin/env python3
"""Regression tests for legacy job data and evidence-score preservation."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from build_workbench import normalize_job


class WorkbenchTests(unittest.TestCase):
    def test_legacy_mapping_preserves_evidence(self):
        row = dict(id="a67", fit=89, co="Mayflower", loc="Munich", mode="Hybrid",
                   date="2026-09-20", sal="Unknown", reason="Evidence", gap="Stretch")
        result = normalize_job(row)
        for key, value in row.items():
            self.assertEqual(result[key], value)
        self.assertEqual(result["score"], 89)
        for key, old in dict(company="co", location="loc", workModel="mode", datePosted="date", salary="sal").items():
            self.assertEqual(result[key], row[old])
        self.assertNotIn("score", row)
        self.assertNotIn("freshness", result)

    def test_canonical_fields_win(self):
        result = normalize_job(dict(score=0, fit=94, company="New", co="Old"))
        self.assertEqual(result["score"], 0)
        self.assertEqual(result["company"], "New")
        self.assertIsNone(normalize_job(dict(score=None, fit=94))["score"])

    def test_unknown_and_invalid_scores(self):
        for value in [None, "", "unknown", True, False, -1, 101, "NaN", "Infinity", [], {}]:
            with self.subTest(value=value):
                self.assertIsNone(normalize_job(dict(fit=value))["score"])
        self.assertIsNone(normalize_job({})["score"])
        self.assertEqual(normalize_job(dict(fit="89.5"))["score"], 89.5)

    def test_generator_accepts_both_containers_without_mutating_source(self):
        script = Path(__file__).with_name("build_workbench.py")
        rows = [dict(id="a67", fit=89, co="Mayflower"), dict(id="unknown")]
        for payload in [rows, {"jobs": rows}]:
            with tempfile.TemporaryDirectory() as folder:
                source = Path(folder) / "verified_jobs.json"
                original = json.dumps(payload)
                source.write_text(original)
                subprocess.run([sys.executable, str(script), "--workdir", folder], check=True, capture_output=True)
                html = (Path(folder) / "job-hunt-workbench.html").read_text()
                self.assertIn('"score": 89', html)
                self.assertIn('"score": null', html)
                self.assertIn('"company": "Mayflower"', html)
                self.assertEqual(source.read_text(), original)


if __name__ == "__main__":
    unittest.main()
