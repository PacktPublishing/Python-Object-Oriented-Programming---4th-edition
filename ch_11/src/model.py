"""
Python 3 Object-Oriented Programming Case Study

Chapter 11. Common Design Patterns
"""
from __future__ import annotations
import bisect
import csv
import heapq
from collections import Counter
from typing import cast, NamedTuple, Callable, Iterable, List, Union


class Sample(NamedTuple):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float


class KnownSample(NamedTuple):
    sample: Sample
    species: str


class TestingKnownSample(NamedTuple):
    sample: KnownSample


class TrainingKnownSample(NamedTuple):
    sample: KnownSample


TestingList = List[TestingKnownSample]
TrainingList = List[TrainingKnownSample]


class UnknownSample(NamedTuple):
    sample: Sample


class ClassifiedKnownSample(NamedTuple):
    sample: KnownSample
    classification: str


class ClassifiedUnknownSample(NamedTuple):
    sample: UnknownSample
    classification: str


AnySample = Union[KnownSample, UnknownSample]
DistanceFunc = Callable[[TrainingKnownSample, AnySample], float]


class Measured(NamedTuple):
    """Measured distance is first to simplify sorting."""

    distance: float
    sample: TrainingKnownSample


import itertools
import collections
from typing import Tuple, Iterator, DefaultDict

ModuloDict = DefaultDict[int, List[KnownSample]]


def partition_2(
    samples: Iterable[KnownSample], training_rule: Callable[[int], bool]
) -> tuple[TrainingList, TestingList]:
    """Separate into non-equal buckets.
    Combine buckets into testing and training subsets.
    Chain into lists.
    Highly dependent on Hash Seed randomization; use PYTHONHASHSEED=0 in the environment.
    """
    rule_multiple = 60
    partitions: ModuloDict = collections.defaultdict(list)
    for s in samples:
        partitions[hash(s) % rule_multiple].append(s)

    training_partitions: list[Iterator[TrainingKnownSample]] = []
    testing_partitions: list[Iterator[TestingKnownSample]] = []
    for i, p in enumerate(partitions.values()):
        if training_rule(i):
            training_partitions.append(TrainingKnownSample(s) for s in p)
        else:
            testing_partitions.append(TestingKnownSample(s) for s in p)

    training = list(itertools.chain(*training_partitions))
    testing = list(itertools.chain(*testing_partitions))
    return training, testing


test_partition_2 = """
With certain hash seeds and a very small pool of data,
we *can* have collisions.
To keep the dataset small and minimize collisions, 
we use prime numbers < 250.

>>> data = [
...     KnownSample(sample=Sample(2, 3, 5, 7), species="C"),
...     KnownSample(sample=Sample(11, 13, 17, 19), species="G"),
...     KnownSample(sample=Sample(23, 29, 31, 37), species="I"),
...     KnownSample(sample=Sample(41, 43, 47, 53), species="O"),
... ]

The 25%/75% rule.
>>> train, test = partition_2(data, lambda i: i % 4 != 0)
>>> len(train)
3
>>> len(test)
1

"""


def k_nn_1(
    k: int, dist: DistanceFunc, training_data: TrainingList, unknown: AnySample
) -> str:
    """
    1.  Create a list of all (distance, training sample) pairs, sorted into ascending order.

    2.  Pick to the first _k_, the _k_ nearest neighbors.

    3.  Find the frequencies of result values among the _k_ nearest neighbors.

    4.  Chose the mode (the highest frequency) among the _k_ nearest neighbors.

    >>> data = [
    ...     TrainingKnownSample(KnownSample(sample=Sample(1, 2, 3, 4), species="a")),
    ...     TrainingKnownSample(KnownSample(sample=Sample(2, 3, 4, 5), species="b")),
    ...     TrainingKnownSample(KnownSample(sample=Sample(3, 4, 5, 6), species="c")),
    ...     TrainingKnownSample(KnownSample(sample=Sample(4, 5, 6, 7), species="d")),
    ... ]
    >>> dist = lambda ts1, u2: max(abs(ts1.sample.sample[i] - u2.sample[i]) for i in range(len(ts1)))
    >>> k_nn_1(1, dist, data, UnknownSample(Sample(1.1, 2.1, 3.1, 4.1)))
    'a'
    """
    distances = sorted(map(lambda t: Measured(dist(t, unknown), t), training_data))
    k_nearest = distances[:k]
    k_frequencies: Counter[str] = Counter(s.sample.sample.species for s in k_nearest)
    mode, fq = k_frequencies.most_common(1)[0]
    return mode


