"""
Python 3 Object-Oriented Programming

Chapter 13.  Testing Object-Oriented Programs.
"""
import unittest
import sys


class SkipTests(unittest.TestCase):
    @unittest.expectedFailure
    def test_fails(self) -> None:
        self.assertEqual(False, True)

    @unittest.skip("Test is useless")
    def test_skip(self) -> None:
        self.assertEqual(False, True)

    @unittest.expectedFailure  # Remove this to see the effect of version number tests.
    @unittest.skipIf(sys.version_info.minor == 8, "broken on 3.8")
    def test_skipif(self) -> None:
        self.assertEqual(False, True)

    @unittest.skipUnless(sys.platform.startswith("linux"), "broken unless on linux")
    def test_skipunless(self) -> None:
        self.assertEqual(False, True)


if __name__ == "__main__":
    unittest.main()
