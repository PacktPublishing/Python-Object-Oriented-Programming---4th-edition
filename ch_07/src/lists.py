"""
Python 3 Object-Oriented Programming

Chapter 7. Python Data Structures
"""
from __future__ import annotations
import string

CHARACTERS = list(string.ascii_letters) + [" "]


def letter_frequency(sentence: str) -> list[tuple[str, int]]:
    frequencies = [(c, 0) for c in CHARACTERS]
    for letter in sentence:
        index = CHARACTERS.index(letter)
        frequencies[index] = (letter, frequencies[index][1] + 1)
    non_zero = [(letter, count) for letter, count in frequencies if count > 0]
    return non_zero


test_lf_1 = """
>>> txt = "A quick brown fox jumps over the lazy dog"
>>> letter_frequency(txt)
[('a', 1), ('b', 1), ('c', 1), ('d', 1), ('e', 2), ('f', 1), ('g', 1), ('h', 1), ('i', 1), ('j', 1), ('k', 1), ('l', 1), ('m', 1), ('n', 1), ('o', 4), ('p', 1), ('q', 1), ('r', 2), ('s', 1), ('t', 1), ('u', 2), ('v', 1), ('w', 1), ('x', 1), ('y', 1), ('z', 1), ('A', 1), (' ', 8)]

"""

from typing import Optional, cast, Any
from dataclasses import dataclass
import datetime
from datetime import timezone


@dataclass(frozen=True)
class MultiItem:
    data_source: str
    timestamp: Optional[float]
    creation_date: Optional[str]
    name: str
    owner_etc: str

    def __lt__(self, other: Any) -> bool:
        if self.data_source == "Local":
            self_datetime = datetime.datetime.fromtimestamp(
                cast(float, self.timestamp), tz=timezone.utc
            )
        else:
            self_datetime = datetime.datetime.fromisoformat(
                cast(str, self.creation_date)
            ).replace(tzinfo=timezone.utc)
        if other.data_source == "Local":
            other_datetime = datetime.datetime.fromtimestamp(
                cast(float, other.timestamp), tz=timezone.utc
            )
        else:
            other_datetime = datetime.datetime.fromisoformat(
                cast(str, other.creation_date)
            ).replace(tzinfo=timezone.utc)
        return self_datetime < other_datetime

    def __eq__(self, other: object) -> bool:
        return self.datetime == cast(MultiItem, other).datetime

    @property
    def datetime(self) -> datetime.datetime:
        if self.data_source == "Local":
            return datetime.datetime.fromtimestamp(
                cast(float, self.timestamp), tz=timezone.utc
            )
        else:
            return datetime.datetime.fromisoformat(
                cast(str, self.creation_date)
            ).replace(tzinfo=timezone.utc)


test_multi_item_class = """
>>> mi_0 = MultiItem("Local", 1607262522.000000, None, "Some File", "etc. 0")
>>> mi_1 = MultiItem("Remote", None, "2020-12-06T13:47:52.000001", "Another File", "etc. 1")
>>> mi_2 = MultiItem("Local", 1579355292.000002, None, "This File", "etc. 2")
>>> mi_3 = MultiItem("Remote", None, "2020-01-18T13:48:12.000003", "That File", "etc. 3")
>>> file_list = [mi_0, mi_1, mi_2, mi_3]
>>> file_list.sort()

>>> [f.datetime for f in file_list]
[datetime.datetime(2020, 1, 18, 13, 48, 12, 2, tzinfo=datetime.timezone.utc), datetime.datetime(2020, 1, 18, 13, 48, 12, 3, tzinfo=datetime.timezone.utc), datetime.datetime(2020, 12, 6, 13, 47, 52, 1, tzinfo=datetime.timezone.utc), datetime.datetime(2020, 12, 6, 13, 48, 42, tzinfo=datetime.timezone.utc)]
 
>>> from pprint import pprint
>>> pprint(file_list)
[MultiItem(data_source='Local', timestamp=1579355292.000002, creation_date=None, name='This File', owner_etc='etc. 2'),
 MultiItem(data_source='Remote', timestamp=None, creation_date='2020-01-18T13:48:12.000003', name='That File', owner_etc='etc. 3'),
 MultiItem(data_source='Remote', timestamp=None, creation_date='2020-12-06T13:47:52.000001', name='Another File', owner_etc='etc. 1'),
 MultiItem(data_source='Local', timestamp=1607262522.0, creation_date=None, name='Some File', owner_etc='etc. 0')]

"""


from functools import total_ordering


@total_ordering
class MultiItemTO(MultiItem):
    pass


