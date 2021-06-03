"""
Python 3 Object-Oriented Programming

Chapter 6, Abstract Base Classes and Operator Overloading
"""
from lookup_mapping import Lookup

def test_lookup_mapping():
    x = Lookup(
        [
            ["z", "Zillah"],
            ["a", "Amy"],
            ["c", "Clara"],
            ["b", "Basil"],
        ]
    )

    assert "a" in x
    assert "d" not in x
    assert len(x) == 4
    assert x["a"] == "Amy"
    assert x["z"] == "Zillah"
    assert list(x) == ["a", "b", "c", "z"]
