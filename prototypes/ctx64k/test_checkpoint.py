import unittest
from checkpoint import Checkpoint, encode, decode

class CheckpointTests(unittest.TestCase):
    def fixture(self):
        return Checkpoint(1, "CTX-64K", "Improve useful context", ("Never lose approvals",),
                          ("github:issue/5",), ("Test 64K",), ("GPU timeout unverified",),
                          "github:commit/baseline", "PARTIALLY_VERIFIED")

    def test_roundtrip(self):
        x = self.fixture()
        self.assertEqual(decode(encode(x)), x)
        self.assertEqual(encode(decode(encode(x))), encode(x))

    def test_unknown_state_fails(self):
        x = encode(self.fixture()).replace("PARTIALLY_VERIFIED", "SUCCESS")
        with self.assertRaises(ValueError): decode(x)

    def test_missing_fields_fail(self):
        with self.assertRaises(ValueError): decode('{"schema_version":1}')

    def test_reject_untrusted_extra_fields(self):
        x = encode(self.fixture()).replace('"schema_version":1', '"new_authority":"admin","schema_version":1')
        with self.assertRaises(ValueError): decode(x)

if __name__ == "__main__":
    unittest.main()
