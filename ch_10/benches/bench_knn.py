"""
Python 3 Object-Oriented Programming Case Study

Chapter 10.
"""
from __future__ import annotations
import time
import random
import sys
from model import *

def a_lot_of_data(n: int = 1_250) -> tuple[list[TrainingKnownSample], list[TestingKnownSample]]:
    random.seed(42)
    training_partition = (
        KnownSample(
            sample=Sample(
                sepal_length=random.random(),
                sepal_width=random.random(),
                petal_length=random.random(),
                petal_width=random.random(),
            ),
            species=random.choice("abcd")
        )
        for i in range(8*n//10)
    )
    training_data = [TrainingKnownSample(s) for s in training_partition]
    testing_partition = (
        KnownSample(
            sample=Sample(
                sepal_length=random.random(),
                sepal_width=random.random(),
                petal_length=random.random(),
                petal_width=random.random(),
            ),
            species=random.choice("abcd")
        )
        for i in range(2*n//10)
    )
    testing_data = [TestingKnownSample(s) for s in testing_partition]
    return training_data, testing_data

def test_classifier(
        training_data: list[TrainingKnownSample],
        testing_data: list[TestingKnownSample],
        classifier: Classifier) -> None:
    h = Hyperparameter(
        k=5,
        distance_function=manhattan,
        training_data=training_data,
        classifier=classifier)
    start = time.perf_counter()
    q = h.test(testing_data)
    end = time.perf_counter()
    print(
        f'| {classifier.__name__:10s} '
        f'| q={q:5}/{len(testing_data):5} '
        f'| {end-start:6.3f}s |')

def main() -> None:
    test, train = a_lot_of_data(5_000)
    print("| algorithm  | test quality  | time    |")
    print("|------------|---------------|---------|")
    test_classifier(test, train, k_nn_1)
    test_classifier(test, train, k_nn_b)
    test_classifier(test, train, k_nn_q)

if __name__ == "__main__":
    main()
