"""
Python 3 Object-Oriented Programming Case Study

Chapter 6, Abstract Base Classes and Operator Overloading
"""
from __future__ import annotations
import abc
import collections
import csv
import datetime
import itertools
import json
import jsonschema  # type: ignore[import]
from math import isclose
from pathlib import Path
import random
import sys
from typing import (
    cast,
    overload,
    Any,
    Optional,
    Union,
    Iterable,
    Iterator,
    List,
    Dict,
    Counter,
    Callable,
    Protocol,
    TypedDict,
    TypeVar,
    DefaultDict,
)
import weakref
import yaml


class Sample:
    """Abstract superclass for all samples."""

    def __init__(
        self,
        sepal_length: float,
        sepal_width: float,
        petal_length: float,
        petal_width: float,
    ) -> None:
        self.sepal_length = sepal_length
        self.sepal_width = sepal_width
        self.petal_length = petal_length
        self.petal_width = petal_width

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"sepal_length={self.sepal_length}, "
            f"sepal_width={self.sepal_width}, "
            f"petal_length={self.petal_length}, "
            f"petal_width={self.petal_width}, "
            f")"
        )

    def hash(self) -> int:
        return (
            sum(
                [
                    hash(self.sepal_length),
                    hash(self.sepal_width),
                    hash(self.petal_length),
                    hash(self.petal_width),
                ]
            )
            % sys.hash_info.modulus
        )

    def __eq__(self, other: Any) -> bool:
        if not issubclass(type(other), Sample):
            return False
        if self.hash() != other.hash():
            return False
        return all(
            [
                self.sepal_length == other.sepal_length,
                self.sepal_width == other.sepal_width,
                self.petal_length == other.petal_length,
                self.petal_width == other.petal_width,
            ]
        )


class KnownSample(Sample):
    """Abstract superclass for testing and training data, the species is set externally."""

    def __init__(
        self,
        species: str,
        sepal_length: float,
        sepal_width: float,
        petal_length: float,
        petal_width: float,
    ) -> None:
        super().__init__(
            sepal_length=sepal_length,
            sepal_width=sepal_width,
            petal_length=petal_length,
            petal_width=petal_width,
        )
        self.species = species

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"sepal_length={self.sepal_length}, "
            f"sepal_width={self.sepal_width}, "
            f"petal_length={self.petal_length}, "
            f"petal_width={self.petal_width}, "
            f"species={self.species!r}, "
            f")"
        )

    def __eq__(self, other: Any) -> bool:
        other = cast(KnownSample, other)
        return all(
            [
                self.sepal_length == other.sepal_length,
                self.sepal_width == other.sepal_width,
                self.petal_length == other.petal_length,
                self.petal_width == other.petal_width,
                self.species == other.species,
            ]
        )


class TrainingKnownSample(KnownSample):
    """Training data."""

    pass


class TestingKnownSample(KnownSample):
    """Testing data. A classifier can assign a species, which may or may not be correct."""

    def __init__(
        self,
        /,
        species: str,
        sepal_length: float,
        sepal_width: float,
        petal_length: float,
        petal_width: float,
        classification: Optional[str] = None,
    ) -> None:
        super().__init__(
            species=species,
            sepal_length=sepal_length,
            sepal_width=sepal_width,
            petal_length=petal_length,
            petal_width=petal_width,
        )
        self.classification = classification

    def matches(self) -> bool:
        return self.species == self.classification

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"sepal_length={self.sepal_length}, "
            f"sepal_width={self.sepal_width}, "
            f"petal_length={self.petal_length}, "
            f"petal_width={self.petal_width}, "
            f"species={self.species!r}, "
            f"classification={self.classification!r}, "
            f")"
        )


class UnknownSample(Sample):
    """A sample provided by a User, not yet classified."""

    pass


class ClassifiedSample(Sample):
    """Created from a sample provided by a User, and the results of classification."""

    def __init__(self, classification: str, sample: UnknownSample) -> None:
        super().__init__(
            sepal_length=sample.sepal_length,
            sepal_width=sample.sepal_width,
            petal_length=sample.petal_length,
            petal_width=sample.petal_width,
        )
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


class Distance:
    """A distance computation"""

    def distance(self, s1: Sample, s2: Sample) -> float:
        raise NotImplementedError


