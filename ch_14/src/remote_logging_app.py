"""
Python 3 Object-Oriented Programming

Chapter 14.  Concurrency
"""
from __future__ import annotations
import abc
from itertools import permutations
import logging
import logging.handlers
import os
import random
import time
import sys
from typing import Iterable

logger = logging.getLogger(f"app_{os.getpid()}")


class Sorter(abc.ABC):
    def __init__(self) -> None:
        id = os.getpid()
        self.logger = logging.getLogger(f"app_{id}.{self.__class__.__name__}")

    @abc.abstractmethod
    def sort(self, data: list[float]) -> list[float]:
        ...


class BogoSort(Sorter):
    @staticmethod
    def is_ordered(data: tuple[float, ...]) -> bool:
        pairs: Iterable[tuple[float, float]] = zip(data, data[1:])
        return all(a <= b for a, b in pairs)

    def sort(self, data: list[float]) -> list[float]:
        self.logger.info("Sorting %d", len(data))
        start = time.perf_counter()

        ordering: tuple[float, ...] = tuple(data[:])
        permute_iter = permutations(data)
        steps = 0
        while not BogoSort.is_ordered(ordering):
            ordering = next(permute_iter)
            steps += 1

        duration = 1000 * (time.perf_counter() - start)
        self.logger.info(
            "Sorted %d items in %d steps, %.3f ms", len(data), steps, duration
        )
        return list(ordering)


class GnomeSort(Sorter):
    def sort(self, data: list[float]) -> list[float]:
        self.logger.info("Sorting %d", len(data))
        start = time.perf_counter()

        index = 1
        while index != len(data):
            if data[index - 1] < data[index]:
                index += 1
            else:
                data[index - 1], data[index] = data[index], data[index - 1]
                if index > 1:
                    index -= 1

        duration = 1000 * (time.perf_counter() - start)
        self.logger.info("Sorted %d items, %.3f ms", len(data), duration)
        return data


def main(workload: int = 10, sorter: Sorter = BogoSort()) -> int:
    total = 0
    for i in range(workload):
        samples = random.randint(3, 10)
        data = [random.random() for _ in range(samples)]
        ordered = sorter.sort(data)
        total += samples
    return total


if __name__ == "__main__":
    LOG_HOST, LOG_PORT = "localhost", 18842
    socket_handler = logging.handlers.SocketHandler(LOG_HOST, LOG_PORT)
    stream_handler = logging.StreamHandler(sys.stderr)
    logging.basicConfig(handlers=[socket_handler, stream_handler], level=logging.INFO)

    start = time.perf_counter()
    workload = 10
    logger.info("sorting %d collections", workload)
    samples = main(workload, GnomeSort())
    end = time.perf_counter()
    logger.info("produced %d entries, taking %f s", workload * 2 + 2, end - start)

    logging.shutdown()
