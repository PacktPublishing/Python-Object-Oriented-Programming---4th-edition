"""
Python 3 Object-Oriented Programming

Chapter 10. The Iterator Pattern
"""
from typing import Iterable, Iterator


class CapitalIterable(Iterable[str]):
    def __init__(self, string: str) -> None:
        self.string = string

    def __iter__(self) -> Iterator[str]:
        return CapitalIterator(self.string)


class CapitalIterator(Iterator[str]):
    def __init__(self, string: str) -> None:
        self.words = [w.capitalize() for w in string.split()]
        self.index = 0

    def __next__(self) -> str:
        if self.index == len(self.words):
            raise StopIteration()

        word = self.words[self.index]
        self.index += 1
        return word

    # def __iter__(self) -> Iterator[str]:
    #     return self


test_iterable = """
>>> iterable = CapitalIterable('the quick brown fox jumps over the lazy dog')
>>> iterator = iter(iterable)
>>> while True:
...     try:
...         print(next(iterator))
...     except StopIteration:
...         break
...     
The
Quick
Brown
Fox
Jumps
Over
The
Lazy
Dog

>>> for i in iterable:
...     print(i)
...     
The
Quick
Brown
Fox
Jumps
Over
The
Lazy
Dog

>>> iterator = iter(iterable)
>>> for i in iter(iterator):
...     print(i)
...
The
Quick
Brown
Fox
Jumps
Over
The
Lazy
Dog

"""


__test__ = {name: case for name, case in globals().items() if name.startswith("test_")}
