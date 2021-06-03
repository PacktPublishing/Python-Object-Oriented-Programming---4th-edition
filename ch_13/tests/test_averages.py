"""
Python 3 Object-Oriented Programming

Chapter 13.  Testing Object-Oriented Programs.
"""
from __future__ import annotations
import unittest
from typing import Optional


def average(seq: list[Optional[float]]) -> float:
    """Average of non-None values"""
    total, count = 0.0, 0
    for v in filter(None, seq):
        total += v
        count += 1
    return total / count


class TestAverage(unittest.TestCase):
    def test_zero(self) -> None:
        self.assertRaises(ZeroDivisionError, average, [])

    def test_with_zero(self) -> None:
        with self.assertRaises(ZeroDivisionError):
            average([])


if __name__ == "__main__":
    unittest.main()
