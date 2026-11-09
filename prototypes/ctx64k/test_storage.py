import os
import tempfile
import unittest
from pathlib import Path
from checkpoint import Checkpoint
from storage import save, load

class StorageTests(unittest.TestCase):
    def test_roundtrip_and_private_mode(self):
        cp = Checkpoint(1, "CTX-64K", "Preserve task", ("constraint",),
                        ("github:issue/5",), ("next",), ("failure",),
                        "baseline", "PARTIALLY_VERIFIED")
        with tempfile.TemporaryDirectory() as d:
            path = Path(d)/"nested"/"checkpoint.json"
            save(path, cp)
            self.assertEqual(load(path), cp)
            self.assertEqual(path.stat().st_mode & 0o777, 0o600)
            self.assertEqual((path.parent.stat().st_mode & 0o777), 0o700)
            save(path, cp)
            self.assertEqual(load(path), cp)

    def test_bad_checkpoint_not_written(self):
        cp = Checkpoint(1, "CTX-64K", "Task", (), (), (), (), "", "INVALID")
        with tempfile.TemporaryDirectory() as d:
            path = Path(d)/"cp.json"
            with self.assertRaises(ValueError):
                save(path, cp)
            self.assertFalse(path.exists())

if __name__ == "__main__":
    unittest.main()
