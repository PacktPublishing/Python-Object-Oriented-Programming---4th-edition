"""
Python 3 Object-Oriented Programming

Chapter 13.  Testing Object-Oriented Programs.
"""
from stats import StatsList
import unittest


class TestValidInputs(unittest.TestCase):
    def setUp(self) -> None:
        self.stats = StatsList([1, 2, 2, 3, 3, 4])

    def test_mean(self) -> None:
        self.assertEqual(self.stats.mean(), 2.5)

    def test_median(self) -> None:
        self.assertEqual(self.stats.median(), 2.5)
        self.stats.append(4)
        self.assertEqual(self.stats.median(), 3)

    def test_mode(self) -> None:
        self.assertEqual(self.stats.mode(), [2, 3])
        self.stats.remove(2)
        self.assertEqual(self.stats.mode(), [3])


if __name__ == "__main__":
    unittest.main()
