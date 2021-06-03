"""
Python 3 Object-Oriented Programming

Chapter 9. Strings and Serialization
"""


class Contact:
    def __init__(self, first: str, last: str) -> None:
        self.first = first
        self.last = last

    @property
    def full_name(self) -> str:
        return f"{self.first} {self.last}"


test_contact_1 = """
>>> import json
>>> c = Contact("Noriko", "Hannah")
>>> json.dumps(c.__dict__)
'{"first": "Noriko", "last": "Hannah"}'


"""


import json
from typing import Any


class ContactEncoder(json.JSONEncoder):
    def default(self, obj: Any) -> Any:
        if isinstance(obj, Contact):
            return {
                "__class__": "Contact",
                "first": obj.first,
                "last": obj.last,
                "full_name": obj.full_name,
            }
        return super().default(obj)


def decode_contact(json_object: Any) -> Any:
    if json_object.get("__class__") == "Contact":
        return Contact(json_object["first"], json_object["last"])
    else:
        return json_object


test_contact_2 = """
>>> import json
>>> c = Contact("Noriko", "Hannah")
>>> text = json.dumps(c, cls=ContactEncoder)
>>> text
'{"__class__": "Contact", "first": "Noriko", "last": "Hannah", "full_name": "Noriko Hannah"}'

>>> some_text = (
...     '{"__class__": "Contact", "first": "Milli", "last": "Dale", '
...     '"full_name": "Milli Dale"}'
... )
>>> c2 = json.loads(some_text, object_hook=decode_contact)
>>> c2.full_name
'Milli Dale'

"""

__test__ = {name: case for name, case in globals().items() if name.startswith("test_")}
