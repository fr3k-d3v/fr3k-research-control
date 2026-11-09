import unittest
from retrieval import Passage, retrieve

class RetrievalTests(unittest.TestCase):
    def test_scope_isolation(self):
        p = [Passage("private", "alice", "github:private", "secret alpha token"),
             Passage("public", "public", "github:public", "alpha token")]
        hits = retrieve("alpha token", p, allowed_scopes=frozenset({"public"}))
        self.assertEqual(tuple(x.id for x in hits), ("public",))

    def test_exact_match_ranks_first(self):
        p = [Passage("a", "public", "a", "beta alpha x"),
             Passage("b", "public", "b", "alpha beta")]
        self.assertEqual(retrieve("alpha beta", p, allowed_scopes=frozenset({"public"}))[0].id, "b")

    def test_bounded_text_and_no_matches(self):
        p = [Passage("a", "public", "a", "needle " + "x"*100)]
        hits = retrieve("needle", p, allowed_scopes=frozenset({"public"}), max_chars_per_hit=10)
        self.assertEqual(len(hits[0].text), 10)
        self.assertEqual(retrieve("missing", p, allowed_scopes=frozenset({"public"})), ())

    def test_duplicate_rejected(self):
        p = [Passage("x", "public", "a", "alpha"), Passage("x", "private", "b", "beta")]
        with self.assertRaises(ValueError):
            retrieve("alpha", p, allowed_scopes=frozenset({"public"}))

if __name__ == "__main__":
    unittest.main()
