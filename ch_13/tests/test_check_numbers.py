"""
Python 3 Object-Oriented Programming

Chapter 13.  Testing Object-Oriented Programs.
"""
import unittest


class CheckNumbers(unittest.TestCase):
    def test_int_float(self) -> None:
        self.assertEqual(1, 1.0)

    @unittest.expectedFailure
    def test_str_float(self) -> None:
        """Remove the @unittest.expectedFailure decorator to see a failing test."""
        self.assertEqual(1, "1")


if __name__ == "__main__":
    unittest.main()
