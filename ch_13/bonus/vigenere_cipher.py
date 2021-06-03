"""
Python 3 Object-Oriented Programming

Chapter 13.  Testing Object-Oriented Programs.
"""
from string import ascii_uppercase
from typing import Callable


class VigenèreCipher:
    """Version 1. Incomplete"""

    def __init__(self, keyword: str) -> None:
        self.keyword = keyword

    def encode(self, plaintext: str) -> str:
        return "XECWQXUIVCRKHWA"

    def extend_keyword(self, length: int) -> str:
        repeats = length // len(self.keyword) + 1
        return (self.keyword * repeats)[:length]


class VigenèreCipher_2:
    """Version 2. Complete"""

    def __init__(self, keyword: str) -> None:
        self.keyword = keyword

    def encode(self, plaintext: str) -> str:
        keyword = self.extend_keyword(len(plaintext))
        encoded = (combine_character(p, k) for p, k in zip(plaintext, keyword))
        return "".join(encoded)

    def decode(self, ciphertext: str) -> str:
        keyword = self.extend_keyword(len(ciphertext))
        decoded = (separate_character(c, k) for c, k in zip(ciphertext, keyword))
        return "".join(decoded)

    def extend_keyword(self, length: int) -> str:
        repeats = length // len(self.keyword) + 1
        return (self.keyword * repeats)[:length]


class VigenèreCipher_3:
    """Version 3. Refactored"""

    def __init__(self, keyword: str) -> None:
        self.keyword = keyword

    def _code(self, text: str, combiner: Callable[[str, str], str]) -> str:
        text = text.replace(" ", "").upper()
        keyword = self.extend_keyword(len(text))
        trans_coded = (combiner(t, k) for t, k in zip(text, keyword))
        return "".join(trans_coded)

    def encode(self, plaintext: str) -> str:
        return self._code(plaintext, combine_character)

    def decode(self, ciphertext: str) -> str:
        return self._code(ciphertext, separate_character)

    def extend_keyword(self, length: int) -> str:
        repeats = length // len(self.keyword) + 1
        return (self.keyword * repeats)[:length]


def combine_character(plain: str, key: str) -> str:
    p = ascii_uppercase.index(plain.upper())
    k = ascii_uppercase.index(key.upper())
    return ascii_uppercase[(p + k) % len(ascii_uppercase)]


def separate_character(cipher: str, key: str) -> str:
    c = ascii_uppercase.index(cipher.upper())
    k = ascii_uppercase.index(key.upper())
    return ascii_uppercase[(c - k) % len(ascii_uppercase)]
