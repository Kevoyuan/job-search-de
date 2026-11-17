"""Atomic, change-aware writes and centralized backups."""
import datetime
import os
import tempfile
from pathlib import Path


def atomic_write(path, content):
    path = Path(path)
    content = content.encode('utf-8') if isinstance(content, str) else content
    if path.exists() and path.read_bytes() == content:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    name = None
    try:
        with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as handle:
            name = handle.name
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        if path.exists():
            os.chmod(name, path.stat().st_mode & 0o777)
        os.replace(name, path)
    finally:
        if name and os.path.exists(name):
            os.unlink(name)
    return True


def save_with_backup(path, content, workdir):
    path = Path(path)
    content = content.encode('utf-8') if isinstance(content, str) else content
    if path.exists():
        original = path.read_bytes()
        if original == content:
            return False
        relative = path.resolve().relative_to(Path(workdir).resolve())
        stamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
        backup = Path(workdir) / '.job-search/backups' / relative.parent / (relative.name + '.bak-' + stamp)
        atomic_write(backup, original)
    return atomic_write(path, content)
