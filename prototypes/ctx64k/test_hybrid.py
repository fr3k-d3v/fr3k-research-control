import unittest
from hybrid import hybrid,cosine
from retrieval import Passage

class HybridTests(unittest.TestCase):
    def test_vector_and_lexical(self):
        passages=(Passage("a","public","a","other material"),Passage("b","public","b","target word"))
        out=hybrid("target word",passages,allowed_scopes=frozenset({"public"}),
                   query_vector=(1.,0.),passage_vectors={"a":(1.,0.),"b":(0.,1.)})
        self.assertEqual(out[0].id,"a")

    def test_scope_before_vector(self):
        passages=(Passage("private","secret","secret","target word"),)
        self.assertEqual(hybrid("target word",passages,allowed_scopes=frozenset({"public"}),
                         query_vector=(1.,0.),passage_vectors={"private":(1.,0.)}),())

    def test_invalid_dimensions(self):
        with self.assertRaises(ValueError): cosine((1.,),(1.,2.))

if __name__ == "__main__":
    unittest.main()
