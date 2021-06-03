# Python 3 Object-Oriented Programming Case Study

Chapter 5, When to Use Object-Oriented Programming

## Treat objects as objects

```python

>>> square = [(1,1), (1,2), (2,2), (2,1)]

>>> from math import hypot
>>> def distance(p_1, p_2):
...     return hypot(p_1[0]-p_2[0], p_1[1]-p_2[1])
>>> def perimeter(polygon):
...     pairs = zip(polygon, polygon[1:]+polygon[:1])
...     return sum(
...         distance(p1, p2) for p1, p2 in pairs
...     )

>>> perimeter(square)
4.0

```

## Adding behaviors to class data with properties

## Manager objects
