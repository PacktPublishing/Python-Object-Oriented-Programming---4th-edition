
# Case Study for Chapter Six, Abstract Base Classes (abc's) and Operator Overloading

## Design Patterns

## Smart List

## A Shuffling Strategy

```python
>>> import random
>>> from model import ShufflingSamplePartition
>>> from pprint import pprint
>>> data = [
...     {
...         "sepal_length": i + 0.1,
...         "sepal_width": i + 0.2,
...         "petal_length": i + 0.3,
...         "petal_width": i + 0.4,
...         "species": f"sample {i}",
...     }
...     for i in range(10)
... ]

>>> random.seed(42)
>>> ssp = ShufflingSamplePartition(data)
>>> pprint(ssp.testing)
[TestingKnownSample(sepal_length=0.1, sepal_width=0.2, petal_length=0.3, petal_width=0.4, species='sample 0', classification=None, ),
 TestingKnownSample(sepal_length=1.1, sepal_width=1.2, petal_length=1.3, petal_width=1.4, species='sample 1', classification=None, )]

```

```python
>>> from typing import Callable, Any, Iterable
>>> from functools import wraps
>>> def unsplit(method: Callable[..., Any]) -> Callable[..., Any]:
...     @wraps(method)
...     def concrete_unsplit_method(self, *arg, **kwarg):
...         self.split = None
...         return method(self, *arg, **kwarg)
...     return concrete_unsplit_method
...

```

```python
>>> from model import ShufflingSamplePartition, SampleDict
>>> class Extendable_SamplePartition(ShufflingSamplePartition):
...     @unsplit
...     def append(self, item: SampleDict) -> None:
...         super().append(item)
...     @unsplit
...     def extend(self, item_iterable: Iterable[SampleDict]) -> None:
...         super.extend(item_iterable)
...

```

```python
>>> samples = [
...        {
...            "sepal_length": i + 0.1,
...            "sepal_width": i + 0.2,
...            "petal_length": i + 0.3,
...            "petal_width": i + 0.4,
...            "species": f"sample {i}",
...        }
...        for i in range(10)
... ]
...
>>> x = Extendable_SamplePartition()
>>> x.append(samples[0])
>>> len(x.training)
0
>>> len(x.testing)
1
>>> x.append(samples[0])
>>> len(x.training)
1
>>> len(x.testing)
1

```

## An Incremental Strategy

## Polymorphism

## Duplicate Rejection

### Creating Our Own Collection

### Changes to the <code>DealingPartition</code> classes