class Chebyshev(Distance):
    """
    Computes the Chebyshev distance between two samples.

    ::

        >>> from math import isclose
        >>> from model import TrainingKnownSample, UnknownSample, Chebyshev

        >>> s1 = TrainingKnownSample(
        ...     sepal_length=5.1, sepal_width=3.5, petal_length=1.4, petal_width=0.2, species="Iris-setosa")
        >>> u = UnknownSample(**{"sepal_length": 7.9, "sepal_width": 3.2, "petal_length": 4.7, "petal_width": 1.4})

        >>> algorithm = Chebyshev()
        >>> isclose(3.3, algorithm.distance(s1, u))
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

    m: int

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


class Reduce_Function(Protocol):
    """Define a callable object with specific parameters."""

    def __call__(self, values: list[float]) -> float:
        pass


class Minkowski_2(Distance):
    """A generic way to implement Manhattan, Euclidean, and Chebyshev.

    ::

        >>> from math import isclose
        >>> from model import TrainingKnownSample, UnknownSample, Minkowski_2

        >>> class CD(Minkowski_2):
        ...     m = 1
        ...     reduction = max

        >>> s1 = TrainingKnownSample(
        ...     sepal_length=5.1, sepal_width=3.5, petal_length=1.4, petal_width=0.2, species="Iris-setosa")
        >>> u = UnknownSample(**{"sepal_length": 7.9, "sepal_width": 3.2, "petal_length": 4.7, "petal_width": 1.4})

        >>> algorithm = CD()
        >>> isclose(3.3, algorithm.distance(s1, u))
        True

    """

    m: int
    reduction: Reduce_Function

    def distance(self, s1: Sample, s2: Sample) -> float:
        # Required to prevent Python from passing `self` as the first argument.
        summarize = self.reduction
        return (
            summarize(
                [
                    abs(s1.sepal_length - s2.sepal_length) ** self.m,
                    abs(s1.sepal_width - s2.sepal_width) ** self.m,
                    abs(s1.petal_length - s2.petal_length) ** self.m,
                    abs(s1.petal_width - s2.petal_width) ** self.m,
                ]
            )
            ** (1 / self.m)
        )


class Hyperparameter:
    """A hyperparameter value and the overall quality of the classification."""

    def __init__(self, k: int, algorithm: "Distance", training: "TrainingData") -> None:
        self.k = k
        self.algorithm = algorithm
        self.data: weakref.ReferenceType["TrainingData"] = weakref.ref(training)
        self.quality: float

    def test(self) -> None:
        """Run the entire test suite."""
        training_data: Optional["TrainingData"] = self.data()
        if not training_data:
            raise RuntimeError("Broken Weak Reference")
        pass_count, fail_count = 0, 0
        for sample in training_data.testing:
            sample.classification = self.classify(sample)
            if sample.matches():
                pass_count += 1
            else:
                fail_count += 1
        self.quality = pass_count / (pass_count + fail_count)

    def classify(self, sample: Union[UnknownSample, TestingKnownSample]) -> str:
        """The k-NN algorithm"""
        training_data = self.data()
        if not training_data:
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


class SampleDict(TypedDict):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float
    species: str


class SamplePartition(List[SampleDict], abc.ABC):
    @overload
    def __init__(self, *, training_subset: float = 0.80) -> None:
        ...

    @overload
    def __init__(
        self,
        iterable: Optional[Iterable[SampleDict]] = None,
        *,
        training_subset: float = 0.80,
    ) -> None:
        ...

    def __init__(
        self,
        iterable: Optional[Iterable[SampleDict]] = None,
        *,
        training_subset: float = 0.80,
    ) -> None:
        self.training_subset = training_subset
        if iterable:
            super().__init__(iterable)
        else:
            super().__init__()

    @abc.abstractproperty
    @property
    def training(self) -> list[TrainingKnownSample]:
        ...

    @abc.abstractproperty
    @property
    def testing(self) -> list[TestingKnownSample]:
        ...


class ShufflingSamplePartition(SamplePartition):
    def __init__(
        self,
        iterable: Optional[Iterable[SampleDict]] = None,
        *,
        training_subset: float = 0.80,
    ) -> None:
        super().__init__(iterable, training_subset=training_subset)
        self.split: Optional[int] = None

    def shuffle(self) -> None:
        if not self.split:
            random.shuffle(self)
            self.split = int(len(self) * self.training_subset)

    @property
    def training(self) -> list[TrainingKnownSample]:
        self.shuffle()
        return [TrainingKnownSample(**sd) for sd in self[: self.split]]

    @property
    def testing(self) -> list[TestingKnownSample]:
        self.shuffle()
        return [TestingKnownSample(**sd) for sd in self[self.split :]]


test_shuffling = """
>>> import random
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

