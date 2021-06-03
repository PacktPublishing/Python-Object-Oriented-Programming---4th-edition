# Case Study for Chapter Ten, The Iterator Pattern

## Multiple Partitions

```python
>>> import itertools

>>> p1 = range(1, 10, 2)
>>> p2 = range(2, 10, 2)
>>> itertools.chain(p1, p2)
<itertools.chain object at ...>

>>> list(itertools.chain(p1, p2))
[1, 3, 5, 7, 9, 2, 4, 6, 8]

```

## Testing

## K-NN Altenative `bisect`

## K-NN Alternative `heapq`

## Conclusion

```python

>>> import timeit

>>> m = timeit.timeit(
...     "manhattan(d1, d2)",
...     """
... from model import Sample, KnownSample, TrainingKnownSample, TestingKnownSample
... from model import manhattan, euclidean
... d1 = TrainingKnownSample(KnownSample(Sample(1, 2, 3, 4), "x"))
... d2 = KnownSample(Sample(2, 3, 4, 5), "y")
... """)

>>> e = timeit.timeit(
...     "euclidean(d1, d2)",
...     """
... from model import Sample, KnownSample, TrainingKnownSample, TestingKnownSample
... from model import manhattan, euclidean
... d1 = TrainingKnownSample(KnownSample(Sample(1, 2, 3, 4), "x"))
... d2 = KnownSample(Sample(2, 3, 4, 5), "y")
... """)

>>> print(f"Manhattan: {m:.3f}")
Manhattan: ...
>>> print(f"Euclidean: {e:.3f}")
Euclidean: ...

```
