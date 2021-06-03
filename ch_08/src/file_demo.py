"""
Python 3 Object-Oriented Programming

Chapter 8. The Intersection of Object-Oriented and Functional Programming
"""
from typing import List, Optional, Type, Literal
from types import TracebackType


class StringJoiner(List[str]):
    def __enter__(self) -> "StringJoiner":
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> Literal[False]:  # Optional[bool]:
        self.result = "".join(self)
        return False


test_joiner = """
>>> with StringJoiner("Hello") as sj:
...     sj.append(", ")
...     sj.extend("world")
...     sj.append("!")
>>> sj.result
'Hello, world!'
"""

test_joiner_exception = """
>>> with StringJoiner("Partial") as sj:
...     sj.append(" ")
...     sj.extend("Results")
...     sj.append(str(2 / 0))
...     sj.extend("Even If There's an Exception")
Traceback (most recent call last):
  ...
  File "<doctest examples.md[60]>", line 3, in <module>
    sj.append(str(2 / 0))
ZeroDivisionError: division by zero
>>> sj.result
'Partial Results'
"""

from contextlib import contextmanager
from typing import List, Any, Iterator


class StringJoiner2(List[str]):
    def __init__(self, *args: str) -> None:
        super().__init__(*args)
        self.result = "".join(self)


@contextmanager
def joiner(*args: Any) -> Iterator[StringJoiner2]:
    string_list = StringJoiner2(*args)
    try:
        yield string_list
    finally:
        string_list.result = "".join(string_list)


test_joiner2 = """
>>> with joiner("Hello") as sj:
...     sj.append(", ")
...     sj.extend("world")
...     sj.append("!")
>>> sj.result
'Hello, world!'
"""

test_joiner2_exception = """
>>> with joiner("Partial") as sj:
...     sj.append(" ")
...     sj.extend("Results")
...     sj.append(str(2 / 0))
...     sj.extend("Even If There's an Exception")
Traceback (most recent call last):
  ...
  File "<doctest examples.md[60]>", line 3, in <module>
    sj.append(str(2 / 0))
ZeroDivisionError: division by zero
>>> sj.result
'Partial Results'
"""


__test__ = {name: case for name, case in globals().items() if name.startswith("test_")}


if __name__ == "__main__":
    results = str(2 ** 2048)
    with open("big_number.txt", "w") as output:
        output.write("# A big number\n")
        output.writelines([f"{len(results)}\n", f"{results}\n"])
    with open("big_number.txt") as input:
        for line in input:
            print(line)
