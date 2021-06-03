"""
Python 3 Object-Oriented Programming

Chapter 14.  Concurrency
"""
from __future__ import annotations
from pathlib import Path
from typing import List, Iterator, Optional, Union, TYPE_CHECKING

if TYPE_CHECKING:
    Query_Q = Queue[Union[str, None]]
    Result_Q = Queue[List[str]]


def search(paths: list[Path], query_q: Query_Q, results_q: Result_Q) -> None:
    print(f"PID: {os.getpid()}, paths {len(paths)}")
    lines: list[str] = []
    for path in paths:
        lines.extend(l.rstrip() for l in path.read_text().splitlines())

    while True:
        if (query_text := query_q.get()) is None:
            break
        results = [l for l in lines if query_text in l]
        results_q.put(results)


from fnmatch import fnmatch
import os


class DirectorySearch:
    def __init__(self) -> None:
        self.query_queues: list[Query_Q]
        self.results_queue: Result_Q
        self.search_workers: list[Process]

    def setup_search(self, paths: list[Path], cpus: Optional[int] = None) -> None:
        if cpus is None:
            cpus = cpu_count()
        worker_paths = [paths[i::cpus] for i in range(cpus)]
        self.query_queues = [Queue() for p in range(cpus)]
        self.results_queue = Queue()

        self.search_workers = [
            Process(target=search, args=(paths, q, self.results_queue))
            for paths, q in zip(worker_paths, self.query_queues)
        ]
        for proc in self.search_workers:
            proc.start()

    def teardown_search(self) -> None:
        # Signal process termination
        for q in self.query_queues:
            q.put(None)

        for proc in self.search_workers:
            proc.join()

    def search(self, target: str) -> Iterator[str]:
        print(f"search queues={self.query_queues}")
        for q in self.query_queues:
            q.put(target)

        for i in range(len(self.query_queues)):
            for match in self.results_queue.get():
                yield match


def all_source(path: Path, pattern: str) -> Iterator[Path]:
    for root, dirs, files in os.walk(path):
        for skip in {".tox", ".mypy_cache", "__pycache__", ".idea"}:
            if skip in dirs:
                dirs.remove(skip)
        yield from (Path(root) / f for f in files if fnmatch(f, pattern))


# VERY SLOW
# def all_source(path: Path) -> Iterator[Path]:
#     for code_path in path.glob("**/*.py"):
#         if any(n.startswith(".") for n in code_path.parts):
#             continue
#         if any(n.startswith("__") and n.endswith("__") for n in code_path.parts):
#             continue
#         yield code_path.absolute()


from multiprocessing import Process, Queue, cpu_count
import time

if __name__ == "__main__":
    ds = DirectorySearch()
    base = Path.cwd().parent
    all_paths = list(all_source(base, "*.py"))
    ds.setup_search(all_paths)
    for target in ("import", "class", "def"):
        start = time.perf_counter()
        count = 0
        for line in ds.search(target):
            # print(line)
            count += 1
        milliseconds = 1000 * (time.perf_counter() - start)
        print(
            f"Found {count} {target!r} in {len(all_paths)} files "
            f"in {milliseconds:.3f}ms"
        )
    ds.teardown_search()
