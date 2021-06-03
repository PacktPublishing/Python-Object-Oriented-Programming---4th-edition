# Python 3 Object-Oriented Programming

Chapter 11. Common Design Patterns

# Decorator

```python
>>> from math import factorial
>>> def binom(n: int, k: int) -> int:
...     return factorial(n) // (factorial(k) * factorial(n-k))

>>> f"6-card deals: {binom(52, 6):,d}"
'6-card deals: 20,358,520'

>>> from math import factorial
>>> from functools import lru_cache

>>> @lru_cache(64)
... def binom(n: int, k: int) -> int:
...     return factorial(n) // (factorial(k) * factorial(n-k))

>>> f"6-card deals: {binom(52, 6):,d}"
'6-card deals: 20,358,520'

```

# Observer

# Strategy

# Command

# State

# Singleton

```python

>>> class OneOnly: 
...     _singleton = None 
...     def __new__(cls, *args, **kwargs): 
...         if not cls._singleton: 
...             cls._singleton = super().__new__(cls, *args, **kwargs) 
...         return cls._singleton 

>>> o1 = OneOnly()
>>> o2 = OneOnly()
>>> o1 == o2
True
>>> id(o1) == id(o2)
True

```
