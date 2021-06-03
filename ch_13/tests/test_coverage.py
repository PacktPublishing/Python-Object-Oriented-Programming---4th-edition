"""
Python 3 Object-Oriented Programming

Chapter 13.  Testing Object-Oriented Programs.
"""
import pytest
from stats import StatsList


@pytest.fixture
def valid_stats() -> StatsList:
    return StatsList([1, 2, 2, 3, 3, 4])


def test_mean(valid_stats: StatsList) -> None:
    assert valid_stats.mean() == 2.5