test_multi_item_to = """
>>> mi_0 = MultiItem("Local", 1607280522.68012, None, "Some File", "etc. 0")
>>> mi_1 = MultiItem("Remote", None, "2020-12-06T13:47:52.849153", "Another File", "etc. 1")
>>> mi_0 < mi_1
False
>>> mi_0 <= mi_1
Traceback (most recent call last):
  ...
  File "<doctest lists.__test__.test_multi_item_to[5]>", line 1, in <module>
    mi_0 >= mi_1
TypeError: '<=' not supported between instances of 'MultiItem' and 'MultiItem'
>>> mi_0 > mi_1
True
>>> mi_0 >= mi_1
Traceback (most recent call last):
  ...
  File "<doctest lists.__test__.test_multi_item_to[5]>", line 1, in <module>
    mi_0 >= mi_1
TypeError: '>=' not supported between instances of 'MultiItem' and 'MultiItem'

>>> mito_0 = MultiItemTO("Local", 1607280522.68012, None, "Some File", "etc. 0")
>>> mito_1 = MultiItemTO("Remote", None, "2020-12-06T13:47:52.849153", "Another File", "etc. 1")
>>> mito_0 < mito_1
False
>>> mito_0 <= mito_1
False
>>> mito_0 > mito_1
True
>>> mito_0 >= mito_1
True

"""


@dataclass(frozen=True)
class SimpleMultiItem:
    data_source: str
    timestamp: Optional[float]
    creation_date: Optional[str]
    name: str
    owner_etc: str


def by_timestamp(item: SimpleMultiItem) -> datetime.datetime:
    if item.data_source == "Local":
        return datetime.datetime.fromtimestamp(
            cast(float, item.timestamp), tz=timezone.utc
        )
    elif item.data_source == "Remote":
        return datetime.datetime.fromisoformat(cast(str, item.creation_date)).replace(
            tzinfo=timezone.utc
        )
    else:
        raise ValueError(f"Unknown data_source in {item!r}")


test_multi_item_function = """
>>> mi_0 = SimpleMultiItem("Local", 1607262522.000000, None, "Some File", "etc. 0")
>>> mi_1 = SimpleMultiItem("Remote", None, "2020-12-06T13:47:52.000001", "Another File", "etc. 1")
>>> mi_2 = SimpleMultiItem("Local", 1579355292.000002, None, "This File", "etc. 2")
>>> mi_3 = SimpleMultiItem("Remote", None, "2020-01-18T13:48:12.000003", "That File", "etc. 3")
>>> file_list = [mi_0, mi_1, mi_2, mi_3]
>>> file_list.sort(key=by_timestamp)

>>> [by_timestamp(f) for f in file_list]
[datetime.datetime(2020, 1, 18, 13, 48, 12, 2, tzinfo=datetime.timezone.utc), datetime.datetime(2020, 1, 18, 13, 48, 12, 3, tzinfo=datetime.timezone.utc), datetime.datetime(2020, 12, 6, 13, 47, 52, 1, tzinfo=datetime.timezone.utc), datetime.datetime(2020, 12, 6, 13, 48, 42, tzinfo=datetime.timezone.utc)]

>>> from pprint import pprint
>>> pprint(file_list)  # default
[SimpleMultiItem(data_source='Local', timestamp=1579355292.000002, creation_date=None, name='This File', owner_etc='etc. 2'),
 SimpleMultiItem(data_source='Remote', timestamp=None, creation_date='2020-01-18T13:48:12.000003', name='That File', owner_etc='etc. 3'),
 SimpleMultiItem(data_source='Remote', timestamp=None, creation_date='2020-12-06T13:47:52.000001', name='Another File', owner_etc='etc. 1'),
 SimpleMultiItem(data_source='Local', timestamp=1607262522.0, creation_date=None, name='Some File', owner_etc='etc. 0')]

>>> file_list.sort(key=lambda item: item.name)
>>> pprint(file_list)  # name, lambda
[SimpleMultiItem(data_source='Remote', timestamp=None, creation_date='2020-12-06T13:47:52.000001', name='Another File', owner_etc='etc. 1'),
 SimpleMultiItem(data_source='Local', timestamp=1607262522.0, creation_date=None, name='Some File', owner_etc='etc. 0'),
 SimpleMultiItem(data_source='Remote', timestamp=None, creation_date='2020-01-18T13:48:12.000003', name='That File', owner_etc='etc. 3'),
 SimpleMultiItem(data_source='Local', timestamp=1579355292.000002, creation_date=None, name='This File', owner_etc='etc. 2')]

>>> import operator
>>> file_list.sort(key=operator.attrgetter("name"))
>>> pprint(file_list)  # name, attrgetter
[SimpleMultiItem(data_source='Remote', timestamp=None, creation_date='2020-12-06T13:47:52.000001', name='Another File', owner_etc='etc. 1'),
 SimpleMultiItem(data_source='Local', timestamp=1607262522.0, creation_date=None, name='Some File', owner_etc='etc. 0'),
 SimpleMultiItem(data_source='Remote', timestamp=None, creation_date='2020-01-18T13:48:12.000003', name='That File', owner_etc='etc. 3'),
 SimpleMultiItem(data_source='Local', timestamp=1579355292.000002, creation_date=None, name='This File', owner_etc='etc. 2')]

"""

# Hints for the exercises


class LocalItem:
    data_source: str
    timestamp: float
    name: str
    owner_etc: str

    def __repr__(self) -> str:
        return f"LocalItem(timestamp={self.timestamp})"


class RemoteItem:
    data_souce: str
    creation_date: str
    name: str
    owner_etc: str

    def __repr__(self) -> str:
        return f"RemoteItem(creation_date={self.creation_date})"


__test__ = {name: case for name, case in globals().items() if name.startswith("test_")}
