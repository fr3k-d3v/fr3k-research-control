import unittest
from hermes_adapter import Message, assemble
from budget import ContextOverflow

class HermesAdapterTests(unittest.TestCase):
    def test_system_preserved(self):
        m = (Message("s","system","system",required=True),
             Message("u","user","user",priority=10),
             Message("log","tool","verbose",priority=0))
        result = assemble(m,count_tokens=len,capacity=15,output_reserve=2)
        self.assertEqual([x["role"] for x in result],["system","user"])

    def test_privileged_not_optional(self):
        with self.assertRaises(ValueError):
            assemble((Message("s","system","text"),),count_tokens=len)

    def test_required_overflow(self):
        with self.assertRaises(ContextOverflow):
            assemble((Message("s","system","required",required=True),),
                     count_tokens=len,capacity=5,output_reserve=1)

if __name__ == "__main__":
    unittest.main()
