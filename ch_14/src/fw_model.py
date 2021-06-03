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
    NamedTuple,
    TextIO,
    TypedDict,
)

from multiprocessing.shared_memory import ShareableList
from multiprocessing.managers import BaseManager, SharedMemoryManager
from csv import DictReader


class SharedSamplesCSV:
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
    """

    fieldnames = (
        "sepal_length",
        "sepal_width",
        "petal_length",
        "petal_width",
        "species",
    )

    @classmethod
    def load(
        cls, smm: SharedMemoryManager, source: Iterable[dict[str, str]]
    ) -> ShareableList[Any]:
        """
        Usual multiprocessing parent::

            with SharedMemoryManager() as smm:
                with source_path.open() as source:
                    reader = csv.DictReader(source, SharedSamplesCSV.fieldnames)
                    data = SharedSamplesCSV.load(smm, reader)
                with futures.ProcessPoolExecutor() as workers:
                    workers.submit(function, data)

        Usual function(data)::

            factory = SharedSamplesCSV(data)
            row = factory.row(i)

        Test data can be built like this::

            >>> data = [
            ...     {"sepal_length": "5.1",
            ...      "sepal_width": "3.5",
            ...      "petal_length": "1.4",
            ...      "petal_width": "0.2",
            ...      "species": "Iris-setosa"},
            ... ]
            >>> with SharedMemoryManager() as smm:
            ...     data = SharedSamplesCSV.load(smm, data)
            ...     factory = SharedSamplesCSV(data)
            ...     factory.row(0)
            ...     KnownSample(factory, 0)
            {'sepal_length': 5.1, 'sepal_width': 3.5, 'petal_length': 1.4, 'petal_width': 0.2, 'species': 'Iris-setosa'}
            KnownSample(sample=Sample(sepal_length=5.1, sepal_width=3.5, petal_length=1.4, petal_width=0.2, ), species='Iris-setosa')

        """
        interim: list[Any] = []
        for source_dict in source:
            # Normalize source rows to fixed length and ordering.
            # TODO: Conversions could be done here.
            row = [source_dict.get(key, None) for key in cls.fieldnames]
            interim.extend(row)
        return smm.ShareableList(interim)

    def __init__(self, shareable: ShareableList[Any]) -> None:
        self._data = shareable

    def __len__(self) -> int:
        return len(self._data) // len(self.fieldnames)

    def row(self, r: int) -> dict[str, Any]:
        row_len = len(self.fieldnames)
        str_row = {
            name: self._data[r * row_len + offset]
            for offset, name in enumerate(self.fieldnames)
        }
        # TODO: Split out conversions
        return {
            "sepal_length": float(str_row["sepal_length"]),
            "sepal_width": float(str_row["sepal_width"]),
            "petal_length": float(str_row["petal_length"]),
            "petal_width": float(str_row["petal_width"]),
            "species": str_row["species"],
        }

    def row_iter(self) -> Iterable[dict[str, Any]]:
        exemplar = self.fieldnames[0]
        for i in range(len(self)):
            yield self.row(i)


class FWSample:
    """A Flyweight design that relies on a collection of ShareableList instances."""

    def __init__(self, shareable: SharedSamplesCSV, row_num: int) -> None:
        self._data = shareable.row(row_num)

    def __repr__(self) -> str:
        return (
            f"Sample(sepal_length={self.sepal_length}, "
            f"sepal_width={self.sepal_width}, "
            f"petal_length={self.petal_length}, "
            f"petal_width={self.petal_width}, "
            f")"
        )

    @property
    def sepal_length(self) -> float:
        return float(self._data["sepal_length"])

    @property
    def sepal_width(self) -> float:
        return float(self._data["sepal_width"])

    @property
    def petal_length(self) -> float:
        return float(self._data["petal_length"])

    @property
    def petal_width(self) -> float:
        return float(self._data["petal_width"])

    def astuple(self) -> tuple[float, float, float, float]:
        return (
            self.sepal_length,
            self.sepal_width,
            self.petal_length,
            self.petal_width,
        )

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, FWSample):
            return self.astuple() < other.astuple()
        raise NotImplemented

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, FWSample):
            return self.astuple() == other.astuple()
        raise NotImplemented


class KnownSample:
    def __init__(self, shareable: SharedSamplesCSV, row_num: int) -> None:
        self._data = shareable.row(row_num)
        self.sample = FWSample(shareable, row_num)

    def __repr__(self) -> str:
        return (
            f"KnownSample(sample=Sample(sepal_length={self.sample.sepal_length}, "
            f"sepal_width={self.sample.sepal_width}, "
            f"petal_length={self.sample.petal_length}, "
            f"petal_width={self.sample.petal_width}, "
            f"), species={self.species!r})"
        )

    @property
    def species(self) -> str:
        return str(self._data["species"])

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, KnownSample):
            return self.sample < other.sample
        raise NotImplemented

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, KnownSample):
            return self.sample == other.sample
        raise NotImplemented


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


class USample(NamedTuple):
    """A non-Flyweight Sample, used for UnknownSample,
    to make it polymorphic with the Testing/Training KnownSample wrappers.
    """

    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float


class UnknownSample:
    def __init__(self, sample: USample) -> None:
        self.sample = sample

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(sample={self.sample!r})"


Sample = Union[FWSample, USample]


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
>>> data = [
...     {"sepal_length": "5.1",
...      "sepal_width": "3.5",
...      "petal_length": "1.4",
...      "petal_width": "0.2",
...      "species": "Iris-setosa"}
... ]
>>> with SharedMemoryManager() as smm:
...     shareable_data = SharedSamplesCSV.load(smm, data)
...     factory = SharedSamplesCSV(shareable_data)
...     s1 = TrainingKnownSample(KnownSample(factory, 0))
...     unknown_row = {"sepal_length": 7.9, "sepal_width": 3.2, "petal_length": 4.7, "petal_width": 1.4}
...     u = UnknownSample(USample(**unknown_row))
...     isclose(3.3, CD().distance(s1.sample.sample, u.sample))
...     isclose(4.50111097, ED().distance(s1.sample.sample, u.sample))
...     isclose(7.6, MD().distance(s1.sample.sample, u.sample))
...     isclose(0.2773722627, SD().distance(s1.sample.sample, u.sample))
True
True
True
True

"""