"""


class DealingPartition(abc.ABC):
    @abc.abstractmethod
    def __init__(
        self,
        items: Optional[Iterable[SampleDict]],
        *,
        training_subset: tuple[int, int] = (8, 10),
    ) -> None:
        ...

    @abc.abstractmethod
    def extend(self, items: Iterable[SampleDict]) -> None:
        ...

    @abc.abstractmethod
    def append(self, item: SampleDict) -> None:
        ...

    @property
    @abc.abstractmethod
    def training(self) -> list[TrainingKnownSample]:
        ...

    @property
    @abc.abstractmethod
    def testing(self) -> list[TestingKnownSample]:
        ...


class CountingDealingPartition(DealingPartition):
    def __init__(
        self,
        items: Optional[Iterable[SampleDict]],
        *,
        training_subset: tuple[int, int] = (8, 10),
    ) -> None:
        self.training_subset = training_subset
        self.counter = 0
        self._training: list[TrainingKnownSample] = []
        self._testing: list[TestingKnownSample] = []
        if items:
            self.extend(items)

    def extend(self, items: Iterable[SampleDict]) -> None:
        for item in items:
            self.append(item)

    def append(self, item: SampleDict) -> None:
        n, d = self.training_subset
        if self.counter % d < n:
            self._training.append(TrainingKnownSample(**item))
        else:
            self._testing.append(TestingKnownSample(**item))
        self.counter += 1

    @property
    def training(self) -> list[TrainingKnownSample]:
        return self._training

    @property
    def testing(self) -> list[TestingKnownSample]:
        return self._testing


import collections.abc
import typing
import sys

if sys.version_info >= (3, 9):
    BucketCollection = collections.abc.Collection[Sample]
else:
    BucketCollection = typing.Collection[Sample]


class BucketedCollection(BucketCollection):
    """
    >>> from pprint import pprint
    >>> b = BucketedCollection()
    >>> b.extend(
    ...     [
    ...         Sample(1, 2, 3, 4),
    ...         Sample(1, 2, 3, 4),
    ...         Sample(1, 1, 1, 1),
    ...         Sample(2, 2, 2, 2),
    ...     ]
    ... )
    ...
    >>> Sample(1, 2, 3, 4) in b
    True
    >>> Sample(2, 2, 2, 3) in b
    False
    >>> len(b)
    4
    >>> pprint(list(b))
    [Sample(sepal_length=1, sepal_width=2, petal_length=3, petal_width=4, ),
     Sample(sepal_length=1, sepal_width=2, petal_length=3, petal_width=4, ),
     Sample(sepal_length=1, sepal_width=1, petal_length=1, petal_width=1, ),
     Sample(sepal_length=2, sepal_width=2, petal_length=2, petal_width=2, )]
    """

    def __init__(self, samples: Optional[Iterable[Sample]] = None) -> None:
        super().__init__()
        self.buckets: DefaultDict[int, list[Sample]] = collections.defaultdict(list)
        if samples:
            self.extend(samples)

    def extend(self, samples: Iterable[Sample]) -> None:
        for sample in samples:
            self.append(sample)

    def append(self, sample: Sample) -> None:
        b = sample.hash() % 128
        self.buckets[b].append(sample)

    def __contains__(self, target: Any) -> bool:
        b = cast(Sample, target).hash() % 128
        return any(existing == target for existing in self.buckets[b])

    def __len__(self) -> int:
        return sum(len(b) for b in self.buckets.values())

    def __iter__(self) -> Iterator[Sample]:
        return itertools.chain(*self.buckets.values())


class BucketedDealingPartition_80(DealingPartition):
    training_subset = (8, 10)  # 8/10 == 80%
    # 2/3 and 1/2 are common choices.

    def __init__(self, items: Optional[Iterable[SampleDict]]) -> None:
        self.counter = 0
        self._training = BucketedCollection()
        self._testing: list[TestingKnownSample] = []
        if items:
            self.extend(items)

    def extend(self, items: Iterable[SampleDict]) -> None:
        for item in items:
            self.append(item)

    def append(self, item: SampleDict) -> None:
        n, d = self.training_subset
        if self.counter % d < n:
            self._training.append(TrainingKnownSample(**item))
        else:
            candidate = TestingKnownSample(**item)
            if candidate in self._training:
                # Duplicate, create a Training sample from it
                self._training.append(TrainingKnownSample(**item))
            else:
                self._testing.append(candidate)
        self.counter += 1

    @property
    def training(self) -> list[TrainingKnownSample]:
        return cast(list[TrainingKnownSample], list(self._training))

    @property
    def testing(self) -> list[TestingKnownSample]:
        return self._testing


class TrainingData:
    """A set of training data and testing data with methods to load and test the samples."""

    partition_class = CountingDealingPartition

    def __init__(self, name: str) -> None:
        self.name = name
        self.uploaded: datetime.datetime
        self.tested: datetime.datetime
        self.training: list[TrainingKnownSample] = []
        self.testing: list[TestingKnownSample] = []
        self.tuning: list[Hyperparameter] = []

    def load(self, raw_data_iter: Iterable[SampleDict]) -> None:
        """Extract TestingKnownSample and TrainingKnownSample from raw data"""
        # Needed to avoid making look like a method
        partition_class = self.partition_class
        partitioner = partition_class(raw_data_iter, training_subset=(1, 2))
        self.training = partitioner.training
        self.testing = partitioner.testing
        self.uploaded = datetime.datetime.now(tz=datetime.timezone.utc)

    def test(self, parameter: Hyperparameter) -> None:
        """Test this hyperparamater value."""
        parameter.test()
        self.tuning.append(parameter)
        self.tested = datetime.datetime.now(tz=datetime.timezone.utc)

    def classify(
        self, parameter: Hyperparameter, sample: UnknownSample
    ) -> ClassifiedSample:
        return ClassifiedSample(
            classification=parameter.classify(sample), sample=sample
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


class CSVIrisReader_2:
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

    def __init__(self, source: Path) -> None:
        self.source = source

    def data_iter(self) -> Iterator[dict[str, str]]:
        with self.source.open() as source_file:
            reader = csv.reader(source_file)
            for row in reader:
                yield dict(
                    sepal_length=row[0],  # in cm
                    sepal_width=row[1],  # in cm
                    petal_length=row[2],  # in cm
                    petal_width=row[3],  # in cm
                    species=row[4],  # class string
                )


class JSONIrisReader:
    def __init__(self, source: Path) -> None:
        self.source = source

    def data_iter(self) -> Iterator[SampleDict]:
        with self.source.open() as source_file:
            sample_list = json.load(source_file)
        yield from iter(sample_list)


class NDJSONIrisReader:
    def __init__(self, source: Path) -> None:
        self.source = source

    def data_iter(self) -> Iterator[SampleDict]:
        with self.source.open() as source_file:
            for line in source_file:
                sample = json.loads(line)
                yield sample


IRIS_SCHEMA = {
    "$schema": "https://json-schema.org/draft/2019-09/hyper-schema",
    "title": "Iris Data Schema",
    "description": "Schema of Bezdek Iris data",
    "type": "object",
    "properties": {
        "sepal_length": {"type": "number", "description": "Sepal Length in cm"},
        "sepal_width": {"type": "number", "description": "Sepal Length in cm"},
        "petal_length": {"type": "number", "description": "Sepal Length in cm"},
        "petal_width": {"type": "number", "description": "Sepal Length in cm"},
        "species": {
            "type": "string",
            "description": "class",
            "enum": ["Iris-setosa", "Iris-versicolor", "Iris-virginica"],
        },
    },
    "required": ["sepal_length", "sepal_width", "petal_length", "petal_width"],
}


class ValidatingNDJSONIrisReader:
    def __init__(self, source: Path, schema: dict[str, Any]) -> None:
        self.source = source
        self.validator = jsonschema.Draft7Validator(schema)

    def data_iter(self) -> Iterator[SampleDict]:
        with self.source.open() as source_file:
            for line in source_file:
                sample = json.loads(line)
                if self.validator.is_valid(sample):
                    yield sample
                else:
                    print(f"Invalid: {sample}")


class YAMLIrisReader:
    def __init__(self, source: Path) -> None:
        self.source = source

    def data_iter(self) -> Iterator[SampleDict]:
        with self.source.open() as source_file:
            yield from yaml.load_all(source_file, Loader=yaml.SafeLoader)


# Special case, we don't *often* test abstract superclasses.
# In this example, however, we can create instances of the abstract class.
test_Sample = """
>>> x = Sample(1, 2, 3, 4)
>>> x
Sample(sepal_length=1, sepal_width=2, petal_length=3, petal_width=4, )
>>> y = Sample(1, 2, 3, 4)
>>> x is y
False
>>> x.hash() == y.hash()
True
>>> x == y
True
>>> z = Sample(2, 3, 4, 1)
>>> x.hash() == z.hash()
True
>>> x == z
False
>>> a = Sample(1, 1, 2, 2)
>>> x.hash() == a.hash()
False
"""

test_TrainingKnownSample = """
>>> s1 = TrainingKnownSample(
...     sepal_length=5.1, sepal_width=3.5, petal_length=1.4, petal_width=0.2, species="Iris-setosa")
>>> s1
TrainingKnownSample(sepal_length=5.1, sepal_width=3.5, petal_length=1.4, petal_width=0.2, species='Iris-setosa', )
"""

test_TestingKnownSample = """
>>> s2 = TestingKnownSample(
...     sepal_length=5.1, sepal_width=3.5, petal_length=1.4, petal_width=0.2, species="Iris-setosa")
>>> s2
TestingKnownSample(sepal_length=5.1, sepal_width=3.5, petal_length=1.4, petal_width=0.2, species='Iris-setosa', classification=None, )
>>> s2.classification = "wrong"
>>> s2
TestingKnownSample(sepal_length=5.1, sepal_width=3.5, petal_length=1.4, petal_width=0.2, species='Iris-setosa', classification='wrong', )
"""

test_UnknownSample = """
>>> u = UnknownSample(sepal_length=5.1, sepal_width=3.5, petal_length=1.4, petal_width=0.2, )
>>> u
UnknownSample(sepal_length=5.1, sepal_width=3.5, petal_length=1.4, petal_width=0.2, )
"""

test_ClassifiedSample = """
>>> u = UnknownSample(sepal_length=5.1, sepal_width=3.5, petal_length=1.4, petal_width=0.2, )
>>> c = ClassifiedSample(classification="Iris-setosa", sample=u)
>>> c
ClassifiedSample(sepal_length=5.1, sepal_width=3.5, petal_length=1.4, petal_width=0.2, classification='Iris-setosa', )
"""

test_Chebyshev = """
>>> s1 = TrainingKnownSample(
...     sepal_length=5.1, sepal_width=3.5, petal_length=1.4, petal_width=0.2, species="Iris-setosa")
>>> u = UnknownSample(**{"sepal_length": 7.9, "sepal_width": 3.2, "petal_length": 4.7, "petal_width": 1.4})

