# Python 3 Object-Oriented Programming

Chapter 8. The Intersection of Object-Oriented and Functional Programming

## Python built-in functions

### The len() function

```python
>>> len([1, 2, 3, 4])
4

```

### The reversed() function

```python
>>> class CustomSequence:
...     def __init__(self, args):
...         self._list = args
...     def __len__(self):
...         return 5
...     def __getitem__(self, index):
...         return f"x{index}"

>>> class FunkyBackwards(list):
...     def __reversed__(self):
...         return "BACKWARDS!"

>>> generic = [1, 2, 3, 4, 5]
>>> custom = CustomSequence([6, 7, 8, 9, 10])
>>> funkadelic = FunkyBackwards([11, 12, 13, 14, 15])

>>> for sequence in generic, custom, funkadelic:
...     print(f"{sequence.__class__.__name__}: ", end="")
...     for item in reversed(sequence):
...         print(f"{item}, ", end="")
...     print()
list: 5, 4, 3, 2, 1, 
CustomSequence: x4, x3, x2, x1, x0, 
FunkyBackwards: B, A, C, K, W, A, R, D, S, !, 

```

### The enumerate() function

```python
>>> from pathlib import Path
>>> with Path("docs/sample_data.md").open() as source:
...     for index, line in enumerate(source, start=1):
...         print(f"{index:3d}: {line.rstrip()}")
  1: # Python 3 Object-Oriented Programming
  2: 
  3: Chapter 8. The Intersection of Object-Oriented and Functional Programming
  4: 
  5: Some sample data to show how the `enumerate()` function works.

```

## An alternative to method overloading

```python
>>> def no_args():
...     return "Hello, world!"

>>> no_args()
'Hello, world!'

>>> def no_args() -> str:
...     return "Hello, world!"

```

```python
>>> def mandatory_args(x, y, z): 
...     return f"{x=}, {y=}, {z=}"

>>> a_variable = 42
>>> mandatory_args("a string", a_variable, True)
"x='a string', y=42, z=True"

>>> from typing import Any
>>> def mandatory_args(x: Any, y: Any, z: Any) -> str: 
...     return f"{x=}, {y=}, {z=}"

```


### Default values for parameters

```python
>>> from typing import Optional

>>> def better_function(x: Optional[int] = None) -> str:
...     if x is None:
...         x = number
...     return f"better: {x=}, {number=}"

>>> number = 5
>>> better_function(42)
'better: x=42, number=5'

>>> number = 7
>>> better_function()
'better: x=7, number=7'

```

```python
>>> def better_function_2(x: Optional[int] = None) -> str:
...     x = number if x is None else x
...     return f"better: {x=}, {number=}"

>>> number = 5
>>> better_function_2(42)
'better: x=42, number=5'

>>> number = 7
>>> better_function_2()
'better: x=7, number=7'

```

### Unpacking arguments

```python
>>> def show_args(arg1, arg2, arg3="THREE"): 
...     return f"{arg1=}, {arg2=}, {arg3=}" 
 
Unpacking a sequence 

>>> some_args = range(3) 
>>> show_args(*some_args)
'arg1=0, arg2=1, arg3=2'


Unpacking a dict

>>> more_args = { 
...        "arg1": "ONE", 
...        "arg2": "TWO"}
>>> show_args(**more_args)
"arg1='ONE', arg2='TWO', arg3='THREE'"


```

```python

>>> x = {'a': 1, 'b': 2}
>>> y = {'b': 11, 'c': 3}
>>> z = {**x, **y}
>>> z
{'a': 1, 'b': 11, 'c': 3}

```

## Functions are objects, too

See Chapter 3 for details

```python
>>> from typing import Callable
>>> def fizz(x: int) -> bool:
...     return x % 3 == 0
>>> def buzz(x: int) -> bool:
...     return x % 5 == 0
>>> def name_or_number(number: int, *tests: Callable[[int], bool]) -> None:
...     for t in tests:
...         if t(number):
...             return t.__name__
...     return str(number)

>>> name_or_number(1, fizz)
'1'
>>> name_or_number(3, fizz)
'fizz'
>>> name_or_number(5, fizz)
'5'
>>> name_or_number(5, fizz, buzz)
'buzz'

>>> for i in range(1, 11):
...     print(name_or_number(i, fizz, buzz))
1
2
fizz
4
buzz
fizz
7
8
fizz
buzz

```


### Using functions to patch a class

```python

>>> class A:
...     def show_something(self):
...         print("My class is A")

>>> a_object = A()
>>> a_object.show_something()
My class is A


>>> def patched_show_something():
...     print("My class is NOT A")

>>> a_object.show_something = patched_show_something
>>> a_object.show_something()
My class is NOT A

>>> b_object = A()
>>> b_object.show_something()
My class is A


```

## File I/O

```python
>>> contents = "Some file contents\n"
>>> file = open("filename.txt", "w")
>>> n = file.write(contents)
>>> file.close()

>>> assert Path("filename.txt").read_text() == contents
>>> Path("filename.txt").unlink()

```

```python

>>> source_path = Path("requirements.txt")
>>> with source_path.open() as source_file:
...     for line in source_file:
...         print(line, end='')
<BLANKLINE>
beautifulsoup4==4.9.1
jsonschema==3.2.0
pyyaml==5.3.1
pillow==8.0.1


```

### Placing it in context

```python
>>> class StringJoiner(list): 
...     def __enter__(self): 
...         return self 
...     def __exit__(self, type, value, tb): 
...         self.result = "".join(self) 

>>> with StringJoiner("Hello") as sj:
...     sj.append(", ")
...     sj.extend("world")
...     sj.append("!")
>>> sj.result
'Hello, world!'

>>> with StringJoiner("Partial") as sj:
...     sj.append(" ")
...     sj.extend("Results")
...     sj.append(str(2 / 0))
...     sj.extend("Even If There's an Exception")
Traceback (most recent call last):
  ...
  File "<doctest examples.md[60]>", line 3, in <module>
    sj.append(str(2 / 0))
ZeroDivisionError: division by zero
>>> sj.result
'Partial Results'


```