class Chebyshev(Distance):
    """
    Computes the Chebyshev distance between two samples.

    ::

        >>> from math import isclose
        >>> from fw_model import TrainingKnownSample, UnknownSample, Chebyshev
        >>> from multiprocessing.managers import SharedMemoryManager
        >>> data = [
        ...     {"sepal_length": "5.1",
        ...      "sepal_width": "3.5",
        ...      "petal_length": "1.4",
        ...      "petal_width": "0.2",
        ...      "species": "Iris-setosa"},
        ... ]
        >>> with SharedMemoryManager() as smm:
        ...     shareable_data = SharedSamplesCSV.load(smm, data)
        ...     factory = SharedSamplesCSV(shareable_data)
        ...     s1 = TrainingKnownSample(KnownSample(factory, 0))
        ...     unknown_row = {"sepal_length": 7.9, "sepal_width": 3.2, "petal_length": 4.7, "petal_width": 1.4}
        ...     u = UnknownSample(USample(**unknown_row))
        ...     algorithm = Chebyshev()
        ...     isclose(3.3, algorithm.distance(s1.sample.sample, u.sample))
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
        >>> from fw_model import TrainingKnownSample, UnknownSample, Minkowski_2

        >>> class CD(Minkowski_2):
        ...     m = 1
        ...     reduction = max

        >>> from multiprocessing.managers import SharedMemoryManager
        >>> data = [
        ...     {"sepal_length": "5.1",
        ...      "sepal_width": "3.5",
        ...      "petal_length": "1.4",
        ...      "petal_width": "0.2",
        ...      "species": "Iris-setosa"},
        ... ]
        >>> with SharedMemoryManager() as smm:
        ...     shareable_data = SharedSamplesCSV.load(smm, data)
        ...     factory = SharedSamplesCSV(shareable_data)
        ...     s1 = TrainingKnownSample(KnownSample(factory, 0))
        ...     unknown_row = {"sepal_length": 7.9, "sepal_width": 3.2, "petal_length": 4.7, "petal_width": 1.4}
        ...     u = UnknownSample(USample(**unknown_row))
        ...     algorithm = CD()
        ...     isclose(3.3, algorithm.distance(s1.sample.sample, u.sample))
        True

    """

    @property
    @abc.abstractmethod
    def m(self) -> int:
        ...

    @staticmethod
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
        for sample in self.data.testing:
            sample.classification = self.classify(sample)
            if sample.matches():
                pass_count += 1
            else:
                fail_count += 1
        self.quality = pass_count / (pass_count + fail_count)
        return self

    def classify(self, unknown: Union[UnknownSample, TestingKnownSample]) -> str:
        """The k-NN algorithm"""
        sample: Sample
        if isinstance(unknown, TestingKnownSample):
            # Unwrap the Sample inside the TestingKnownSample
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
    """A set of training data and testing data with methods to load and test the samples.

    Note that this contains a large number of objects.
    It fails to make good use of the Flyweight design of
    the ``FWSample`` class.

    As an exercise, redesign this class to make ``testing``
    and ``training`` into properties.
    Each of these should be an iterable that's computed only
    when needed by scanning the given factory to get
    flyweight objects from shared memory.
    """

    def __init__(self, name: str) -> None:
        self.name = name
        self.uploaded: datetime.datetime
        self.tested: datetime.datetime
        self.training: list[TrainingKnownSample] = []
        self.testing: list[TestingKnownSample] = []

    def load(self, factory: SharedSamplesCSV) -> None:
        """Extract TestingKnownSample and TrainingKnownSample from raw data"""
        for n in range(len(factory)):
            if n % 5 == 0:
                test = TestingKnownSample(KnownSample(factory, n))
                self.testing.append(test)
                # print(test)
            else:
                train = TrainingKnownSample(KnownSample(factory, n))
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
    with SharedMemoryManager() as smm:
        source_path = Path.cwd().parent / "bezdekiris.data"
        with source_path.open() as source:
            reader = csv.DictReader(source, SharedSamplesCSV.fieldnames)
            shareable_data = SharedSamplesCSV.load(
                cast(SharedMemoryManager, smm), reader
            )

        factory = SharedSamplesCSV(shareable_data)
        td = TrainingData("Iris")
        td.load(factory)
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


