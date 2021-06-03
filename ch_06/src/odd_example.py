"""
Python 3 Object-Oriented Programming Case Study

Chapter 3, When Objects Are Alike
"""

from collections.abc import Container


class OddIntegers:
    def __contains__(self, x: int) -> bool:
        return x % 2 != 0


test_odd = """
>>> odd = OddIntegers()
>>> 1 in odd
True
>>> 2 in odd
False
>>> 3 in odd
True
"""

test_instance = """
>>> odd = OddIntegers()
>>> isinstance(odd, Container)
True
>>> issubclass(OddIntegers, Container)
True

"""

__test__ = {name: case for name, case in globals().items() if name.startswith("test_")}
