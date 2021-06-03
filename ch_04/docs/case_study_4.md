
# Case Study for Chapter 4, Expecting the Unexpected

## Context View

## Processing View

## What can go wrong?

### Bad behavior

## Creating samples from CSV files

```python
>>> row = {"sepal_length": "5.1", "sepal_width": "3.5",
...  "petal_length": "1.4", "petal_width": "0.2",
...  "species": "Iris-setosa"}

```

```python
>>> from model import TrainingKnownSample
>>> valid = {"sepal_length": "5.1", "sepal_width": "3.5",
...  "petal_length": "1.4", "petal_width": "0.2",
...  "species": "Iris-setosa"}

>>> rks = TrainingKnownSample.from_dict(valid)
>>> rks
TrainingKnownSample(sepal_length=5.1, sepal_width=3.5, petal_length=1.4, petal_width=0.2, species='Iris-setosa', )

```

```python
>>> from model import TestingKnownSample, InvalidSampleError
>>> invalid_species = {"sepal_length": "5.1", "sepal_width": "3.5",
...  "petal_length": "1.4", "petal_width": "0.2",
...  "species": "nothing known by this app"}

>>> eks = TestingKnownSample.from_dict(invalid_species)
Traceback (most recent call last):
...
model.InvalidSampleError: invalid species in {'sepal_length': '5.1', 'sepal_width': '3.5', 'petal_length': '1.4', 'petal_width': '0.2', 'species': 'nothing known by this app'}

```

### Enumerated values


```python
>>> from enum import Enum
>>> class Species(Enum):
...    Setosa = "Iris-setosa"
...    Versicolour = "Iris-versicolour"
...    Viginica = "Iris-virginica"

>>> Species("Iris-setosa")
<Species.Setosa: 'Iris-setosa'>

>>> Species("Iris-pinniped")
Traceback (most recent call last):
...
ValueError: 'Iris-pinniped' is not a valid Species

```

## Reading CSV files
