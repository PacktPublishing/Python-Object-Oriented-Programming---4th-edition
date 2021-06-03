"""
Python 3 Object-Oriented Programming Case Study

Chapter 14.  Concurrency
"""
from __future__ import annotations
import abc
import collections
from concurrent import futures
import csv
import datetime
from math import isclose, hypot
from pathlib import Path
from typing import (
    cast,
    Any,
    Optional,
    Union,
    Iterator,
    Iterable,
    Counter,
    Callable,
    Protocol,
    NamedTuple,
)


class Sample(NamedTuple):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float


class KnownSample(NamedTuple):
    sample: Sample
    species: str


class TestingKnownSample:
    def __init__(
        self, sample: KnownSample, classification: Optional[str] = None
    ) -> None:
        self.sample = sample
        self.classification = classification

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(sample={self.sample!r}, classification={self.classification!r})"

    def matches(self) -> bool:
        match = self.sample.species == self.classification
        # print(f"Match {self.sample.species} == {self.classification} -> {match}")
        return match


class TrainingKnownSample(NamedTuple):
    sample: KnownSample


class UnknownSample:
    def __init__(self, sample: Sample) -> None:
        self.sample = sample

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(sample={self.sample!r})"


class ClassifiedSample:
    """Created from a Sample provided by a User, and the results of classification."""

    def __init__(self, classification: str, unknown: UnknownSample) -> None:
        self.sepal_length = unknown.sample.sepal_length
        self.sepal_width = unknown.sample.sepal_width
        self.petal_length = unknown.sample.petal_length
        self.petal_width = unknown.sample.petal_width
        self.classification = classification

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"sepal_length={self.sepal_length}, "
            f"sepal_width={self.sepal_width}, "
            f"petal_length={self.petal_length}, "
            f"petal_width={self.petal_width}, "
            f"classification={self.classification!r}, "
            f")"
        )


class CSVIrisReader:
    """
    Attribute Information:
       1. sepal length in cm
       2. sepal width in cm
       3. petal length in cm
       4. petal width in cm
       5. class:
          -- Iris Setosa
          -- Iris Versicolour
          -- Iris Virginica

    Read from a file::

        reader = CSVIrisReader(some_path)
        for row in reader.data_reader():
            ks = KnownSample(sample=Sample(row["sepal_length"], row["sepal_width"], row["petal_length"], row["petal_width"]), species=row["species"])

    Read from shared memory::

        sm = SharedMemory("some_data")
    """

    header = [
        "sepal_length",  # in cm
        "sepal_width",  # in cm
        "petal_length",  # in cm
        "petal_width",  # in cm
        "species",  # Iris-setosa, Iris-versicolour, Iris-virginica
    ]

    def __init__(self, source: Path) -> None:
        self.source = source

    def data_iter(self) -> Iterator[dict[str, str]]:
        with self.source.open() as source_file:
            reader = csv.DictReader(source_file, self.header)
            yield from reader


class Distance(abc.ABC):
    """Definition of a distance computation"""

    @abc.abstractmethod
    def distance(self, s1: Sample, s2: Sample) -> float:
        ...


class ED(Distance):
    def distance(self, s1: Sample, s2: Sample) -> float:
        return hypot(
            s1.sepal_length - s2.sepal_length,
            s1.sepal_width - s2.sepal_width,
            s1.petal_length - s2.petal_length,
            s1.petal_width - s2.petal_width,
        )


class MD(Distance):
    def distance(self, s1: Sample, s2: Sample) -> float:
        return sum(
            [
                abs(s1.sepal_length - s2.sepal_length),
                abs(s1.sepal_width - s2.sepal_width),
                abs(s1.petal_length - s2.petal_length),
                abs(s1.petal_width - s2.petal_width),
            ]
        )


class CD(Distance):
    def distance(self, s1: Sample, s2: Sample) -> float:
        return max(
            [
                abs(s1.sepal_length - s2.sepal_length),
                abs(s1.sepal_width - s2.sepal_width),
                abs(s1.petal_length - s2.petal_length),
                abs(s1.petal_width - s2.petal_width),
            ]
        )


class SD(Distance):
    def distance(self, s1: Sample, s2: Sample) -> float:
        return sum(
            [
                abs(s1.sepal_length - s2.sepal_length),
                abs(s1.sepal_width - s2.sepal_width),
                abs(s1.petal_length - s2.petal_length),
                abs(s1.petal_width - s2.petal_width),
            ]
        ) / sum(
            [
                s1.sepal_length + s2.sepal_length,
                s1.sepal_width + s2.sepal_width,
                s1.petal_length + s2.petal_length,
                s1.petal_width + s2.petal_width,
            ]
        )


