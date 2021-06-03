"""
Python 3 Object-Oriented Programming 4th ed.

Chapter 3, When Objects Are Alike.
"""
from __future__ import annotations
from typing import Optional, Protocol, Any

## Extending built-ins


class ContactList(list["Contact"]):
    def search(self, name: str) -> list["Contact"]:
        """All contacts with search name in name."""
        matching_contacts: list["Contact"] = []
        for contact in self:
            if name in contact.name:
                matching_contacts.append(contact)
        return matching_contacts


class Contact:
    all_contacts = ContactList()

    def __init__(self, /, name: str = "", email: str = "", **kwargs: Any) -> None:
        super().__init__(**kwargs)  # type: ignore [call-arg]
        self.name = name
        self.email = email
        self.all_contacts.append(self)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(" f"{self.name!r}, {self.email!r}" f")"


test_search = """
>>> Contact.all_contacts = ContactList()

>>> c1 = Contact("John A", "johna@example.net")
>>> c2 = Contact("John B", "johnb@sloop.net")
>>> c3 = Contact("Jenna C", "cutty@sark.io")
>>> [c.name for c in Contact.all_contacts.search('John')]
['John A', 'John B']
"""


## Multiple inheritance -- working version


class AddressHolder:
    def __init__(
        self,
        /,
        street: str = "",
        city: str = "",
        state: str = "",
        code: str = "",
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)  # type: ignore [call-arg]
        self.street = street
        self.city = city
        self.state = state
        self.code = code


class Friend(Contact, AddressHolder):
    def __init__(self, /, phone: str = "", **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.phone = phone


test_friend = """
>>> knave = Friend(
...     name="Knave", 
...     email="knave@multi.com", 
...     phone="555-1313", 
...     street="1212 DogCow Loop", 
...     city="W. Larsen", 
...     state="MA", 
...     code="12345")
>>> knave.phone
'555-1313'
>>> knave.state
'MA'
"""

test_bad_friend = """
>>> cad = Friend(
...     name="Cad", 
...     email="cad@multi.com", 
...     phone="555-1414", 
...     street="1111 Tarot Deck", 
...     city="W. Waite-Rider", 
...     state="MA", 
...     code="12345",
...     extra="This will raise an exception")
Traceback (most recent call last):
  File ...
    exec(compile(example.source, filename, "single",
  File "<doctest commerce.__test__.test_bad_friend[0]>", line 1, in <module>
    cad = Friend(
  File "src/commerce.py", line 67, in __init__
    super().__init__(**kwargs)
  File "src/commerce.py", line 25, in __init__
    super().__init__(**kwargs)  # type: ignore [call-arg]
  File "src/commerce.py", line 58, in __init__
    super().__init__(**kwargs)  # type: ignore [call-arg]
TypeError: object.__init__() takes exactly one argument (the instance to initialize)

"""


__test__ = {name: case for name, case in globals().items() if name.startswith("test_")}