def k_nn_b(
    k: int, dist: DistanceFunc, training_data: TrainingList, unknown: AnySample
) -> str:
    """
    Use bisect.bisect_left() to maintain a short list of the _k_ nearest neighbors, in order.

    1. For each item:

        1. Compute the distance.

        2. If it's greater than the last of the _k_ nearest neighbors, discard it.

        3. Otherwise,

            1.  Find a spot among the _k_ values.

            2.  Insert the new item.

            3. Truncate the list back to length _k_.

    2.  Find the frequencies of result values among the _k_ nearest neighbors.

    3.  Chose the mode (the highest frequency) among the _k_ nearest neighbors.

    >>> data = [
    ...     TrainingKnownSample(KnownSample(sample=Sample(1, 2, 3, 4), species="a")),
    ...     TrainingKnownSample(KnownSample(sample=Sample(2, 3, 4, 5), species="b")),
    ...     TrainingKnownSample(KnownSample(sample=Sample(3, 4, 5, 6), species="c")),
    ...     TrainingKnownSample(KnownSample(sample=Sample(4, 5, 6, 7), species="d")),
    ... ]
    >>> dist = lambda ts1, u2: max(abs(ts1.sample.sample[i] - u2.sample[i]) for i in range(len(ts1)))
    >>> k_nn_b(1, dist, data, UnknownSample(Sample(1.1, 2.1, 3.1, 4.1)))
    'a'
    """
    k_nearest = [
        Measured(float("inf"), cast(TrainingKnownSample, None)) for _ in range(k)
    ]
    for t in training_data:
        t_dist = dist(t, unknown)
        if t_dist > k_nearest[-1].distance:
            continue
        new = Measured(t_dist, t)
        k_nearest.insert(bisect.bisect_left(k_nearest, new), new)
        k_nearest.pop(-1)
    k_frequencies: Counter[str] = Counter(s.sample.sample.species for s in k_nearest)
    mode, fq = k_frequencies.most_common(1)[0]
    return mode


def k_nn_q(
    k: int, dist: DistanceFunc, training_data: TrainingList, unknown: AnySample
) -> str:
    """
    Use heapq to maintain a list of the neighbors, in order, avoiding a sort
    after all computations are completed.

    1. For each item:

        1. Compute the distance.

        2. Push it to the heap queue, maintaining distance order.

    2.  Find the frequencies of result values among the _k_ nearest neighbors.

    3.  Chose the mode (the highest frequency) among the _k_ nearest neighbors.

    >>> data = [
    ...     TrainingKnownSample(KnownSample(sample=Sample(1, 2, 3, 4), species="a")),
    ...     TrainingKnownSample(KnownSample(sample=Sample(2, 3, 4, 5), species="b")),
    ...     TrainingKnownSample(KnownSample(sample=Sample(3, 4, 5, 6), species="c")),
    ...     TrainingKnownSample(KnownSample(sample=Sample(4, 5, 6, 7), species="d")),
    ... ]
    >>> dist = lambda ts1, u2: max(abs(ts1.sample.sample[i] - u2.sample[i]) for i in range(len(ts1)))
    >>> k_nn_q(1, dist, data, UnknownSample(Sample(1.1, 2.1, 3.1, 4.1)))
    'a'
    """
    measured_iter = (Measured(dist(t, unknown), t) for t in training_data)
    k_nearest = heapq.nsmallest(k, measured_iter)
    k_frequencies: Counter[str] = Counter(s.sample.sample.species for s in k_nearest)
    mode, fq = k_frequencies.most_common(1)[0]
    return mode


Classifier = Callable[[int, DistanceFunc, TrainingList, AnySample], str]


from typing import Protocol
from math import hypot


class Distance(Protocol):
    """A distance computation"""

    def distance(self, s1: TrainingKnownSample, s2: AnySample) -> float:
        """Matches the DistanceFunc protocol"""
        ...


class Euclidean(Distance):
    def distance(self, s1: TrainingKnownSample, s2: AnySample) -> float:
        return hypot(
            (s1.sample.sample.sepal_length - s2.sample.sepal_length) ** 2,
            (s1.sample.sample.sepal_width - s2.sample.sepal_width) ** 2,
            (s1.sample.sample.petal_length - s2.sample.petal_length) ** 2,
            (s1.sample.sample.petal_width - s2.sample.petal_width) ** 2,
        )


class Manhattan(Distance):
    def distance(self, s1: TrainingKnownSample, s2: AnySample) -> float:
        return sum(
            [
                abs(s1.sample.sample.sepal_length - s2.sample.sepal_length),
                abs(s1.sample.sample.sepal_width - s2.sample.sepal_width),
                abs(s1.sample.sample.petal_length - s2.sample.petal_length),
                abs(s1.sample.sample.petal_width - s2.sample.petal_width),
            ]
        )


