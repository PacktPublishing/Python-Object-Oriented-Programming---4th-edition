"""
Python 3 Object-Oriented Programming

Chapter 13.  Testing Object-Oriented Programs.
"""
from __future__ import annotations
import datetime
from enum import Enum
import redis
import sys
from typing import Optional


class Status(str, Enum):
    CANCELLED = "CANCELLED"
    DELAYED = "DELAYED"
    ON_TIME = "ON TIME"


class FlightStatusTracker:
    def __init__(self) -> None:
        self.redis = redis.Redis(host="127.0.0.1", port=6379, db=0)

    def change_status(self, flight: str, status: Status) -> None:
        if not isinstance(status, Status):
            raise ValueError(f"{status!r} is not a valid Status")
        key = f"flightno:{flight}"
        now = datetime.datetime.now(tz=datetime.timezone.utc)
        value = f"{now.isoformat()}|{status.value}"
        self.redis.set(key, value)

    def get_status(
        self, flight: str
    ) -> tuple[Optional[datetime.datetime], Optional[Status]]:
        key = f"flightno:{flight}"
        value = self.redis.get(key)
        if value:
            text_timestamp, text_status = value.split("|")
            timestamp = datetime.datetime.fromisoformat(text_timestamp)
            status = Status(text_status)
            return timestamp, status
        return None, None


class FlightStatusTracker_Alt:
    def __init__(self, redis_instance: Optional[redis.Connection] = None) -> None:
        self.redis = (
            redis_instance
            if redis_instance
            else redis.Redis(host="127.0.0.1", port=6379, db=0)
        )


def demo() -> None:
    fst = FlightStatusTracker()
    fst.change_status("42", Status.ON_TIME)
    as_of, status = fst.get_status("42")
    print(as_of, status)


if __name__ == "__main__":
    demo()