test_Mink1 = """
>>> s1 = TrainingKnownSample(
...     sample=KnownSample(
...         sample=Sample(
...             sepal_length=5.1, sepal_width=3.5, petal_length=1.4, petal_width=0.2), 
...         species="Iris-setosa")
...     )
>>> u = UnknownSample(
...    Sample(**{"sepal_length": 7.9, "sepal_width": 3.2, "petal_length": 4.7, "petal_width": 1.4})
... )

>>> isclose(3.3, CD().distance(s1.sample.sample, u.sample))
True
>>> isclose(4.50111097, ED().distance(s1.sample.sample, u.sample))
True
>>> isclose(7.6, MD().distance(s1.sample.sample, u.sample))
True
>>> isclose(0.2773722627, SD().distance(s1.sample.sample, u.sample))
True

"""


class Chebyshev(Distance):
    """
    Computes the Chebyshev distance between two samples.

    ::

        >>> from math import isclose
        >>> from model import TrainingKnownSample, UnknownSample, Chebyshev

        >>> s1 = TrainingKnownSample(
        ...     sample=KnownSample(
        ...         sample=Sample(sepal_length=5.1, sepal_width=3.5, petal_length=1.4, petal_width=0.2),
        ...         species="Iris-setosa"
        ...     )
        ... )
        >>> u = UnknownSample(
        ...     Sample(**{"sepal_length": 7.9, "sepal_width": 3.2,
        ...        "petal_length": 4.7, "petal_width": 1.4})
        ... )

        >>> algorithm = Chebyshev()
        >>> isclose(3.3, algorithm.distance(s1.sample.sample, u.sample))
        True

    """

    def distance(self, s1: Sample, s2: Sample) -> float:
        return max(
            [
                abs(s1.sepal_length - s2.sepal_length),
                abs(s1.sepal_width - s2.sepal_width),
                abs(s1.petal_length - s2.petal_length),
                abs(s1.petal_width - s2.petal_width),
            ]
        )


class Minkowski(Distance):
    """An abstraction to provide a way to implement Manhattan and Euclidean."""

    @property
    @abc.abstractmethod
    def m(self) -> int:
        ...

    def distance(self, s1: Sample, s2: Sample) -> float:
        return (
            sum(
                [
                    abs(s1.sepal_length - s2.sepal_length) ** self.m,
                    abs(s1.sepal_width - s2.sepal_width) ** self.m,
                    abs(s1.petal_length - s2.petal_length) ** self.m,
                    abs(s1.petal_width - s2.petal_width) ** self.m,
                ]
            )
            ** (1 / self.m)
        )


class Euclidean(Minkowski):
    m = 2


class Manhattan(Minkowski):
    m = 1


class Sorensen(Distance):
    def distance(self, s1: Sample, s2: Sample) -> float:
        return sum(
            [
                abs(s1.sepal_length - s2.sepal_length),
                abs(s1.sepal_width - s2.sepal_width),
                abs(s1.petal_length - s2.petal_length),
                abs(s1.petal_width - s2.petal_width),
            ]
        ) / sum(
            [
                s1.sepal_length + s2.sepal_length,
                s1.sepal_width + s2.sepal_width,
                s1.petal_length + s2.petal_length,
                s1.petal_width + s2.petal_width,
            ]
        )


test_similarity = """
>>> distances = [2.0, 3.0, 1.0, 3.0]
>>> max(distances) == 3.0
True
>>> sum(distances) == 9.0
True
"""


class Minkowski_2(Distance):
    """A generic way to implement Manhattan, Euclidean, and Chebyshev.

    ::

        >>> from math import isclose
        >>> from model import TrainingKnownSample, UnknownSample, Minkowski_2

        >>> class CD(Minkowski_2):
        ...     m = 1
        ...     reduction = max

        >>> s1 = TrainingKnownSample(
        ...     sample=KnownSample(
        ...         sample=Sample(sepal_length=5.1, sepal_width=3.5, petal_length=1.4, petal_width=0.2),
        ...         species="Iris-setosa"
        ...     )
        ... )
        >>> u = UnknownSample(Sample(**{"sepal_length": 7.9, "sepal_width": 3.2, "petal_length": 4.7, "petal_width": 1.4}))

        >>> algorithm = CD()
        >>> isclose(3.3, algorithm.distance(s1.sample.sample, u.sample))
        True

    """

    @property
    @abc.abstractmethod
    def m(self) -> int:
        ...

    @staticmethod
    # @abc.abstractstaticmethod
    def reduction(values: Iterable[float]) -> float:
        ...

    def distance(self, s1: Sample, s2: Sample) -> float:
        return (
            self.reduction(
                [
                    abs(s1.sepal_length - s2.sepal_length) ** self.m,
                    abs(s1.sepal_width - s2.sepal_width) ** self.m,
                    abs(s1.petal_length - s2.petal_length) ** self.m,
                    abs(s1.petal_width - s2.petal_width) ** self.m,
                ]
            )
            ** (1 / self.m)
        )


