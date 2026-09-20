import importlib.util
import io
import json
from pathlib import Path
import tarfile
import tempfile
import unittest
from unittest.mock import patch
from types import SimpleNamespace

spec = importlib.util.spec_from_file_location('teleport', Path(__file__).parents[1] / 'scripts/teleport.py')
tp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tp)


class TransferTests(unittest.TestCase):
    def test_failed_destination_preflight_never_exports_source(self):
        root = Path(tempfile.mkdtemp(prefix='teleport-test-', dir='/tmp'))
        a = SimpleNamespace(source='local', dest='m1srv', run_id='preflight',
                            as_kind=None, kind='codex')
        with patch.object(tp, 'ROOT', root), patch.object(tp, 'endpoint') as endpoint:
            endpoint.return_value = {'codex_runtime': {'ready': False, 'error': 'fixture timeout'}}
            with self.assertRaisesRegex(RuntimeError, 'source was not stopped'):
                tp.transfer(a)
            endpoint.assert_called_once_with('m1srv', 'doctor', {})

    def test_corrupt_bundle_is_rejected_before_import(self):
        root = Path(tempfile.mkdtemp(prefix='teleport-test-', dir='/tmp'))
        archive = root / 'corrupt.tar'
        archive.write_bytes(b'not the exported bundle')
        with self.assertRaisesRegex(RuntimeError, 'checksum mismatch'):
            tp.import_session({'run_id': 'test-' + root.name, 'archive': str(archive), 'sha256': '0' * 64})

    def test_archive_escape_and_symlink_rejected(self):
        root = Path(tempfile.mkdtemp(prefix='teleport-test-', dir='/tmp'))
        for name, kind in [('../escape', tarfile.REGTYPE), ('link', tarfile.SYMTYPE)]:
            archive = root / ('bad-' + kind.decode() + '.tar')
            with tarfile.open(archive, 'w') as tf:
                m = tarfile.TarInfo(name)
                m.type = kind
                m.linkname = '/tmp'
                tf.addfile(m, io.BytesIO())
            with self.assertRaises(RuntimeError):
                tp.extract_safe(archive, root / 'dest')

    def test_workspace_roundtrip_staged_unstaged_binary_deleted_and_untracked(self):
        root = Path(tempfile.mkdtemp(prefix='teleport-test-', dir='/tmp'))
        repo = root / 'source'
        repo.mkdir()
        tp.git(repo, 'init')
        tp.git(repo, 'config', 'user.name', 'Teleport Test')
        tp.git(repo, 'config', 'user.email', 'teleport-test@example.invalid')
        (repo / 'text.txt').write_text('base\n')
        (repo / 'delete.txt').write_text('delete\n')
        (repo / 'image.bin').write_bytes(bytes(range(256)))
        tp.git(repo, 'add', '.')
        tp.git(repo, 'commit', '-m', 'Fixture')
        (repo / 'text.txt').write_text('staged\n')
        tp.git(repo, 'add', 'text.txt')
        (repo / 'text.txt').write_text('staged\nunstaged\n')
        (repo / 'delete.txt').unlink()
        (repo / 'image.bin').write_bytes(b'changed\x00binary')
        (repo / 'new file.txt').write_text('untracked\n')
        (repo / '.env').write_text('PLACEHOLDER=not-a-real-secret\n')
        stage = root / 'stage'
        stage.mkdir()
        m = tp.workspace_export(repo, stage, [])
        restored = tp.workspace_restore(stage, m, 'test-' + root.name)
        self.assertEqual((restored / 'text.txt').read_bytes(), (repo / 'text.txt').read_bytes())
        self.assertEqual((restored / 'image.bin').read_bytes(), (repo / 'image.bin').read_bytes())
        self.assertFalse((restored / 'delete.txt').exists())
        self.assertEqual((restored / 'new file.txt').read_text(), 'untracked\n')
        self.assertFalse((restored / '.env').exists())
        self.assertEqual(m['excluded'], [str(repo.resolve() / '.env')])
        self.assertEqual(tp.git(repo, 'diff', '--cached', '--binary').stdout,
                         tp.git(restored, 'diff', '--cached', '--binary').stdout)
        with self.assertRaises(RuntimeError):
            tp.workspace_restore(stage, m, 'test-' + root.name)


if __name__ == '__main__':
    unittest.main()
