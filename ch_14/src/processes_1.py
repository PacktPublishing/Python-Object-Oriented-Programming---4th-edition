"""
Python 3 Object-Oriented Programming

Chapter 14.  Concurrency
"""
from multiprocessing import Process, cpu_count
from threading import Thread
import time
import os


class MuchCPU(Process):
    def run(self) -> None:
        print(f"OS PID {os.getpid()}")

        s = sum(2 * i + 1 for i in range(100_000_000))


class MoreCPU(Thread):
    def run(self) -> None:
        print(f"OS PID {os.getpid()}")

        s = sum(2 * i + 1 for i in range(100_000_000))


if __name__ == "__main__":
    # workers = [MuchCPU() for f in range(cpu_count())]
    workers = [MoreCPU() for f in range(cpu_count())]

    t = time.perf_counter()
    for p in workers:
        p.start()
    for p in workers:
        p.join()
    print(f"work took {time.perf_counter() - t:.3f} seconds")
