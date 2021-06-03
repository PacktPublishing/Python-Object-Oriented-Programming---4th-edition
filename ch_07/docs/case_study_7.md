
# Case Study for Chapter Seven, Python Data Structures

## Logical Model

```python

>>> from model import Sample
>>> x = Sample(1, 2, 3, 4)
>>> x
Sample(sepal_length=1, sepal_width=2, petal_length=3, petal_width=4)

```

```python

>>> from model import TrainingKnownSample
>>> s1 = TrainingKnownSample(
...     sepal_length=5.1, sepal_width=3.5, petal_length=1.4, petal_width=0.2, species="Iris-setosa")
>>> s1
TrainingKnownSample(sepal_length=5.1, sepal_width=3.5, petal_length=1.4, petal_width=0.2, species='Iris-setosa')

# This is undesirable...
>>> s1.classification = "wrong"
>>> s1
TrainingKnownSample(sepal_length=5.1, sepal_width=3.5, petal_length=1.4, petal_width=0.2, species='Iris-setosa')
>>> s1.classification
'wrong'

```

## Frozen Dataclasses

```python
>>> from model_f import TrainingKnownSample, KnownSample
>>> s1 = TrainingKnownSample(
...     sample=KnownSample(
...         sepal_length=5.1, sepal_width=3.5, petal_length=1.4, petal_width=0.2, species="Iris-setosa"
...     )
... )
>>> s1
TrainingKnownSample(sample=KnownSample(sepal_length=5.1, sepal_width=3.5, petal_length=1.4, petal_width=0.2, species='Iris-setosa'))

```

```python
>>> s1.classification = "wrong"
Traceback (most recent call last):
... details omitted
dataclasses.FrozenInstanceError: cannot assign to field 'classification'

```

## NamedTuple classes

```python
>>> from model_t import TrainingKnownSample, KnownSample, Sample
>>> s1 = TrainingKnownSample(
...     sample=KnownSample(
...         sample=Sample(sepal_length=5.1, sepal_width=3.5, petal_length=1.4, petal_width=0.2),
...         species="Iris-setosa"
...     ),
... )
>>> s1
TrainingKnownSample(sample=KnownSample(sample=Sample(sepal_length=5.1, sepal_width=3.5, petal_length=1.4, petal_width=0.2), species='Iris-setosa'))

>>> s1.classification = "wrong"
Traceback (most recent call last):
...
AttributeError: 'TrainingKnownSample' object has no attribute 'classification'

```

## Conclusion

