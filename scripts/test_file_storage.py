import os
from pathlib import Path
import tempfile
import time
import unittest
from unittest.mock import patch
from file_storage import atomic_write, save_with_backup
from cleanup_backups import cleanup, run_cleanup


class StorageTests(unittest.TestCase):
    def test_retention_and_unchanged_write(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve()
            source = root / 'verified_jobs.json'
            source.write_text('old')
            save_with_backup(source, 'new', root)
            before = source.stat().st_mtime_ns
            self.assertFalse(save_with_backup(source, 'new', root))
            self.assertEqual(before, source.stat().st_mtime_ns)
            backup = next((root / '.job-search/backups').iterdir())
            os.utime(backup, (time.time() - 40 * 86400,) * 2)
            for i in range(8):
                (root / f'page.html.bak-{i}').write_text('copy')
            self.assertEqual(len(cleanup(root, True)), 3)
            self.assertEqual(len(list(root.glob('page.html.bak-*'))), 8)
            run_cleanup(root)
            self.assertEqual(len(list(root.glob('page.html.bak-*'))), 5)
            self.assertTrue(backup.exists())
            self.assertEqual(source.read_text(), 'new')

    def test_failed_replace_preserves_original(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / 'data.json'
            source.write_text('original')
            with patch('file_storage.os.replace', side_effect=OSError('test failure')):
                with self.assertRaises(OSError):
                    atomic_write(source, 'changed')
            self.assertEqual(source.read_text(), 'original')
            self.assertEqual(list(Path(tmp).iterdir()), [source])

    def test_symlink_and_recent_directory_are_preserved(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve()
            live = root / 'data.json'
            live.write_text('live')
            (root / 'link.bak-old').symlink_to(live)
            directory = root / '.bak-old'
            directory.mkdir()
            (directory / 'recent').write_text('recent')
            os.utime(directory, (time.time() - 40 * 86400,) * 2)
            self.assertEqual(cleanup(root), [])


if __name__ == '__main__':
    unittest.main()
