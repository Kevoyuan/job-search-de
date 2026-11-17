#!/usr/bin/env python3
"""Remove expired, explicitly named local backups; never follow symlinks."""
import argparse
import datetime
import json
from file_storage import atomic_write
import configparser
import re
import shutil
import time
from pathlib import Path

BACKUP = re.compile(r'(?:^\.bak(?:-|$)|\.bak(?:[-.]|$)|\.backup(?:[-.]|$))')


def newest_mtime(path):
    newest = path.lstat().st_mtime
    if path.is_dir():
        for child in path.iterdir():
            if not child.is_symlink():
                newest = max(newest, newest_mtime(child))
    return newest


def cleanup(workdir, dry_run=False):
    workdir = Path(workdir).resolve()
    config = configparser.ConfigParser(interpolation=None)
    config.read(workdir / '.job-search/settings.ini', encoding='utf-8')
    days = config.getint('maintenance', 'backup_retention_days', fallback=30)
    if days < 1:
        raise ValueError('backup_retention_days must be a positive integer')
    maximum = config.getint('maintenance', 'backup_max_per_file', fallback=5)
    if maximum < 1:
        raise ValueError('backup_max_per_file must be positive')
    cutoff = time.time() - days * 86400
    removed = []
    groups = {}
    directories = [workdir, workdir / '.job-search']
    central = workdir / '.job-search/backups'
    if central.is_dir() and not central.is_symlink():
        directories.append(central)
        # New backups only use this one additional level for project configuration.
        directories.append(central / '.job-search')
    for directory in directories:
        if directory.is_symlink() or not directory.is_dir():
            continue
        for path in directory.iterdir():
            if path.is_symlink() or not BACKUP.search(path.name):
                continue
            base = BACKUP.split(path.name)[0]
            is_config = directory == workdir / '.job-search' or directory == central / '.job-search'
            key = ('config' if is_config else 'root', base or path.name)
            groups.setdefault(key, []).append((newest_mtime(path), path))
    for (_, base), entries in groups.items():
        entries.sort(key=lambda item: (item[0], str(item[1])), reverse=True)
        for index, (modified, path) in enumerate(entries):
            # Keep one recovery copy of canonical job data, even after expiry.
            if index == 0 and base == 'verified_jobs.json':
                continue
            if index < maximum and modified >= cutoff:
                continue
            if not dry_run:
                if path.is_dir():
                    shutil.rmtree(path)
                else:
                    path.unlink()
            removed.append(str(path))
    return removed


def run_cleanup(workdir, dry_run=False):
    state = Path(workdir) / '.job-search/backup-cleanup-status.json'
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    try:
        removed = cleanup(workdir, dry_run)
    except Exception as exc:
        if not dry_run:
            atomic_write(state, json.dumps({'checkedAt': now, 'removed': 0, 'error': str(exc)}, ensure_ascii=False))
        raise
    if not dry_run:
        atomic_write(state, json.dumps({'checkedAt': now, 'removed': len(removed), 'error': None}, ensure_ascii=False))
        for name in ('backup-cleanup.log', 'backup-cleanup-error.log'):
            log = Path(workdir) / '.job-search' / name
            if log.is_file() and not log.is_symlink() and log.stat().st_size > 65536:
                with log.open('r+b') as handle:
                    handle.seek(-32768, 2)
                    tail = handle.read()
                    handle.seek(0)
                    handle.write(tail)
                    handle.truncate()
    return removed


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--workdir', required=True)
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    paths = run_cleanup(args.workdir, args.dry_run)
    print(f'{"Eligible" if args.dry_run else "Removed"}: {len(paths)} expired backups')
    for path in paths:
        print(path)
