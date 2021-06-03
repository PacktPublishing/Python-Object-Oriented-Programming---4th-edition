"""
Python 3 Object-Oriented Programming

Chapter 14.  Concurrency
"""
from __future__ import annotations
from math import sqrt
from model import TrainingData, CSVIrisReader, TrainingKnownSample
from pathlib import Path
from typing import List, NamedTuple, cast

SpeciesValue = {
    "Iris-setosa": 1,
    "Iris-versicolor": 2,
    "Iris-virginica": 3,
}


class SpeciesFeature(NamedTuple):
    tks: TrainingKnownSample

    def species(self) -> int:
        return SpeciesValue[self.tks.sample.species]

    def feature(self, name: str) -> float:
        return cast(float, getattr(self.tks.sample.sample, name))


def covariance(data: list[TrainingKnownSample], attr: str) -> None:
    species_feature_data = [SpeciesFeature(tks) for tks in data]
    n = sum(1 for s in species_feature_data)
    species_mean = sum(s.species() for s in species_feature_data) / n
    feature_mean = sum(s.feature(attr) for s in species_feature_data) / n
    feature_min = min(s.feature(attr) for s in species_feature_data)
    feature_max = max(s.feature(attr) for s in species_feature_data)
    species_sd = sqrt(
        sum((s.species() - species_mean) ** 2 for s in species_feature_data) / n
    )
    feature_sd = sqrt(
        sum((s.feature(attr) - feature_mean) ** 2 for s in species_feature_data) / n
    )
    covariance = (
        sum(
            (s.species() - species_mean) * (s.feature(attr) - feature_mean)
            for s in species_feature_data
        )
        / n
    )
    correlation = covariance / (species_sd * feature_sd)
    print(
        f"{attr:12s} "
        f"{feature_min:3.1f} {feature_max:3.1f} "
        f"{feature_mean:4.2f} {feature_sd:4.2f} "
        f"{correlation:7.4f}"
    )


def analyze() -> None:
    td = TrainingData("Iris")
    source_path = Path.cwd().parent / "bezdekiris.data"
    reader = CSVIrisReader(source_path)
    td.load(reader.data_iter())

    print(f"{'attribute':12s} {'min':3s} {'max':3s} {'mean':4s} {'sd':4s} {'corr':7s}")
    for attr in "sepal_length", "sepal_width", "petal_length", "petal_width":
        covariance(td.training, attr)


if __name__ == "__main__":
    analyze()
