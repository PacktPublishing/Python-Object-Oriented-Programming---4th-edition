"""
Python 3 Object-Oriented Programming 4th ed.

Chapter 2, Objects in Python.
"""
from __future__ import annotations
from typing import Optional, Any


class Database:
    """The Database Implementation"""

    def __init__(self, connection: Optional[str] = None) -> None:
        """Create a connection to a database."""
        self.connection = connection

    def fetch(self, key: str) -> dict[str, Any]:
        return {"key": key}


db: Optional[Database] = None


def initialize_database(connection: Optional[str] = None) -> None:
    global db
    db = Database(connection)
    # print(f"initialized {db!r} with {connection!r}")


def get_database(connection: Optional[str] = None) -> Database:
    global db
    if not db:
        db = Database(connection)
        # print(f"initialized {db!r} with {connection!r}")
    return db


class Query:
    """A place-holder for a more sophistcated Query object."""

    def __init__(self, database: Database, collection: str) -> None:
        """Create a query for a database"""
        pass
