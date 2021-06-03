"""
Python 3 Object-Oriented Programming Case Study

Chapter 7.
"""
from __future__ import annotations
import collections
from dataclasses import dataclass, asdict
from typing import Optional, Counter, List
import weakref
import sys


@dataclass
class Sample:
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float


@dataclass
class KnownSample(Sample):
    species: str


@dataclass
class TestingKnownSample(KnownSample):
    classification: Optional[str] = None


@dataclass
class TrainingKnownSample(KnownSample):
    """Cannot be classified -- there's no classification instance variable available."""

    pass


@dataclass
class UnknownSample(Sample):
    classification: Optional[str] = None


class Distance:
    """Abstact definition of a distance computation"""

    def distance(self, s1: Sample, s2: Sample) -> float:
        raise NotImplementedError


@dataclass
class Hyperparameter:
    """A specific tuning parameter set with k and a distance algorithm"""

    k: int
    algorithm: Distance
    data: weakref.ReferenceType["TrainingData"]

    def classify(self, sample: Sample) -> str:
        """The k-NN algorithm"""
        if not (training_data := self.data()):
            raise RuntimeError("No TrainingData object")
        distances: list[tuple[float, TrainingKnownSample]] = sorted(
            (self.algorithm.distance(sample, known), known)
            for known in training_data.training
        )
        k_nearest = (known.species for d, known in distances[: self.k])
        frequency: Counter[str] = collections.Counter(k_nearest)
        best_fit, *others = frequency.most_common()
        species, votes = best_fit
        return species


@dataclass
class TrainingData:
    testing: List[TestingKnownSample]
    training: List[TrainingKnownSample]
    tuning: List[Hyperparameter]


# Special case, we don't *often* test abstract superclasses.
# In this example, however, we can create instances of the abstract class.
test_Sample = """
>>> x = Sample(1, 2, 3, 4)
>>> x
Sample(sepal_length=1, sepal_width=2, petal_length=3, petal_width=4)
"""

test_TrainingKnownSample = """
>>> s1 = TrainingKnownSample(
...     sepal_length=5.1, sepal_width=3.5, petal_length=1.4, petal_width=0.2, species="Iris-setosa")
>>> s1
TrainingKnownSample(sepal_length=5.1, sepal_width=3.5, petal_length=1.4, petal_width=0.2, species='Iris-setosa')

# This is undesirable...

>>> s1.sepal_length = 0 
>>> s1
TrainingKnownSample(sepal_length=0, sepal_width=3.5, petal_length=1.4, petal_width=0.2, species='Iris-setosa')

# This makes duplicate detection awkward...

>>> hash(s1)
Traceback (most recent call last):
...
TypeError: unhashable type: 'TrainingKnownSample'

"""

test_TestingKnownSample = """
>>> s2 = TestingKnownSample(
...     sepal_length=5.1, sepal_width=3.5, petal_length=1.4, petal_width=0.2, species="Iris-setosa")
>>> s2
TestingKnownSample(sepal_length=5.1, sepal_width=3.5, petal_length=1.4, petal_width=0.2, species='Iris-setosa', classification=None)

# This is more expected...

>>> s2.classification = "wrong"
>>> s2
TestingKnownSample(sepal_length=5.1, sepal_width=3.5, petal_length=1.4, petal_width=0.2, species='Iris-setosa', classification='wrong')
"""

test_UnknownSample = """
>>> u = UnknownSample(sepal_length=5.1, sepal_width=3.5, petal_length=1.4, petal_width=0.2, classification=None)
>>> u
UnknownSample(sepal_length=5.1, sepal_width=3.5, petal_length=1.4, petal_width=0.2, classification=None)
"""


__test__ = {name: case for name, case in globals().items() if name.startswith("test_")}
