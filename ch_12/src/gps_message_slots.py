"""
Python 3 Object-Oriented Programming

Chapter 12. Advanced Python Design Patterns
"""
from __future__ import annotations
import abc
import weakref
from dataclasses import dataclass
from math import radians, floor, fmod
from typing import (
    Optional,
    cast,
    Container,
    overload,
    Union,
    Sequence,
    Iterator,
)


class Point:
    __slots__ = ("latitude", "longitude")

    def __init__(self, latitude: float, longitude: float) -> None:
        self.latitude = latitude
        self.longitude = longitude

    def __repr__(self) -> str:
        return f"Point(latitude={self.latitude}, longitude={self.longitude})"

    @classmethod
    def from_bytes(
        cls,
        latitude: bytes,
        N_S: bytes,
        longitude: bytes,
        E_W: bytes,
    ) -> "Point":
        lat_deg = float(latitude[:2]) + float(latitude[2:]) / 60
        lat_sign = 1 if N_S.upper() == b"N" else -1
        lon_deg = float(longitude[:3]) + float(longitude[3:]) / 60
        lon_sign = 1 if E_W.upper() == b"E" else -1
        return Point(lat_deg * lat_sign, lon_deg * lon_sign)

    def __str__(self) -> str:
        lat = abs(self.latitude)
        lat_deg = floor(lat)
        lat_min_sec = 60 * (lat - lat_deg)
        lat_dir = "N" if self.latitude > 0 else "S"
        lon = abs(self.longitude)
        lon_deg = floor(lon)
        lon_min_sec = 60 * (lon - lon_deg)
        lon_dir = "E" if self.longitude > 0 else "W"
        return (
            f"({lat_deg:02.0f}°{lat_min_sec:07.4f}{lat_dir}, "
            f"{lon_deg:03.0f}°{lon_min_sec:07.4f}{lon_dir})"
        )

    @property
    def lat(self) -> float:
        return radians(self.latitude)

    @property
    def lon(self) -> float:
        return radians(self.longitude)


test_point = """
>>> p = Point.from_bytes(b"4916.45", b"N", b"12311.12", b"W")
>>> p
Point(latitude=49.274166666666666, longitude=-123.18533333333333)
>>> str(p)
'(49°16.4500N, 123°11.1200W)'

>>> p.lat
0.8599964445097726
>>> p.lon
-2.1499896568333883

>>> p2 = Point(latitude=49.274, longitude=-123.185)
>>> p2.extra_attribute = 42
Traceback (most recent call last):
...
AttributeError: 'Point' object has no attribute 'extra_attribute'

"""


class Buffer(Sequence[int]):
    def __init__(self, content: bytes) -> None:
        self.content = content

    def __len__(self) -> int:
        return len(self.content)

    def __iter__(self) -> Iterator[int]:
        return iter(self.content)

    @overload
    def __getitem__(self, index: int) -> int:
        ...

    @overload
    def __getitem__(self, index: slice) -> bytes:
        ...

    def __getitem__(self, index: Union[int, slice]) -> Union[int, bytes]:
        return self.content[index]


class GPSError(Exception):
    pass


class Message:
    __slots__ = ("buffer", "offset", "end", "commas")

    def __init__(self) -> None:
        self.buffer: weakref.ReferenceType[Buffer]
        self.offset: int
        self.end: Optional[int]
        self.commas: list[int]

    def from_buffer(self, buffer: Buffer, offset: int) -> "Message":
        self.buffer = weakref.ref(buffer)
        self.offset = offset
        self.commas = [offset]
        self.end = None
        for index in range(offset, offset + 82):
            if buffer[index] == ord(b","):
                self.commas.append(index)
            elif buffer[index] == ord(b"*"):
                self.commas.append(index)
                self.end = index + 3
                break
        if self.end is None:
            raise GPSError("Incomplete")
        # TODO: confirm checksum.
        return self

    def __getitem__(self, field: int) -> bytes:
        if not hasattr(self, "buffer") or (buffer := self.buffer()) is None:
            raise RuntimeError("Broken reference")
        start, end = self.commas[field] + 1, self.commas[field + 1]
        return buffer[start:end]

    def get_fix(self) -> Point:
        return Point.from_bytes(
            self.latitude(), self.lat_n_s(), self.longitude(), self.lon_e_w()
        )

    @abc.abstractmethod
    def latitude(self) -> bytes:
        ...

    @abc.abstractmethod
    def lat_n_s(self) -> bytes:
        ...

    @abc.abstractmethod
    def longitude(self) -> bytes:
        ...

    @abc.abstractmethod
    def lon_e_w(self) -> bytes:
        ...


class GPGGA(Message):
    __slots__ = ()

    def latitude(self) -> bytes:
        return self[2]

    def lat_n_s(self) -> bytes:
        return self[3]

    def longitude(self) -> bytes:
        return self[4]

    def lon_e_w(self) -> bytes:
        return self[5]


test_gpgga = """
>>> raw = Buffer(b"$GPGGA,170834,4124.8963,N,08151.6838,W,1,05,1.5,280.2,M,-34.0,M,,*75")
>>> m = GPGGA()
>>> m.from_buffer(raw, 0)
<gps_message_slots.GPGGA object...
>>> fix = m.get_fix()
>>> fix
Point(latitude=41.41493833333333, longitude=-81.86139666666666)
>>> fix.lat
0.7228270334270795
>>> fix.lon
-1.4287509021144442

"""