>>> algorithm = Chebyshev()
>>> isclose(3.3, algorithm.distance(s1, u))
True
"""

test_Euclidean = """
>>> s1 = TrainingKnownSample(
...     sepal_length=5.1, sepal_width=3.5, petal_length=1.4, petal_width=0.2, species="Iris-setosa")
>>> u = UnknownSample(**{"sepal_length": 7.9, "sepal_width": 3.2, "petal_length": 4.7, "petal_width": 1.4})

>>> algorithm = Euclidean()
>>> isclose(4.50111097, algorithm.distance(s1, u))
True
"""

test_Manhattan = """
>>> s1 = TrainingKnownSample(
...     sepal_length=5.1, sepal_width=3.5, petal_length=1.4, petal_width=0.2, species="Iris-setosa")
>>> u = UnknownSample(**{"sepal_length": 7.9, "sepal_width": 3.2, "petal_length": 4.7, "petal_width": 1.4})

>>> algorithm = Manhattan()
>>> isclose(7.6, algorithm.distance(s1, u))
True
"""

test_Sorensen = """
>>> s1 = TrainingKnownSample(
...     sepal_length=5.1, sepal_width=3.5, petal_length=1.4, petal_width=0.2, species="Iris-setosa")
>>> u = UnknownSample(**{"sepal_length": 7.9, "sepal_width": 3.2, "petal_length": 4.7, "petal_width": 1.4})

