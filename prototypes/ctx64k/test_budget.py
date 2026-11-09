import unittest
from budget import ContextItem, ContextOverflow, plan_context

class BudgetTests(unittest.TestCase):
    def test_hard_limit_and_mandatory(self):
        items = [ContextItem("system", 100, 0, True), ContextItem("code", 700, 9), ContextItem("log", 600, 1)]
        result = plan_context(items, capacity=1000, output_reserve=200)
        self.assertEqual(result.kept, ("system", "code"))
        self.assertEqual(result.dropped, ("log",))
        self.assertEqual(result.used_tokens + result.reserved_output, 1000)

    def test_deterministic_priority_and_ties(self):
        items = [ContextItem("a", 10, 3), ContextItem("b", 10, 3), ContextItem("c", 10, 4)]
        self.assertEqual(plan_context(items, capacity=20, output_reserve=0).kept, ("a", "c"))

    def test_required_overflow_fails_closed(self):
        with self.assertRaises(ContextOverflow):
            plan_context([ContextItem("system", 100, 0, True)], capacity=100, output_reserve=1)

    def test_duplicate_and_negative_rejected(self):
        with self.assertRaises(ValueError):
            plan_context([ContextItem("x", 1, 0), ContextItem("x", 2, 0)])
        with self.assertRaises(ValueError):
            plan_context([ContextItem("x", -1, 0)])

    def test_overhead_counted(self):
        r = plan_context([ContextItem("a", 50, 1)], capacity=100, output_reserve=20, fixed_overhead=30)
        self.assertEqual(r.used_tokens, 80)

if __name__ == "__main__":
    unittest.main()
