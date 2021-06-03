
# Case Study for Chapter 5, When to Use Object-Oriented Programming

## Input Validation

## Input Partitioning

## The Sample Class Hierarchy

## The Purpose Enumeration

```python
>>> from model import KnownSample, Purpose
>>> s2 = KnownSample(
...     sepal_length=5.1, 
...     sepal_width=3.5, 
...     petal_length=1.4, 
...     petal_width=0.2, 
...     species="Iris-setosa", 
...     purpose=Purpose.Testing.value)
>>> s2
KnownSample(sepal_length=5.1, sepal_width=3.5, petal_length=1.4, petal_width=0.2, purpose=1, species='Iris-setosa')
>>> s2.classification is None
True

```

## Property Setters

## Repeated If Statements

## Context Managers

