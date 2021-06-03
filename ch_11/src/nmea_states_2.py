"""
Python 3 Object-Oriented Programming

Chapter 11. Common Design Patterns
"""
from __future__ import annotations
from typing import Optional, Iterable, Iterator, cast


class NMEA_State:
    def enter(self, message: "Message") -> "NMEA_State":
        return self

    def feed_byte(self, message: "Message", input: int) -> "NMEA_State":
        return self

    def valid(self, message: "Message") -> bool:
        return False

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"


class Waiting(NMEA_State):
    def feed_byte(self, message: "Message", input: int) -> "NMEA_State":
        if input == ord(b"$"):
            return HEADER
        return self


class Header(NMEA_State):
    def enter(self, message: "Message") -> "NMEA_State":
        message.reset()
        return self

    def feed_byte(self, message: "Message", input: int) -> "NMEA_State":
        if input == ord(b"$"):
            return HEADER
        size = message.body_append(input)
        if size == 5:
            return BODY
        return self


class Body(NMEA_State):
    def feed_byte(self, message: "Message", input: int) -> "NMEA_State":
        if input == ord(b"$"):
            return HEADER
        if input == ord(b"*"):
            return CHECKSUM
        size = message.body_append(input)
        return self


class Checksum(NMEA_State):
    def feed_byte(self, message: "Message", input: int) -> "NMEA_State":
        if input == ord(b"$"):
            return HEADER
        if input in {ord(b"\n"), ord(b"\r")}:
            # Incomplete checksum... Will be invalid.
            return END
        size = message.checksum_append(input)
        if size == 2:
            return END
        return self


class End(NMEA_State):
    def feed_byte(self, message: "Message", input: int) -> "NMEA_State":
        if input == ord(b"$"):
            return HEADER
        elif input not in {ord(b"\n"), ord(b"\r")}:
            return WAITING
        return self

    def valid(self, message: "Message") -> bool:
        return message.valid


WAITING = Waiting()
HEADER = Header()
BODY = Body()
CHECKSUM = Checksum()
END = End()


class Message:
    def __init__(self) -> None:
        self.body = bytearray(80)
        self.checksum_source = bytearray(2)
        self.body_len = 0
        self.checksum_len = 0
        self.checksum_computed = 0

    def reset(self) -> None:
        self.body_len = 0
        self.checksum_len = 0
        self.checksum_computed = 0

    def body_append(self, input: int) -> int:
        self.body[self.body_len] = input
        self.body_len += 1
        self.checksum_computed ^= input
        return self.body_len

    def checksum_append(self, input: int) -> int:
        self.checksum_source[self.checksum_len] = input
        self.checksum_len += 1
        return self.checksum_len

    @property
    def valid(self) -> bool:
        return (
            self.checksum_len == 2
            and int(self.checksum_source, 16) == self.checksum_computed
        )

    def header(self) -> bytes:
        return bytes(self.body[:5])

    def fields(self) -> list[bytes]:
        return bytes(self.body[: self.body_len]).split(b",")

    def __repr__(self) -> str:
        body = self.body[: self.body_len]
        checksum = self.checksum_source[: self.checksum_len]
        return f"Message({body}, {checksum}, computed={self.checksum_computed:02x})"

    def message(self) -> bytes:
        return (
            b"$"
            + bytes(self.body[: self.body_len])
            + b"*"
            + bytes(self.checksum_source[: self.checksum_len])
        )


class Reader:
    def __init__(self) -> None:
        self.buffer = Message()
        self.state: NMEA_State = WAITING

    def read(self, source: Iterable[bytes]) -> Iterator[Message]:
        for byte in source:
            new_state = self.state.feed_byte(self.buffer, cast(int, byte))
            if self.buffer.valid:
                yield self.buffer
                self.buffer = Message()
                new_state = WAITING
            if new_state != self.state:
                # self.state.exit()  # A common extension
                new_state.enter(self.buffer)
                self.state = new_state


test_reader = """
>>> message = b'''
... $GPGGA,161229.487,3723.2475,N,12158.3416,W,1,07,1.0,9.0,M,,,,0000*18
... $GPGLL,3723.2475,N,12158.3416,W,161229.487,A,A*41
... '''
>>> rdr = Reader()
>>> result = list(rdr.read(message))
>>> result
[Message(bytearray(b'GPGGA,161229.487,3723.2475,N,12158.3416,W,1,07,1.0,9.0,M,,,,0000'), bytearray(b'18'), computed=18), Message(bytearray(b'GPGLL,3723.2475,N,12158.3416,W,161229.487,A,A'), bytearray(b'41'), computed=41)]
>>> result[0].message()
b'$GPGGA,161229.487,3723.2475,N,12158.3416,W,1,07,1.0,9.0,M,,,,0000*18'
>>> result[1].message()
b'$GPGLL,3723.2475,N,12158.3416,W,161229.487,A,A*41'
>>> result[0].fields()
[b'GPGGA', b'161229.487', b'3723.2475', b'N', b'12158.3416', b'W', b'1', b'07', b'1.0', b'9.0', b'M', b'', b'', b'', b'0000']
>>> result[1].fields()
[b'GPGLL', b'3723.2475', b'N', b'12158.3416', b'W', b'161229.487', b'A', b'A']

"""


__test__ = {name: case for name, case in globals().items() if name.startswith("test_")}