# Special case, we don't *often* test abstract superclasses.
# In this example, however, we can create instances of the abstract class.
test_Sample = """
>>> data = [
...     {"sepal_length": "1",
...      "sepal_width": "2",
...      "petal_length": "3",
...      "petal_width": "4",
...      "species": "Iris-setosa"},
... ]
>>> with SharedMemoryManager() as smm:
...     shareable_data = SharedSamplesCSV.load(smm, data)
...     factory = SharedSamplesCSV(shareable_data)
...     x = Sample(factory, 0)
...     x
Sample(sepal_length=1.0, sepal_width=2.0, petal_length=3.0, petal_width=4.0, )

"""

test_TrainingKnownSample = """
>>> data = [
...     {"sepal_length": "5.1",
...      "sepal_width": "3.5",
...      "petal_length": "1.4",
...      "petal_width": "0.2",
...      "species": "Iris-setosa"},
... ]
>>> with SharedMemoryManager() as smm:
...     shareable_data = SharedSamplesCSV.load(smm, data)
...     factory = SharedSamplesCSV(shareable_data)
...     s1 = TrainingKnownSample(KnownSample(factory, 0))
...     s1
TrainingKnownSample(sample=KnownSample(sample=Sample(sepal_length=5.1, sepal_width=3.5, petal_length=1.4, petal_width=0.2, ), species='Iris-setosa'))

"""

test_TestingKnownSample = """
>>> data = [
...     {"sepal_length": "5.1",
...      "sepal_width": "3.5",
...      "petal_length": "1.4",
...      "petal_width": "0.2",
...      "species": "Iris-setosa"},
... ]
>>> with SharedMemoryManager() as smm:
...     shareable_data = SharedSamplesCSV.load(smm, data)
...     factory = SharedSamplesCSV(shareable_data)
...     s2 = TestingKnownSample(KnownSample(factory, 0))
...     s2
TestingKnownSample(sample=KnownSample(sample=Sample(sepal_length=5.1, sepal_width=3.5, petal_length=1.4, petal_width=0.2, ), species='Iris-setosa'), classification=None)
>>> s2.classification = "wrong"
>>> s2
TestingKnownSample(sample=KnownSample(sample=Sample(sepal_length=5.1, sepal_width=3.5, petal_length=1.4, petal_width=0.2, ), species='Iris-setosa'), classification='wrong')
"""

