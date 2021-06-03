
# Case Study for Chapter 3, When Objects Are Alike

## Logical View

## The Strategy Design Pattern

```python

>>> from math import isclose
>>> from model import TrainingKnownSample, UnknownSample, Chebyshev

>>> s1 = TrainingKnownSample(
...     sepal_length=5.1, sepal_width=3.5, petal_length=1.4, petal_width=0.2, species="Iris-setosa")
>>> u = UnknownSample(**{"sepal_length": 7.9, "sepal_width": 3.2, "petal_length": 4.7, "petal_width": 1.4})

>>> algorithm = Chebyshev()
>>> isclose(3.3, algorithm.distance(s1, u))
True

```

## The Minkowski Solution

```python

>>> from math import isclose
>>> from model import TrainingKnownSample, UnknownSample, Euclidean

>>> s1 = TrainingKnownSample(
...     sepal_length=5.1, sepal_width=3.5, petal_length=1.4, petal_width=0.2, species="Iris-setosa")
>>> u = UnknownSample(**{"sepal_length": 7.9, "sepal_width": 3.2, "petal_length": 4.7, "petal_width": 1.4})

>>> algorithm = Euclidean()
>>> isclose(4.50111097, algorithm.distance(s1, u))
True

```

## One More Example

## Another Strategy

```python

>>> from model import TrainingKnownSample, UnknownSample, Minkowski_2

>>> class CD(Minkowski_2):
...     m = 1
...     reduction = max

>>> class MD(Minkowski_2):
...     m = 1
...     reduction = sum

>>> class ED(Minkowski_2):
...     m = 2
...     reduction = sum

```

## Type Hints for Minkowski_2

