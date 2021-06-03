"""
Python 3 Object-Oriented Programming

Chapter 14.  Concurrency
"""
import abc
from PIL import Image  # type: ignore [import]
from pathlib import Path
from typing import Iterator, List


# State design with data copying.


class RLERun(abc.ABC):
    def __init__(self) -> None:
        self.value: List[int]
        self.count: int

    @abc.abstractmethod
    def state(self, next: int) -> "RLERun":
        ...

    @abc.abstractmethod
    def append(self, next: int) -> None:
        ...

    @abc.abstractmethod
    def emit(self) -> bytes:
        ...


class Replicate(RLERun):
    """
    >>> s = Replicate(42)
    >>> s.state(42) == s
    True
    >>> s.append(42)
    >>> s.value
    [42]
    >>> s.count
    2
    >>> s.state(43) == s
    False
    >>> s.emit()
    b'\x81*'

    >>> t = Replicate(43)
    >>> t.count = 127
    >>> t.state(43) == t
    True
    >>> t.append(43)
    >>> t.state(43) == t
    False
    >>> t.emit()
    b'\xff+'

    """

    flag = 0x80  # Identical Bytes

    def __init__(self, start: int) -> None:
        self.value: List[int] = [start]
        self.count = 1

    def state(self, next: int) -> "RLERun":
        if next == self.value[-1] and self.count < 128:
            return self
        return Literal()

    def append(self, next: int) -> None:
        self.count += 1

    def emit(self) -> bytes:
        return bytes([(self.count - 1) | self.flag]) + bytes(self.value)


class Literal(RLERun):
    """
    >>> s = Literal()
    >>> s.state(42) == s
    True
    >>> s.append(42)
    >>> s.state(43) == s
    True
    >>> s.append(43)
    >>> s.value
    [42, 43]
    >>> s.state(44) == s
    True
    >>> s.append(44)
    >>> s.state(44) == s
    False
    >>> s.emit()
    b'\\x01*+'

    """

    flag = 0x00  # Unique Bytes

    def __init__(self) -> None:
        self.value: List[int] = []
        self.count = 0

    def state(self, next: int) -> "RLERun":
        if self.count == 0:
            return self
        if next != self.value[-1] and len(self.value) < 128:
            return self
        last = self.value.pop(-1)
        self.count = len(self.value)
        return Replicate(last)

    def append(self, next: int) -> None:
        self.value.append(next)
        self.count = len(self.value)

    def emit(self) -> bytes:
        return bytes([(self.count - 1) | self.flag]) + bytes(self.value)


def blocks(image_bytes: bytes) -> Iterator[RLERun]:
    """
    >>> row = bytes([42, 42, 42, 42, 43, 44, 45, 45, 45])
    >>> [b.emit() for b in blocks(row)]
    [b'\\x83*', b'\\x01+,', b'\\x82-']

    """
    state: RLERun = Literal()
    for value in image_bytes:
        next_state = state.state(value)
        if next_state != state:
            # Initial state may be wrong.
            if state.count > 0:
                yield state
            state = next_state
        next_state.append(value)
    yield state


# Application


def rle(image_path: Path) -> None:
    with Image.open(image_path) as image:
        b_w = image.convert("L")
        width, height = b_w.size
        image_bytes = b_w.getdata()
        for r in range(height):
            row = image_bytes[r * width : (r + 1) * width]
            for b in blocks(row):
                print(b)


def main() -> None:
    files = (Path.cwd() / "images").glob("bricks*.png")
    for image_path in files:
        rle(image_path)


if __name__ == "__main__":
    main()