class CD2(Minkowski_2):
    m = 1

    @staticmethod
    def reduction(values: Iterable[float]) -> float:
        return max(values)


class MD2(Minkowski_2):
    m = 1

    @staticmethod
    def reduction(values: Iterable[float]) -> float:
        return sum(values)


class ED2(Minkowski_2):
    m = 2

    @staticmethod
    def reduction(values: Iterable[float]) -> float:
        return sum(values)


class ED2S(Minkowski_2):
    m = 2
    reduction = sum  # type: ignore [assignment]


class Hyperparameter:
    """A hyperparameter value and the overall quality of the classification."""

    def __init__(self, k: int, algorithm: "Distance", training: "TrainingData") -> None:
        self.k = k
        self.algorithm = algorithm
        self.data = training
        self.quality: Optional[float] = None

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"k={self.k}, algorithm={self.algorithm}, "
            f"data={self.data})"
        )

    def test(self) -> "Hyperparameter":
        """Run the entire test suite."""
        pass_count, fail_count = 0, 0
        for test_known in self.data.testing:
            test_known.classification = self.classify(test_known)
            if test_known.matches():
                pass_count += 1
            else:
                fail_count += 1
        self.quality = pass_count / (pass_count + fail_count)
        return self

    def classify(self, unknown: Union[UnknownSample, TestingKnownSample]) -> str:
        """The k-NN algorithm"""
        sample: Sample
        if isinstance(unknown, TestingKnownSample):
            sample = unknown.sample.sample
        else:
            sample = unknown.sample
        distances: list[tuple[float, TrainingKnownSample]] = sorted(
            (
                (
                    self.algorithm.distance(known.sample.sample, sample),
                    known,
                )
                for known in self.data.training
            ),
        )
        # print(distances[: self.k])
        k_nearest = (known.sample.species for d, known in distances[: self.k])
        frequency: Counter[str] = collections.Counter(k_nearest)
        best_fit, *others = frequency.most_common()
        # print(best_fit, others)
        species, votes = best_fit
        return species


class TrainingData:
    """A set of training data and testing data with methods to load and test the samples."""

    def __init__(self, name: str) -> None:
        self.name = name
        self.uploaded: datetime.datetime
        self.tested: datetime.datetime
        self.training: list[TrainingKnownSample] = []
        self.testing: list[TestingKnownSample] = []

    def load(self, raw_data_iter: Iterable[dict[str, str]]) -> None:
        """Extract TestingKnownSample and TrainingKnownSample from raw data"""
        for n, row in enumerate(raw_data_iter):
            ks = KnownSample(
                sample=Sample(
                    sepal_length=float(row["sepal_length"]),
                    sepal_width=float(row["sepal_width"]),
                    petal_length=float(row["petal_length"]),
                    petal_width=float(row["petal_width"]),
                ),
                species=row["species"],
            )
            if n % 5 == 0:
                test = TestingKnownSample(ks)
                self.testing.append(test)
                # print(test)
            else:
                train = TrainingKnownSample(ks)
                self.training.append(train)
                # print(train)
        self.uploaded = datetime.datetime.now(tz=datetime.timezone.utc)

    def classify(
        self, parameter: Hyperparameter, unknown: UnknownSample
    ) -> ClassifiedSample:
        return ClassifiedSample(
            classification=parameter.classify(unknown), unknown=unknown
        )


def grid_search_1() -> None:
    td = TrainingData("Iris")
    source_path = Path.cwd().parent / "bezdekiris.data"
    reader = CSVIrisReader(source_path)
    td.load(reader.data_iter())
    tuning_results: list[Hyperparameter] = []
    with futures.ProcessPoolExecutor(8) as workers:
        test_runs: list[futures.Future[Hyperparameter]] = []
        for k in range(1, 41, 2):
            for algo in ED(), MD(), CD(), SD():
                h = Hyperparameter(k, algo, td)
                test_runs.append(workers.submit(h.test))
        for f in futures.as_completed(test_runs):
            tuning_results.append(f.result())
    for result in tuning_results:
        print(
            f"{result.k:2d} {result.algorithm.__class__.__name__:2s}"
            f" {result.quality:.3f}"
        )