test_UnknownSample = """
>>> u = UnknownSample(USample(sepal_length=5.1, sepal_width=3.5, petal_length=1.4, petal_width=0.2))
>>> u
UnknownSample(sample=USample(sepal_length=5.1, sepal_width=3.5, petal_length=1.4, petal_width=0.2))
"""

test_ClassifiedSample = """
>>> u = UnknownSample(USample(sepal_length=5.1, sepal_width=3.5, petal_length=1.4, petal_width=0.2))
>>> c = ClassifiedSample(classification="Iris-setosa", unknown=u)
>>> c
ClassifiedSample(sepal_length=5.1, sepal_width=3.5, petal_length=1.4, petal_width=0.2, classification='Iris-setosa', )
"""

test_Chebyshev = """
>>> data = [
...     {"sepal_length": "5.1",
...      "sepal_width": "3.5",
...      "petal_length": "1.4",
...      "petal_width": "0.2",
...      "species": "Iris-setosa"},
... ]
>>> with SharedMemoryManager() as smm:
...     shareable_data = SharedSamplesCSV.load(smm, data)
...     factory = SharedSamplesCSV(shareable_data)
...     s1 = TrainingKnownSample(KnownSample(factory, 0))
...     u = UnknownSample(USample(**{"sepal_length": 7.9, "sepal_width": 3.2, "petal_length": 4.7, "petal_width": 1.4}))
...     algorithm = Chebyshev()
...     isclose(3.3, algorithm.distance(s1.sample.sample, u.sample))
True
"""

test_Euclidean = """
>>> data = [
...     {"sepal_length": "5.1",
...      "sepal_width": "3.5",
...      "petal_length": "1.4",
...      "petal_width": "0.2",
...      "species": "Iris-setosa"},
... ]
>>> with SharedMemoryManager() as smm:
...     shareable_data = SharedSamplesCSV.load(smm, data)
...     factory = SharedSamplesCSV(shareable_data)
...     s1 = TrainingKnownSample(KnownSample(factory, 0))
...     u = UnknownSample(USample(**{"sepal_length": 7.9, "sepal_width": 3.2, "petal_length": 4.7, "petal_width": 1.4}))
...     algorithm = Euclidean()
...     isclose(4.50111097, algorithm.distance(s1.sample.sample, u.sample))
True
"""

test_Manhattan = """
>>> data = [
...     {"sepal_length": "5.1",
...      "sepal_width": "3.5",
...      "petal_length": "1.4",
...      "petal_width": "0.2",
...      "species": "Iris-setosa"},
... ]
>>> with SharedMemoryManager() as smm:
...     shareable_data = SharedSamplesCSV.load(smm, data)
...     factory = SharedSamplesCSV(shareable_data)
...     s1 = TrainingKnownSample(KnownSample(factory, 0))
...     u = UnknownSample(USample(**{"sepal_length": 7.9, "sepal_width": 3.2, "petal_length": 4.7, "petal_width": 1.4}))
...     algorithm = Manhattan()
...     isclose(7.6, algorithm.distance(s1.sample.sample, u.sample))
True
"""

test_Sorensen = """
>>> data = [
...     {"sepal_length": "5.1",
...      "sepal_width": "3.5",
...      "petal_length": "1.4",
...      "petal_width": "0.2",
...      "species": "Iris-setosa"},
... ]
>>> with SharedMemoryManager() as smm:
...     shareable_data = SharedSamplesCSV.load(smm, data)
...     factory = SharedSamplesCSV(shareable_data)
...     s1 = TrainingKnownSample(KnownSample(factory, 0))
...     u = UnknownSample(USample(**{"sepal_length": 7.9, "sepal_width": 3.2, "petal_length": 4.7, "petal_width": 1.4}))
...     algorithm = Sorensen()
...     isclose(0.2773722627, algorithm.distance(s1.sample.sample, u.sample))
True
"""

