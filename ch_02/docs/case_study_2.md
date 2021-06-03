
# Case Study for Chapter 2, Objects in Python

## Logical View

## Samples and Their States

## Sample State Transitions

```python
>>> from model import Sample
>>> s2 = Sample(
...     sepal_length=5.1, sepal_width=3.5, petal_length=1.4, petal_width=0.2, species="Iris-setosa")
>>> s2
KnownSample(sepal_length=5.1, sepal_width=3.5, petal_length=1.4, petal_width=0.2, species='Iris-setosa')
>>> s2.classification = "wrong"
>>> s2
KnownSample(sepal_length=5.1, sepal_width=3.5, petal_length=1.4, petal_width=0.2, species='Iris-setosa', classification='wrong')

```

## The Hyperparameter Class

```python

>>> class TrainingData:
...     pass
>>> td_1 = TrainingData()

```

```python

>>> from weakref import ref
>>> b = ref(td_1)

```

```python

>>> type(b)
<class 'weakref'>

```

```python

>>> b() == td_1
True

```

```python

>>> del td_1
>>> b() is None
True

```

## Responsibilities

## The Training Data Class

