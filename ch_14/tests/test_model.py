"""
Python 3 Object-Oriented Programming

Chapter 13.  Testing Object-Oriented Programs.
"""
from __future__ import annotations
import pytest
from model import TrainingKnownSample, UnknownSample, KnownSample, Sample
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
    ks = KnownSample(
        sample=Sample(
            sepal_length=float(known_row["sepal_length"]),
            sepal_width=float(known_row["sepal_width"]),
            petal_length=float(known_row["petal_length"]),
            petal_width=float(known_row["petal_width"]),
        ),
        species=known_row["species"],
    )
    k = TrainingKnownSample(ks)

    unknown_row = {
        "sepal_length": 7.9,
        "sepal_width": 3.2,
        "petal_length": 4.7,
        "petal_width": 1.4,
    }
    u = UnknownSample(
        sample=Sample(
            sepal_length=float(unknown_row["sepal_length"]),
            sepal_width=float(unknown_row["sepal_width"]),
            petal_length=float(unknown_row["petal_length"]),
            petal_width=float(unknown_row["petal_width"]),
        )
    )
    return k, u


def test_cd(known_unknown_example_15: Known_Unknown) -> None:
    k, u = known_unknown_example_15
    assert CD().distance(k.sample.sample, u.sample) == pytest.approx(3.3)


def test_ed(known_unknown_example_15: Known_Unknown) -> None:
    k, u = known_unknown_example_15
    assert ED().distance(k.sample.sample, u.sample) == pytest.approx(4.50111097)


def test_md(known_unknown_example_15: Known_Unknown) -> None:
    k, u = known_unknown_example_15
    assert MD().distance(k.sample.sample, u.sample) == pytest.approx(7.6)


def test_sd(known_unknown_example_15: Known_Unknown) -> None:
    k, u = known_unknown_example_15
    assert SD().distance(k.sample.sample, u.sample) == pytest.approx(0.2773722627)


from model import Hyperparameter
from unittest.mock import Mock, sentinel, call


@pytest.fixture
def sample_data() -> list[Mock]:
    return [
        Mock(name="TrainingKnownSample1", sample=Mock(name="KnownSample1", sample=sentinel.Sample1, species=sentinel.Species3)),
        Mock(name="TrainingKnownSample1", sample=Mock(name="KnownSample2", sample=sentinel.Sample2, species=sentinel.Species1)),
        Mock(name="TrainingKnownSample1", sample=Mock(name="KnownSample3", sample=sentinel.Sample3, species=sentinel.Species1)),
        Mock(name="TrainingKnownSample1", sample=Mock(name="KnownSample4", sample=sentinel.Sample4, species=sentinel.Species1)),
        Mock(name="TrainingKnownSample1", sample=Mock(name="KnownSample5", sample=sentinel.Sample6, species=sentinel.Species3)),
    ]


@pytest.fixture
def hyperparameter(sample_data: list[Mock]) -> Hyperparameter:
    mocked_distance = Mock(distance=Mock(side_effect=[11, 1, 2, 3, 13]))
    mocked_training_data = Mock(training=sample_data)
    fixture = Hyperparameter(k=3, algorithm=mocked_distance, training=mocked_training_data)
    return fixture


def test_hyperparameter(sample_data: list[Mock], hyperparameter: Mock) -> None:
    mock_unknown = Mock(sample=sentinel.Unknown)
    s = hyperparameter.classify(mock_unknown)
    assert s == sentinel.Species1
    assert hyperparameter.algorithm.distance.mock_calls == [
        call(sample_data[0].sample.sample, sentinel.Unknown),
        call(sample_data[1].sample.sample, sentinel.Unknown),
        call(sample_data[2].sample.sample, sentinel.Unknown),
        call(sample_data[3].sample.sample, sentinel.Unknown),
        call(sample_data[4].sample.sample, sentinel.Unknown),
    ]
