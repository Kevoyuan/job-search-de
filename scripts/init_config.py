#!/usr/bin/env python3
"""Create candidate-specific .job-search configuration without overwriting files."""

import argparse
import shutil
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--workdir", default=".")
    args = parser.parse_args()

    skill_root = Path(__file__).resolve().parent.parent
    template_dir = skill_root / "assets" / "config-template"
    destination = Path(args.workdir).resolve() / ".job-search"
    destination.mkdir(parents=True, exist_ok=True)

    created = []
    preserved = []
    for source in sorted(template_dir.iterdir()):
        target = destination / source.name
        if target.exists():
            preserved.append(target.name)
            continue
        shutil.copyfile(source, target)
        created.append(target.name)

    print("config_dir=" + str(destination))
    print("created=" + ",".join(created))
    print("preserved=" + ",".join(preserved))


if __name__ == "__main__":
    main()