>>> algorithm = Sorensen()
>>> isclose(0.2773722627, algorithm.distance(s1, u))
True
"""

test_Hyperparameter = """
>>> td = TrainingData('test')
>>> s2 = TestingKnownSample(
...     sepal_length=5.1, sepal_width=3.5, petal_length=1.4, petal_width=0.2, species="Iris-setosa")
>>> td.testing = [s2]
>>> t1 = TrainingKnownSample(**{"sepal_length": 5.1, "sepal_width": 3.5, "petal_length": 1.4, "petal_width": 0.2, "species": "Iris-setosa"})
>>> t2 = TrainingKnownSample(**{"sepal_length": 7.9, "sepal_width": 3.2, "petal_length": 4.7, "petal_width": 1.4, "species": "Iris-versicolor"})
>>> td.training = [t1, t2]
>>> h = Hyperparameter(k=3, algorithm=Chebyshev(), training=td)
>>> u = UnknownSample(sepal_length=5.1, sepal_width=3.5, petal_length=1.4, petal_width=0.2)
>>> h.classify(u)
'Iris-setosa'
>>> h.test()
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
>>> td.test(h)
>>> print(f"data={td.name!r}, k={h.k}, quality={h.quality}")
data='test', k=3, quality=0.0
"""

__test__ = {name: case for name, case in globals().items() if name.startswith("test_")}
