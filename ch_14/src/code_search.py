"""
Python 3 Object-Oriented Programming

Chapter 14.  Concurrency
"""
from __future__ import annotations
import argparse
import ast
from concurrent import futures
from fnmatch import fnmatch
import os
from pathlib import Path
import sys
import time
from typing import Iterator, NamedTuple


class ImportResult(NamedTuple):
    path: Path
    imports: set[str]

    @property
    def focus(self) -> bool:
        return "typing" in self.imports


class ImportVisitor(ast.NodeVisitor):
    def __init__(self) -> None:
        self.imports: set[str] = set()

    def visit_Import(self, node: ast.Import) -> None:
        # print(ast.dump(node))
        for alias in node.names:
            self.imports.add(alias.name)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        # print(ast.dump(node))
        if node.module:
            self.imports.add(node.module)


def find_imports(path: Path) -> ImportResult:
    tree = ast.parse(path.read_text())
    iv = ImportVisitor()
    iv.visit(tree)
    return ImportResult(path, iv.imports)


def all_source(path: Path, pattern: str) -> Iterator[Path]:
    for root, dirs, files in os.walk(path):
        for skip in {".tox", ".mypy_cache", "__pycache__", ".idea"}:
            if skip in dirs:
                dirs.remove(skip)
        yield from (Path(root) / f for f in files if fnmatch(f, pattern))


def get_options(argv: list[str] = sys.argv[1:]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=Path, nargs="*")
    return parser.parse_args(argv)


def main(base: Path = Path.cwd()) -> None:
    print(f"\n{base}")
    start = time.perf_counter()
    with futures.ThreadPoolExecutor(24) as pool:
        analyzers = [
            pool.submit(find_imports, path) for path in all_source(base, "*.py")
        ]
        analyzed = (worker.result() for worker in futures.as_completed(analyzers))
    for example in sorted(analyzed):
        print(
            f"{'->' if example.focus else '':2s} "
            f"{example.path.relative_to(base)} {example.imports}"
        )
    end = time.perf_counter()
    rate = 1000 * (end - start) / len(analyzers)
    print(f"Searched {len(analyzers)} files in {base} at {rate:.3f}ms/file")


if __name__ == "__main__":
    options = get_options()
    for path in options.path:
        main(path)
