"""
Python 3 Object-Oriented Programming

Chapter 9. Strings and Serialization
"""
from pathlib import Path
from typing import Callable


def scan_python_1(path: Path) -> int:
    sloc = 0
    with path.open() as source:
        for line in source:
            line = line.strip()
            if line and not line.startswith("#"):
                sloc += 1
    return sloc


def scan_python_2(path: Path) -> int:
    with path.open() as source:
        partitioned = (line.partition("#") for line in source)
        code_only = (code.strip() for code, _, comment in partitioned)
        non_empty = filter(None, code_only)
        sloc = sum(1 for line in non_empty)
    return sloc


import ast


class StatementVisitor(ast.NodeVisitor):
    def __init__(self) -> None:
        self.sloc = 0

    def visit_statement(self, node: ast.AST) -> None:
        self.sloc += 1
        super().generic_visit(node)


for classname in (
    "FunctionDef",
    "AsyncFunctionDef",
    "ClassDef",
    "Return",
    "Delete",
    "Assign",
    "AugAssign",
    "AnnAssign",
    "For",
    "AsyncFor",
    "While",
    "If",
    "With",
    "AsyncWith",
    "Raise",
    "Try",
    "Assert",
    "Import",
    "ImportFrom",
    "Global",
    "Nonlocal",
    "Expr",
    "Pass",
    "Break",
    "Continue",
):
    setattr(StatementVisitor, f"visit_{classname}", StatementVisitor.visit_statement)


def scan_python_3(path: Path) -> int:
    stmt_count = StatementVisitor()
    with path.open() as source:
        code = ast.parse(source.read(), str(path))
        stmt_count.visit(code)
    return stmt_count.sloc


def count_sloc(path: Path, scanner: Callable[[Path], int]) -> int:
    if path.name.startswith("."):
        return 0
    elif path.is_file():
        if path.suffix != ".py":
            return 0
        with path.open() as source:
            return scanner(path)
    elif path.is_dir():
        count = sum(count_sloc(name, scanner) for name in path.iterdir())
        return count
    else:
        return 0


test_ch_02 = """
>>> base = Path.cwd().parent
>>> chapter =  base / "ch_02"
>>> count = count_sloc(chapter, scan_python_1)
>>> print(
...     f"{chapter.relative_to(base)}: {count} lines of code"
... )
ch_02: 545 lines of code

>>> count = count_sloc(chapter, scan_python_2)
>>> count 
545

>>> count = count_sloc(chapter, scan_python_3)
>>> print(
...     f"{chapter.relative_to(base)}: {count} statements"
... )
ch_02: 260 statements

"""

__test__ = {name: case for name, case in globals().items() if name.startswith("test_")}
