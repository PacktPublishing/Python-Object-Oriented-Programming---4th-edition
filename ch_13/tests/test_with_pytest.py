"""
Python 3 Object-Oriented Programming

Chapter 13.  Testing Object-Oriented Programs.
"""
import pytest


class TestNumbers:
    def test_int_float(self) -> None:
        assert 1 == 1.0

    @pytest.mark.skip("expected to fail")
    def test_int_str(self) -> None:
        assert 1 == "1"  # type: ignore [comparison-overlap]
