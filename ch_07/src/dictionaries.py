"""
Python 3 Object-Oriented Programming

Chapter 7. Python Data Structures
"""
from __future__ import annotations
import sys


def letter_frequency(sentence: str) -> dict[str, int]:
    frequencies: dict[str, int] = {}
    for letter in sentence:
        frequency = frequencies.setdefault(letter, 0)
        frequencies[letter] = frequency + 1
    return frequencies


test_lf_1 = """
>>> txt = "A quick brown fox jumps over the lazy dog"
>>> letter_frequency(txt)
{'A': 1, ' ': 8, 'q': 1, 'u': 2, 'i': 1, 'c': 1, 'k': 1, 'b': 1, 'r': 2, 'o': 4, 'w': 1, 'n': 1, 'f': 1, 'x': 1, 'j': 1, 'm': 1, 'p': 1, 's': 1, 'v': 1, 'e': 2, 't': 1, 'h': 1, 'l': 1, 'a': 1, 'z': 1, 'y': 1, 'd': 1, 'g': 1}

"""

from collections import defaultdict


def letter_frequency_2(sentence: str) -> defaultdict[str, int]:
    frequencies: defaultdict[str, int] = defaultdict(int)
    for letter in sentence:
        frequencies[letter] += 1
    return frequencies


test_lf_2 = """
>>> txt = "A quick brown fox jumps over the lazy dog"
>>> letter_frequency_2(txt)
defaultdict(<class 'int'>, {'A': 1, ' ': 8, 'q': 1, 'u': 2, 'i': 1, 'c': 1, 'k': 1, 'b': 1, 'r': 2, 'o': 4, 'w': 1, 'n': 1, 'f': 1, 'x': 1, 'j': 1, 'm': 1, 'p': 1, 's': 1, 'v': 1, 'e': 2, 't': 1, 'h': 1, 'l': 1, 'a': 1, 'z': 1, 'y': 1, 'd': 1, 'g': 1})

>>> import collections
>>> lf = collections.defaultdict(lambda: "Unknown", letter_frequency_2(txt))
>>> lf["A"]
1
>>> lf[":"]
'Unknown'

"""

from collections import Counter


def letter_frequency_3(sentence: str) -> Counter[str]:
    return Counter(sentence)


test_lf_3 = """
>>> txt = "A quick brown fox jumps over the lazy dog"
>>> letter_frequency_3(txt)
Counter({' ': 8, 'o': 4, 'u': 2, 'r': 2, 'e': 2, 'A': 1, 'q': 1, 'i': 1, 'c': 1, 'k': 1, 'b': 1, 'w': 1, 'n': 1, 'f': 1, 'x': 1, 'j': 1, 'm': 1, 'p': 1, 's': 1, 'v': 1, 't': 1, 'h': 1, 'l': 1, 'a': 1, 'z': 1, 'y': 1, 'd': 1, 'g': 1})

"""


__test__ = {name: case for name, case in globals().items() if name.startswith("test_")}
