# Python 3 Object-Oriented Programming 4th ed.

Chapter 3, When Objects Are Alike

## Basic inheritance

```python
>>> from typing import List
>>> class Contact:
...    all_contacts: List["Contact"] = []
...    def __init__(self, name: str, email: str) -> None:
...        self.name = name
...        self.email = email
...        Contact.all_contacts.append(self)
...    def __repr__(self) -> str:
...        return (
...            f"{self.__class__.__name__}("
...            f"{self.name!r}, {self.email!r}"
...            f")"
...       )
...
>>> c_1 = Contact("Dusty", "dusty@example.com")
>>> c_2 = Contact("Steve", "steve@itmaybeahack.com")
>>> Contact.all_contacts
[Contact('Dusty', 'dusty@example.com'), Contact('Steve', 'steve@itmaybeahack.com')]


>>> class Supplier(Contact):
...    def order(self, order: "Order") -> None:
...        print(
...            "If this were a real system we would send "
...            f"'{order}' order to '{self.name}'"
...        )
...


>>> c = Contact("Some Body", "somebody@example.net")
>>> s = Supplier("Sup Plier", "supplier@example.net")
>>> print(c.name, c.email, s.name, s.email)
Some Body somebody@example.net Sup Plier supplier@example.net

>>> from pprint import pprint
>>> pprint(c.all_contacts)
[Contact('Dusty', 'dusty@example.com'),
 Contact('Steve', 'steve@itmaybeahack.com'),
 Contact('Some Body', 'somebody@example.net'),
 Supplier('Sup Plier', 'supplier@example.net')]

>>> c.order("I need pliers")
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: 'Contact' object has no attribute 'order'
>>> s.order("I need pliers")
If this were a real system we would send 'I need pliers' order to 'Sup Plier'


```

### Extending built-ins

```python
>>> [] == list()
True

```

```python

>>> CL_2 = list["Contact"]
>>> type(CL_2)
<class 'types.GenericAlias'>

```

### Overriding and super

```python
>>> class Friend(Contact):
...     def __init__(self, name: str, email: str, phone: str) -> None:
...         self.name = name
...         self.email = email
...         self.phone = phone

```

## Multiple inheritance

### The Diamond Problem

## Polymorphism

## Case Study

```python

>>> from typing import Iterable
>>> class SumPow:
...     def __call__(self, sequence: Iterable[float], p: float=1.0) -> float:
...         return sum(x**p for x in sequence)
        
>>> sum_pow = SumPow()
>>> distances=[3.0, 1.0, 2.0, 3.0]
>>> sum_pow(distances)
9.0
>>> sum_pow(distances, 2)
23.0
>>> sum_pow([2.5, 2.5], 2) == 12.5
True

```
