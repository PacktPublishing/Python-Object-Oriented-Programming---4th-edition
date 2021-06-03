"""
Python 3 Object-Oriented Programming

Chapter 13.  Testing Object-Oriented Programs.
"""
from __future__ import annotations
import pytest
from model import TrainingKnownSample, UnknownSample
from model import CD, ED, MD, SD
from typing import Tuple, TypedDict


Known_Unknown = Tuple[TrainingKnownSample, UnknownSample]


class Row(TypedDict):
    species: str
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float


@pytest.fixture
def known_unknown_example_15() -> Known_Unknown:
    known_row: Row = {
        "species": "Iris-setosa",
        "sepal_length": 5.1,
        "sepal_width": 3.5,
        "petal_length": 1.4,
        "petal_width": 0.2,
    }
    k = TrainingKnownSample(**known_row)
    unknown_row = {
        "sepal_length": 7.9,
        "sepal_width": 3.2,
        "petal_length": 4.7,
        "petal_width": 1.4,
    }
    u = UnknownSample(**unknown_row)
    return k, u


def test_cd(known_unknown_example_15: Known_Unknown) -> None:
    k, u = known_unknown_example_15
    assert CD().distance(k, u) == pytest.approx(3.3)


def test_ed(known_unknown_example_15: Known_Unknown) -> None:
    k, u = known_unknown_example_15
    assert ED().distance(k, u) == pytest.approx(4.50111097)


def test_md(known_unknown_example_15: Known_Unknown) -> None:
    k, u = known_unknown_example_15
    assert MD().distance(k, u) == pytest.approx(7.6)


def test_sd(known_unknown_example_15: Known_Unknown) -> None:
    k, u = known_unknown_example_15
    assert SD().distance(k, u) == pytest.approx(0.2773722627)


from model import Hyperparameter
from unittest.mock import Mock, sentinel, call


@pytest.fixture
def sample_data() -> list[Mock]:
    return [
        Mock(name="Sample1", species=sentinel.Species3),
        Mock(name="Sample2", species=sentinel.Species1),
        Mock(name="Sample3", species=sentinel.Species1),
        Mock(name="Sample4", species=sentinel.Species1),
        Mock(name="Sample5", species=sentinel.Species3),
    ]


@pytest.fixture
def hyperparameter(sample_data: list[Mock]) -> Hyperparameter:
    mocked_distance = Mock(distance=Mock(side_effect=[11, 1, 2, 3, 13]))
    mocked_training_data = Mock(training=sample_data)
    mocked_weakref = Mock(return_value=mocked_training_data)
    fixture = Hyperparameter(k=3, algorithm=mocked_distance, training=sentinel.Unused)
    fixture.data = mocked_weakref
    return fixture


def test_hyperparameter(sample_data: list[Mock], hyperparameter: Mock) -> None:
    s = hyperparameter.classify(sentinel.Unknown)
    assert s == sentinel.Species1
    assert hyperparameter.algorithm.distance.mock_calls == [
        call(sentinel.Unknown, sample_data[0]),
        call(sentinel.Unknown, sample_data[1]),
        call(sentinel.Unknown, sample_data[2]),
        call(sentinel.Unknown, sample_data[3]),
        call(sentinel.Unknown, sample_data[4]),
    ]