test_gpgga_bad = """
>>> raw = Buffer(b"$GPGGA,170834,4124.8963,N,08151.6838,W,1,05,1.5,280.2,M,-34.0,M,,*75")
>>> m = GPGGA()
>>> fix = m.get_fix()
Traceback (most recent call last):
...
RuntimeError: Broken reference

>>> m.__class__.__mro__
(<class 'gps_message_slots.GPGGA'>, <class 'gps_message_slots.Message'>, <class 'object'>)

>>> m.__class__.__mro__[1].__slots__
('buffer', 'offset', 'end', 'commas')

>>> m.__dict__
Traceback (most recent call last):
...
AttributeError: 'GPGGA' object has no attribute '__dict__'


"""


class GPGLL(Message):
    __slots__ = ()

    def latitude(self) -> bytes:
        return self[1]

    def lat_n_s(self) -> bytes:
        return self[2]

    def longitude(self) -> bytes:
        return self[3]

    def lon_e_w(self) -> bytes:
        return self[4]


test_gpgll = """
>>> raw = Buffer(b"$GPGLL,3751.65,S,14507.36,E*77")
>>> m = GPGLL()
>>> m.from_buffer(raw, 0)
<gps_message_slots.GPGLL object...
>>> fix = m.get_fix()
>>> fix
Point(latitude=-37.86083333333333, longitude=145.12266666666667)
>>> fix.lat
-0.6607961992154864
>>> fix.lon
2.5328683526075575

"""


class GPRMC(Message):
    __slots__ = ()

    def latitude(self) -> bytes:
        return self[3]

    def lat_n_s(self) -> bytes:
        return self[4]

    def longitude(self) -> bytes:
        return self[5]

    def lon_e_w(self) -> bytes:
        return self[6]


test_gprmc = """
>>> raw = Buffer(b"$GPRMC,225446,A,4916.45,N,12311.12,W,000.5,054.7,191194,020.3,E*68")
>>> m = GPRMC()
>>> m.from_buffer(raw, 0)
<gps_message_slots.GPRMC object...
>>> fix = m.get_fix()
>>> fix
Point(latitude=49.274166666666666, longitude=-123.18533333333333)
>>> fix.lat
0.8599964445097726
>>> fix.lon
-2.1499896568333883

"""


def message_factory(header: bytes) -> Optional[Message]:
    # TODO: Add functools.lru_cache to save storage and time
    if header == b"GPGGA":
        return GPGGA()
    elif header == b"GPGLL":
        return GPGLL()
    elif header == b"GPRMC":
        return GPRMC()
    else:
        return None


test_factory = """
>>> buffer = Buffer(
...     b"$GPGLL,3751.65,S,14507.36,E*77"
... )
>>> flyweight = message_factory(buffer[1 : 6])
>>> flyweight.__class__.__name__
'GPGLL'
>>> flyweight.from_buffer(buffer, 0)
<gps_message_slots.GPGLL object at ...>

>>> flyweight.get_fix()
Point(latitude=-37.86083333333333, longitude=145.12266666666667)
>>> print(flyweight.get_fix())
(37°51.6500S, 145°07.3600E)

>>> buffer_2 = Buffer(
...     b"$GPGLL,3751.65,S,14507.36,E*77\\r\\n"
...     b"$GPGLL,3723.2475,N,12158.3416,W,161229.487,A,A*41\\r\\n"
... )
>>> start = 0
>>> flyweight = message_factory(buffer_2[start+1 : start+6])
>>> p_1 = flyweight.from_buffer(buffer_2, start).get_fix()
>>> p_1
Point(latitude=-37.86083333333333, longitude=145.12266666666667)
>>> print(p_1)
(37°51.6500S, 145°07.3600E)

>>> flyweight.end
30
>>> next_start = buffer_2.index(ord(b"$"), flyweight.end)
>>> next_start
32
>>> 
>>> p_2 = flyweight.from_buffer(buffer_2, next_start).get_fix()
>>> p_2
Point(latitude=37.387458333333335, longitude=-121.97236)
>>> print(p_2)
(37°23.2475N, 121°58.3416W)

"""


class Client:
    def __init__(self, buffer: Buffer) -> None:
        self.buffer = buffer

    def scan(self) -> None:
        end = 0
        while True:
            try:
                start = self.buffer.index(ord(b"$"), end)
                header = self.buffer[start + 1 : start + 6]
                m = message_factory(header)
                if m:
                    fix = m.from_buffer(self.buffer, start).get_fix()
                    print(fix)
                    end = cast(int, m.end)
                else:
                    star = self.buffer.index(ord(b"*"), end)
                    end = star + 3
            except ValueError:
                # No "$" found: no more messages
                break
            except GPSError:
                # No final "*" found: last message damaged
                break


test_client = """
>>> buffer = Buffer(b'''
... $GPGGA,161229.487,3723.2475,N,12158.3416,W,1,07,1.0,9.0,M,,,,0000*18
... $GPGLL,3723.2475,N,12158.3416,W,161229.487,A,A*41
... $GPGSA,A,3,07,02,26,27,09,04,15,,,,,,1.8,1.0,1.5*33
... $GPVTG,309.62,T,,M,0.13,N,0.2,K,A*23
... $GPRMC,161229.487,A,3723.2475,N,12158.3416,W,0.13,309.62,120598,,*10
... ''')
>>> c = Client(buffer)
>>> len(buffer)
278
>>> bytes([buffer[1]])
b'$'
>>> buffer[2:7]
b'GPGGA'
>>> c.scan()
(37°23.2475N, 121°58.3416W)
(37°23.2475N, 121°58.3416W)
(37°23.2475N, 121°58.3416W)


"""

__test__ = {name: case for name, case in globals().items() if name.startswith("test_")}