test_Mink2 = """
>>> data = [
...     {"sepal_length": "5.1",
...      "sepal_width": "3.5",
...      "petal_length": "1.4",
...      "petal_width": "0.2",
...      "species": "Iris-setosa"},
... ]
>>> with SharedMemoryManager() as smm:
...     shareable_data = SharedSamplesCSV.load(smm, data)
...     factory = SharedSamplesCSV(shareable_data)
...     s1 = TrainingKnownSample(KnownSample(factory, 0))
...     u = UnknownSample(USample(**{"sepal_length": 7.9, "sepal_width": 3.2, "petal_length": 4.7, "petal_width": 1.4}))
...     isclose(3.3, CD2().distance(s1.sample.sample, u.sample))
...     isclose(7.6, MD2().distance(s1.sample.sample, u.sample))
...     isclose(4.50111097, ED2().distance(s1.sample.sample, u.sample))
...     isclose(4.50111097, ED2S().distance(s1.sample.sample, u.sample))
True
True
True
True

"""

test_Hyperparameter = """
>>> data = [
...     {"sepal_length": "5.1",
...      "sepal_width": "3.5",
...      "petal_length": "1.4",
...      "petal_width": "0.2",
...      "species": "Iris-setosa"},
...     {"sepal_length": 5.1, "sepal_width": 3.5, "petal_length": 1.4, "petal_width": 0.2, "species": "Iris-setosa"},
...     {"sepal_length": 7.9, "sepal_width": 3.2, "petal_length": 4.7, "petal_width": 1.4, "species": "Iris-versicolor"},
... ]
>>> with SharedMemoryManager() as smm:
...     td = TrainingData('test')
...     shareable_data = SharedSamplesCSV.load(smm, data)
...     factory = SharedSamplesCSV(shareable_data)
...     t0 = TestingKnownSample(KnownSample(factory, 0))
...     td.testing = [t0]
...     t1 = TrainingKnownSample(KnownSample(factory, 1))
...     t2 = TrainingKnownSample(KnownSample(factory, 2))
...     td.training = [t1, t2]
...     h = Hyperparameter(k=3, algorithm=Chebyshev(), training=td)
...     u = UnknownSample(USample(sepal_length=5.1, sepal_width=3.5, petal_length=1.4, petal_width=0.2))
...     h.classify(u)
...     h.test()
...     print(f"data={td.name!r}, k={h.k}, quality={h.quality}")
'Iris-setosa'
Hyperparameter(k=3, algorithm=<fw_model.Chebyshev object at ...>, data=<fw_model.TrainingData object at ...>)
data='test', k=3, quality=1.0
"""

test_TrainingData = """
>>> raw_data = [
... {"sepal_length": 5.1, "sepal_width": 3.5, "petal_length": 1.4, "petal_width": 0.2, "species": "Iris-setosa"},
... {"sepal_length": 7.9, "sepal_width": 3.2, "petal_length": 4.7, "petal_width": 1.4, "species": "Iris-versicolor"},
... ]
>>> with SharedMemoryManager() as smm:
...     shareable_data = SharedSamplesCSV.load(smm, raw_data)
...     factory = SharedSamplesCSV(shareable_data)
...     td = TrainingData('test')
...     td.load(smm, factory.row_iter())
...     h = Hyperparameter(k=3, algorithm=Chebyshev(), training=td)
...     len(td.training)
...     len(td.testing)
...     h.test()
...     print(f"data={td.name!r}, k={h.k}, quality={h.quality}")
1
1
Hyperparameter(k=3, algorithm=<fw_model.Chebyshev object at ...>, data=<fw_model.TrainingData object at ...>)
data='test', k=3, quality=0.0
"""

__test__ = {name: case for name, case in globals().items() if name.startswith("test_")}

import time

if __name__ == "__main__":
    start = time.perf_counter()
    grid_search_1()
    end = time.perf_counter()
    print(f"Training Complete: {(end-start)*1000:.3f}ms")
