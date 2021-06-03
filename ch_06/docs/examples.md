# Python 3 Object-Oriented Programming

Chapter 6. Abstract Base Classes and Operator Overloading


## Abstract base classes

### Creating an abstract base class

### The abs's of collections

```python
>>> from collections.abc import Container 
>>> Container.__abstractmethods__ == frozenset({'__contains__'})
True

```

### ABC's and type hints

## The collections.anc module 

```python
>>> x = dict({"a": 42, "b": 7, "c": 6})
>>> y = dict([("a", 42), ("b", 7), ("c", 6)])
>>> x == y
True

```

## Creating your own abstract base class

### Operator overloading

```python
>>> from pathlib import PurePosixPath
>>> home = PurePosixPath("/Users/slott")
>>> home / "miniconda3" / "envs"  # doctest: +ELLIPSIS
PurePosixPath('.../miniconda3/envs')

```

### Extending built-ins

```python
>>> d = {"a": 42, "a": 3.14}
>>> d
{'a': 3.14}

>>> {1: "one", True: "true"}
{1: 'true'}

```


```python
>>> from typing import Dict, Hashable, Any, Mapping, Iterable
>>> class NoDupDict(Dict[Hashable, Any]):
...     def __setitem__(self, key, value) -> None:
...         if key in self:
...             raise ValueError(f"duplicate {key!r}")
...         super().__setitem__(key, value)
...     def __init__(self, init=None, **kwargs) -> None:
...         if isinstance(init, Mapping):
...             for k, v in init.items():
...                 self[k] = v
...         elif isinstance(init, Iterable):
...             for k, v in init:
...                 self[k] = v
...         elif init is None:
...             super().__init__(**kwargs)
...         else:
...             super().__init__(init, **kwargs)

>>> nd = NoDupDict()
>>> nd["a"] = 1
>>> nd["a"] = 2
Traceback (most recent call last):
  ...
  File "<doctest examples.md[10]>", line 1, in <module>
    nd["a"] = 2
  File "<doctest examples.md[7]>", line 4, in __setitem__
    raise ValueError(f"duplicate {key!r}")
ValueError: duplicate 'a'

Doesn't work -- Arguments created a standard dict first

>>> NoDupDict({"a": 42, "a": 3.14})
{'a': 3.14}

>>> NoDupDict([("a", 42), ("a", 3.14)])
Traceback (most recent call last):
  ...
  File "<doctest examples.md[10]>", line 1, in <module>
    nd["a"] = 2
  File "<doctest examples.md[7]>", line 4, in __setitem__
    raise ValueError(f"duplicate {key!r}")
ValueError: duplicate 'a'


```


```python
>>> class MC(type):
...     @classmethod
...     def __prepare__(cls, *args, **kwargs):
...         print(f"__prepare__({cls}, *{args}, **{kwargs})")
...         return type.__prepare__(cls, *args, **kwargs)
...     def __new__(cls, *args, **kwargs):
...         print(f"__new__(*{args}, **{kwargs})")
...         return type.__new__(cls, *args, **kwargs)
...     def __call__(self, *args, **kwargs):
...         print(f"__call__(*{args}, **{kwargs})")
...         return super().__call__(*args, **kwargs)

>>> class X(metaclass=MC):
...     def __init__(self, a):
...         self.a = a
__prepare__(<class '__main__.MC'>, *('X', ()), **{})
__new__(*('X', (), {'__module__': '__main__', '__qualname__': 'X', '__init__': <function X.__init__ at ...>}), **{})

>>> x = X(42)
__call__(*(42,), **{})

```

## Demystifying the magic

```python

>>> import abc
>>> abc.ABCMeta.__mro__
(<class 'abc.ABCMeta'>, <class 'type'>, <class 'object'>)


```