class Chebyshev(Distance):
    def distance(self, s1: TrainingKnownSample, s2: AnySample) -> float:
        return max(
            [
                abs(s1.sample.sample.sepal_length - s2.sample.sepal_length),
                abs(s1.sample.sample.sepal_width - s2.sample.sepal_width),
                abs(s1.sample.sample.petal_length - s2.sample.petal_length),
                abs(s1.sample.sample.petal_width - s2.sample.petal_width),
            ]
        )


class Hyperparameter(NamedTuple):
    k: int
    distance: Distance
    training_data: TrainingList
    classifier: Classifier

    def classify(self, unknown: AnySample) -> str:
        classifier = self.classifier
        distance = self.distance
        return classifier(self.k, distance.distance, self.training_data, unknown)

    def test(self, testing: TestingList) -> float:
        classifier = self.classifier
        distance = self.distance
        test_results = (
            ClassifiedKnownSample(
                t.sample,
                classifier(self.k, distance.distance, self.training_data, t.sample),
            )
            for t in testing
        )
        pass_fail = map(
            lambda t: (1 if t.sample.species == t.classification else 0), test_results
        )
        return sum(pass_fail) / len(testing)


test_hyperparameter = """
>>> data = [
...     KnownSample(sample=Sample(1, 2, 3, 4), species="a"),
...     KnownSample(sample=Sample(2, 3, 4, 5), species="b"),
...     KnownSample(sample=Sample(3, 4, 5, 6), species="c"),
...     KnownSample(sample=Sample(4, 5, 6, 7), species="d"),
... ]
>>> manhattan = Manhattan()
>>> training_data = [TrainingKnownSample(s) for s in data]
>>> h = Hyperparameter(1, manhattan, training_data, k_nn_1)
>>> h.classify(UnknownSample(Sample(2, 3, 4, 5)))
'b'
>>> testing_data = [
...     TestingKnownSample(KnownSample(sample=Sample(1.1, 2.1, 3.1, 4.1), species="a")),
...     TestingKnownSample(KnownSample(sample=Sample(1.2, 2.2, 3.2, 4.3), species="b")),
... ]
>>> h.test(testing_data)
0.5
"""


class Timing(NamedTuple):
    k: int
    distance_name: str
    classifier_name: str
    quality: float
    time: float  # Milliseconds


import time


class TestCommand:
    def __init__(
        self,
        hyper_param: Hyperparameter,
        testing: TestingList,
    ) -> None:
        self.hyperparameter = hyper_param
        self.testing_samples = testing

    def test(self) -> Timing:
        start = time.perf_counter()
        recall_score = self.hyperparameter.test(self.testing_samples)
        end = time.perf_counter()
        timing = Timing(
            k=self.hyperparameter.k,
            distance_name=self.hyperparameter.distance.__class__.__name__,
            classifier_name=self.hyperparameter.classifier.__name__,
            quality=recall_score,
            time=round((end - start) * 1000.0, 3),
        )
        return timing


from pathlib import Path

manhattan = Manhattan()
euclidean = Euclidean()
chebyshev = Chebyshev()


def load(source: Path) -> tuple[TrainingList, TestingList]:
    """Load and partition known samples.
    The :func:`partition_2` function requires
    :envvar:`PYTHONHASHSEED` is zero in the environment settings.
    """
    header = ["sepal_length", "sepal_width", "petal_length", "petal_width", "species"]
    with source.open() as source_file:
        reader = csv.DictReader(source_file, header)
        data = (
            KnownSample(
                sample=Sample(
                    float(row["sepal_length"]),
                    float(row["sepal_width"]),
                    float(row["petal_length"]),
                    float(row["petal_width"]),
                ),
                species=row["species"],
            )
            for row in reader
        )
        train, test = partition_2(data, lambda i: i % 4 != 0)
    print(
        f"Training: {len(train)}, Testing: {len(test)}, Total: {len(train)+len(test)}"
    )
    return train, test


def tuning(source: Path) -> None:
    """
    1. Load data. Requires ``PYTHONHASHSEED=0`` in the environment settings.
    2. Create test scenarios.
    3. Execute all tests and gather timing.
    4. Display results.
    """
    train, test = load(source)
    scenarios = [
        TestCommand(Hyperparameter(k, df, train, cl), test)
        for k in range(3, 33, 2)
        for df in (euclidean, manhattan, chebyshev)
        for cl in (k_nn_1, k_nn_b, k_nn_q)
    ]
    timings = [s.test() for s in scenarios]
    for t in timings:
        if t.quality >= 1.0:
            print(t)


__test__ = {name: case for name, case in globals().items() if name.startswith("test_")}


if __name__ == "__main__":
    tuning(Path.cwd().parent / "bezdekiris.data")
