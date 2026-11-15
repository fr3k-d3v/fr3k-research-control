import json
import unittest
from unittest.mock import patch
from tokenizer import count, tokenize, TokenizerError

class FakeResponse:
    def __enter__(self): return self
    def __exit__(self, *args): pass
    def read(self, *args): return json.dumps({"tokens":[1,2,3]}).encode()

class TokenizerTests(unittest.TestCase):
    def test_count_and_authorization(self):
        with patch("tokenizer.urlopen", return_value=FakeResponse()) as request:
            self.assertEqual(count("abc", base_url="http://127.0.0.1:8080", api_key="test"), 3)
            self.assertEqual(request.call_args.args[0].get_header("Authorization"), "Bearer test")

    def test_bad_endpoint_rejected(self):
        with self.assertRaises(ValueError):
            tokenize("hi", base_url="file:///etc/passwd", api_key="test")

    def test_fail_closed(self):
        with patch("tokenizer.urlopen", side_effect=OSError("offline")):
            with self.assertRaises(TokenizerError):
                count("hi", base_url="http://127.0.0.1:8080", api_key="test")

if __name__ == "__main__":
    unittest.main()
