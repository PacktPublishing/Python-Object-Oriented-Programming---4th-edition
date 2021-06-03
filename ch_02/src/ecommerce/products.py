"""
Python 3 Object-Oriented Programming 4th ed.

Chapter 2, Objects in Python.
"""
import ecommerce.database as database

from .database import Database

from .database import Database as DB

from .database import Database, Query

from .contact.email import send_mail


class Product:
    def __init__(self, name: str) -> None:
        self.name = name