def load_and_tune(k: int, distance_algo: str) -> tuple[int, str, float]:
    """
    Variant 2:
    Build a TrainingData and Hyperparameter object from the source file
    and the parameters.
    Works for very small datasets, where the load time is minimal.
    Doesn't work for large datasets, where shared memory is required.
    """
    algo = eval(distance_algo)()
    td = TrainingData("Iris")
    source_path = Path.cwd().parent / "bezdekiris.data"
    reader = CSVIrisReader(source_path)
    td.load(reader.data_iter())
    h = Hyperparameter(k, algo, td)
    h.test()
    return k, distance_algo, cast(float, h.quality)


def grid_search_2() -> None:
    with futures.ProcessPoolExecutor(8) as workers:
        test_runs: list[futures.Future[tuple[int, str, float]]] = []
        for k in range(1, 41, 2):
            for algo in ED, MD, CD, SD:
                test_runs.append(workers.submit(load_and_tune, k, algo.__name__))
        for f in futures.as_completed(test_runs):
            k, algo_name, quality = f.result()
            print(f"{k:2d} {algo_name:2s} {quality:.3f}")


# Special case, we don't *often* test abstract superclasses.
# In this example, however, we can create instances of the abstract class.
test_Sample = """
>>> x = Sample(1, 2, 3, 4)
>>> x
Sample(sepal_length=1, sepal_width=2, petal_length=3, petal_width=4)
"""

test_TrainingKnownSample = """
>>> s1 = TrainingKnownSample(
...     sample=KnownSample(
...         sample=Sample(
...             sepal_length=5.1, sepal_width=3.5, petal_length=1.4, petal_width=0.2), 
...         species="Iris-setosa")
...     )
>>> s1
TrainingKnownSample(sample=KnownSample(sample=Sample(sepal_length=5.1, sepal_width=3.5, petal_length=1.4, petal_width=0.2), species='Iris-setosa'))
"""

test_TestingKnownSample = """
>>> s2 = TestingKnownSample(
...     sample=KnownSample(
...         sample=Sample(
...             sepal_length=5.1, sepal_width=3.5, petal_length=1.4, petal_width=0.2),
...         species="Iris-setosa")
...    )
>>> s2
TestingKnownSample(sample=KnownSample(sample=Sample(sepal_length=5.1, sepal_width=3.5, petal_length=1.4, petal_width=0.2), species='Iris-setosa'), classification=None)
>>> s2.classification = "wrong"
>>> s2
TestingKnownSample(sample=KnownSample(sample=Sample(sepal_length=5.1, sepal_width=3.5, petal_length=1.4, petal_width=0.2), species='Iris-setosa'), classification='wrong')
"""

test_UnknownSample = """
>>> u = UnknownSample(
...     sample=Sample(sepal_length=5.1, sepal_width=3.5, petal_length=1.4, petal_width=0.2)
... )
>>> u
UnknownSample(sample=Sample(sepal_length=5.1, sepal_width=3.5, petal_length=1.4, petal_width=0.2))
"""

test_ClassifiedSample = """
>>> u = UnknownSample(
...     sample=Sample(sepal_length=5.1, sepal_width=3.5, petal_length=1.4, petal_width=0.2)
... )
>>> c = ClassifiedSample(classification="Iris-setosa", unknown=u)
>>> c
ClassifiedSample(sepal_length=5.1, sepal_width=3.5, petal_length=1.4, petal_width=0.2, classification='Iris-setosa', )
"""

test_Chebyshev = """
>>> s1 = TrainingKnownSample(
...     sample=KnownSample(
...         sample=Sample(
...             sepal_length=5.1, sepal_width=3.5, petal_length=1.4, petal_width=0.2), 
...         species="Iris-setosa")
...    )
>>> u = UnknownSample(Sample(**{"sepal_length": 7.9, "sepal_width": 3.2, "petal_length": 4.7, "petal_width": 1.4}))

>>> algorithm = Chebyshev()
>>> isclose(3.3, algorithm.distance(s1.sample.sample, u.sample))
True
"""

test_Euclidean = """
>>> s1 = TrainingKnownSample(
...     sample=KnownSample(
...         sample=Sample(
...             sepal_length=5.1, sepal_width=3.5, petal_length=1.4, petal_width=0.2), 
...         species="Iris-setosa")
...     )
>>> u = UnknownSample(Sample(**{"sepal_length": 7.9, "sepal_width": 3.2, "petal_length": 4.7, "petal_width": 1.4}))

>>> algorithm = Euclidean()
>>> isclose(4.50111097, algorithm.distance(s1.sample.sample, u.sample))
True
"""

