"""
Python 3 Object-Oriented Programming 4th ed.

Chapter 3, When Objects Are Alike
"""

import abc


class MediaLoader(abc.ABC):
    @abc.abstractmethod
    def play(self) -> None:
        ...

    @property
    @abc.abstractmethod
    def ext(self) -> str:
        ...


test_abstractions = """
>>> MediaLoader.__abstractmethods__ == frozenset({'ext', 'play'})
True

"""

test_concrete_subclasses = """
>>> class Wav(MediaLoader): 
...     pass 
... 
>>> x = Wav() 
Traceback (most recent call last):
...
TypeError: Can't instantiate abstract class Wav with abstract methods ext, play

>>> class Ogg(MediaLoader): 
...     ext = '.ogg' 
...     def play(self) -> None: 
...         pass 
... 
>>> o = Ogg() 

"""

# Exposed here so mypy can examine this, also.


class Ogg(MediaLoader):
    ext = ".ogg"

    def play(self) -> None:
        pass


o = Ogg()

__test__ = {name: case for name, case in globals().items() if name.startswith("test_")}
