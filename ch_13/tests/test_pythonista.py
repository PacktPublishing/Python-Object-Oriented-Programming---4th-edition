"""
Python 3 Object-Oriented Programming

Chapter 13.  Testing Object-Oriented Programs.
"""
import sys
import pytest


def test_simple_skip() -> None:
    if sys.platform != "ios":
        pytest.skip("Test works only on Pythonista for ios")

    import location  # type: ignore [import]

    img = location.render_map_snapshot(36.8508, -76.2859)
    assert img is not None