test_Manhattan = """
>>> s1 = TrainingKnownSample(
...     sample=KnownSample(
...         sample=Sample(
...             sepal_length=5.1, sepal_width=3.5, petal_length=1.4, petal_width=0.2), 
...         species="Iris-setosa")
...    )
>>> u = UnknownSample(Sample(**{"sepal_length": 7.9, "sepal_width": 3.2, "petal_length": 4.7, "petal_width": 1.4}))

>>> algorithm = Manhattan()
>>> isclose(7.6, algorithm.distance(s1.sample.sample, u.sample))
True
"""

test_Sorensen = """
>>> s1 = TrainingKnownSample(
...     sample=KnownSample(
...         sample=Sample(
...             sepal_length=5.1, sepal_width=3.5, petal_length=1.4, petal_width=0.2), 
...         species="Iris-setosa")
...    )
>>> u = UnknownSample(Sample(**{"sepal_length": 7.9, "sepal_width": 3.2, "petal_length": 4.7, "petal_width": 1.4}))

>>> algorithm = Sorensen()
>>> isclose(0.2773722627, algorithm.distance(s1.sample.sample, u.sample))
True
"""

test_Mink2 = """
>>> s1 = TrainingKnownSample(
...     sample=KnownSample(
...         sample=Sample(
...             sepal_length=5.1, sepal_width=3.5, petal_length=1.4, petal_width=0.2), 
...         species="Iris-setosa")
...     )
>>> u = UnknownSample(Sample(**{"sepal_length": 7.9, "sepal_width": 3.2, "petal_length": 4.7, "petal_width": 1.4}))

>>> isclose(3.3, CD2().distance(s1.sample.sample, u.sample))
True
>>> isclose(7.6, MD2().distance(s1.sample.sample, u.sample))
True
>>> isclose(4.50111097, ED2().distance(s1.sample.sample, u.sample))
True
>>> isclose(4.50111097, ED2S().distance(s1.sample.sample, u.sample))
True

"""

test_Hyperparameter = """
>>> td = TrainingData('test')
>>> s2 = TestingKnownSample(
...     sample=KnownSample(
...         sample=Sample(
...             sepal_length=5.1, sepal_width=3.5, petal_length=1.4, petal_width=0.2), 
...         species="Iris-setosa")
...     )
>>> td.testing = [s2]
>>> t1 = TrainingKnownSample(KnownSample(Sample(**{"sepal_length": 5.1, "sepal_width": 3.5, "petal_length": 1.4, "petal_width": 0.2}), species="Iris-setosa"))
>>> t2 = TrainingKnownSample(KnownSample(Sample(**{"sepal_length": 7.9, "sepal_width": 3.2, "petal_length": 4.7, "petal_width": 1.4}), species="Iris-versicolor"))
>>> td.training = [t1, t2]
>>> h = Hyperparameter(k=3, algorithm=Chebyshev(), training=td)
>>> u = UnknownSample(Sample(sepal_length=5.1, sepal_width=3.5, petal_length=1.4, petal_width=0.2))
>>> h.classify(u)
'Iris-setosa'
>>> h.test()
Hyperparameter(k=3, algorithm=<model.Chebyshev object at ...>, data=<model.TrainingData object at ...>)
>>> print(f"data={td.name!r}, k={h.k}, quality={h.quality}")
data='test', k=3, quality=1.0
"""

test_TrainingData = """
>>> td = TrainingData('test')
>>> raw_data = [
... {"sepal_length": 5.1, "sepal_width": 3.5, "petal_length": 1.4, "petal_width": 0.2, "species": "Iris-setosa"},
... {"sepal_length": 7.9, "sepal_width": 3.2, "petal_length": 4.7, "petal_width": 1.4, "species": "Iris-versicolor"},
... ]
>>> td.load(raw_data)
>>> h = Hyperparameter(k=3, algorithm=Chebyshev(), training=td)
>>> len(td.training)
1
>>> len(td.testing)
1
>>> h.test()
Hyperparameter(k=3, algorithm=<model.Chebyshev object at ...>, data=<model.TrainingData object at ...>)
>>> print(f"data={td.name!r}, k={h.k}, quality={h.quality}")
data='test', k=3, quality=0.0
"""

__test__ = {name: case for name, case in globals().items() if name.startswith("test_")}

import time

if __name__ == "__main__":
    start = time.perf_counter()
    grid_search_1()
    end = time.perf_counter()
    print(f"Training Complete: {(end-start)*1000:.3f}ms")
