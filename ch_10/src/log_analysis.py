"""
Python 3 Object-Oriented Programming

Chapter 10. The Iterator Pattern
"""
from __future__ import annotations
import csv
import re
from pathlib import Path
from typing import Match, cast, Sequence


def extract_and_parse_1(full_log_path: Path, warning_log_path: Path) -> None:
    with warning_log_path.open("w", newline="") as target:
        writer = csv.writer(target, delimiter="\t")
        pattern = re.compile(r"(\w\w\w \d\d, \d\d\d\d \d\d:\d\d:\d\d) (\w+) (.*)")
        with full_log_path.open() as source:
            for line in source:
                if "WARN" in line:
                    line_groups = cast(Match[str], pattern.match(line)).groups()
                    writer.writerow(line_groups)


test_extract_and_parse_1 = """
>>> from pathlib import Path
>>> full_log_path = Path.cwd() / "data" / "sample.log"
>>> warning_log_path = Path.cwd() / "data" / "warnings1.tab"
>>> extract_and_parse_1(full_log_path, warning_log_path)

>>> list(filter(None, warning_log_path.read_text().splitlines()))
['Apr 05, 2021 20:03:53\\tWARNING\\tThis is a warning. It could be serious.', 'Apr 05, 2021 20:03:59\\tWARNING\\tAnother warning sent.', 'Apr 05, 2021 20:04:35\\tWARNING\\tWarnings should be heeded.', 'Apr 05, 2021 20:04:41\\tWARNING\\tWatch for warnings.']

"""

import csv
import re
from pathlib import Path
from typing import Match, cast, Iterator, Tuple, TextIO


class WarningReformat(Iterator[Tuple[str, ...]]):
    pattern = re.compile(r"(\w\w\w \d\d, \d\d\d\d \d\d:\d\d:\d\d) (\w+) (.*)")

    def __init__(self, source: TextIO) -> None:
        self.insequence = source

    def __iter__(self) -> Iterator[tuple[str, ...]]:
        return self

    def __next__(self) -> tuple[str, ...]:
        line = self.insequence.readline()
        while line and "WARN" not in line:
            line = self.insequence.readline()
        if not line:
            raise StopIteration
        else:
            return tuple(cast(Match[str], self.pattern.match(line)).groups())


def extract_and_parse_2(full_log_path: Path, warning_log_path: Path) -> None:
    with warning_log_path.open("w", newline="") as target:
        writer = csv.writer(target, delimiter="\t")
        with full_log_path.open() as source:
            filter_reformat = WarningReformat(source)
            for line_groups in filter_reformat:
                writer.writerow(line_groups)


test_extract_and_parse_2 = """
>>> from pathlib import Path
>>> full_log_path = Path.cwd() / "data" / "sample.log"
>>> warning_log_path = Path.cwd() / "data" / "warnings2.tab"
>>> extract_and_parse_2(full_log_path, warning_log_path)

>>> list(filter(None, warning_log_path.read_text().splitlines()))
['Apr 05, 2021 20:03:53\\tWARNING\\tThis is a warning. It could be serious.', 'Apr 05, 2021 20:03:59\\tWARNING\\tAnother warning sent.', 'Apr 05, 2021 20:04:35\\tWARNING\\tWarnings should be heeded.', 'Apr 05, 2021 20:04:41\\tWARNING\\tWatch for warnings.']

"""

import csv
import re
from pathlib import Path
from typing import Match, cast, Iterator, Iterable


def warnings_filter(source: Iterable[str]) -> Iterator[tuple[str, ...]]:
    pattern = re.compile(r"(\w\w\w \d\d, \d\d\d\d \d\d:\d\d:\d\d) (\w+) (.*)")
    for line in source:
        if "WARN" in line:
            yield tuple(cast(Match[str], pattern.match(line)).groups())


def extract_and_parse_3(full_log_path: Path, warning_log_path: Path) -> None:
    with warning_log_path.open("w", newline="") as target:
        writer = csv.writer(target, delimiter="\t")
        with full_log_path.open() as infile:
            filter = warnings_filter(infile)
            for line_groups in filter:
                writer.writerow(line_groups)


test_extract_and_parse_3 = """
>>> from pathlib import Path
>>> full_log_path = Path.cwd() / "data" / "sample.log"
>>> warning_log_path = Path.cwd() / "data" / "warnings3.tab"
>>> extract_and_parse_3(full_log_path, warning_log_path)

>>> list(filter(None, warning_log_path.read_text().splitlines()))
['Apr 05, 2021 20:03:53\\tWARNING\\tThis is a warning. It could be serious.', 'Apr 05, 2021 20:03:59\\tWARNING\\tAnother warning sent.', 'Apr 05, 2021 20:04:35\\tWARNING\\tWarnings should be heeded.', 'Apr 05, 2021 20:04:41\\tWARNING\\tWatch for warnings.']

"""


def extract_and_parse_g(full_log_path: Path, warning_log_path: Path) -> None:
    with warning_log_path.open("w", newline="") as target:
        writer = csv.writer(target, delimiter="\t")
        pattern = re.compile(r"(\w\w\w \d\d, \d\d\d\d \d\d:\d\d:\d\d) (\w+) (.*)")
        with full_log_path.open() as source:
            warnings_filter = (
                tuple(cast(Match[str], pattern.match(line)).groups())
                for line in source
                if "WARN" in line
            )
            for line_groups in warnings_filter:
                writer.writerow(line_groups)


test_extract_and_parse_g = """
>>> from pathlib import Path
>>> full_log_path = Path.cwd() / "data" / "sample.log"
>>> warning_log_path = Path.cwd() / "data" / "warnings_g.tab"
>>> extract_and_parse_g(full_log_path, warning_log_path)

>>> list(filter(None, warning_log_path.read_text().splitlines()))
['Apr 05, 2021 20:03:53\\tWARNING\\tThis is a warning. It could be serious.', 'Apr 05, 2021 20:03:59\\tWARNING\\tAnother warning sent.', 'Apr 05, 2021 20:04:35\\tWARNING\\tWarnings should be heeded.', 'Apr 05, 2021 20:04:41\\tWARNING\\tWatch for warnings.']

"""

test_multiline_extract_and_parse_g = """
>>> from pathlib import Path
>>> full_log_path = Path.cwd() / "data" / "multiline.log"
>>> warning_log_path = Path.cwd() / "data" / "warnings_gf.tab"
>>> extract_and_parse_g(full_log_path, warning_log_path)
Traceback (most recent call last):
  ...
  File "<doctest log_analysis.__test__.test_multiline_extract_and_parse_g[3]>", line 1, in <module>
    extract_and_parse_g(full_log_path, warning_log_path)
  File "src/log_analysis.py", line 123, in extract_and_parse_g
    for line_groups in warnings_filter:
  File "src/log_analysis.py", line 119, in <genexpr>
    tuple(cast(Match[str], pattern.match(line)).groups())
AttributeError: 'NoneType' object has no attribute 'groups'

>>> list(filter(None, warning_log_path.read_text().splitlines()))
['Apr 05, 2021 20:05:25\\tWARNING\\tThis is a warning. It could be serious.', 'Apr 05, 2021 20:05:31\\tWARNING\\tAnother warning sent.']

"""


def extract_and_parse_g1(full_log_path: Path, warning_log_path: Path) -> None:
    def warnings_filter(source: Iterable[str]) -> Iterator[Sequence[str]]:
        pattern = re.compile(r"(\w\w\w \d\d, \d\d\d\d \d\d:\d\d:\d\d) (\w+) (.*)")
        for line in source:
            if match := pattern.match(line):
                if "WARN" in match.group(2):
                    yield match.groups()

    with warning_log_path.open("w") as target:
        writer = csv.writer(target, delimiter="\t")
        with full_log_path.open() as source:
            for line_groups in warnings_filter(source):
                writer.writerow(line_groups)


test_extract_and_parse_g1 = """
>>> from pathlib import Path
>>> full_log_path = Path.cwd() / "data" / "sample.log"
>>> warning_log_path = Path.cwd() / "data" / "warnings_g1.tab"
>>> extract_and_parse_g1(full_log_path, warning_log_path)

>>> list(filter(None, warning_log_path.read_text().splitlines()))
['Apr 05, 2021 20:03:53\\tWARNING\\tThis is a warning. It could be serious.', 'Apr 05, 2021 20:03:59\\tWARNING\\tAnother warning sent.', 'Apr 05, 2021 20:04:35\\tWARNING\\tWarnings should be heeded.', 'Apr 05, 2021 20:04:41\\tWARNING\\tWatch for warnings.']

"""

import csv
import re
from pathlib import Path
from typing import Match, cast, Iterator, Iterable


def file_extract(path_iter: Iterable[Path]) -> Iterator[tuple[str, ...]]:
    for path in path_iter:
        with path.open() as infile:
            yield from warnings_filter(infile)


def extract_and_parse_d(directory: Path, warning_log_path: Path) -> None:
    with warning_log_path.open("w", newline="") as target:
        writer = csv.writer(target, delimiter="\t")
        log_files = list(directory.glob("sample*.log"))
        for line_groups in file_extract(log_files):
            writer.writerow(line_groups)


test_extract_and_parse_d = """
>>> from pathlib import Path
>>> log_directory_path = Path.cwd() / "data"
>>> warning_log_path = Path.cwd() / "data" / "warnings_d.tab"
>>> extract_and_parse_d(log_directory_path, warning_log_path)

>>> list(filter(None, warning_log_path.read_text().splitlines()))
['Apr 05, 2021 20:03:53\\tWARNING\\tThis is a warning. It could be serious.', 'Apr 05, 2021 20:03:59\\tWARNING\\tAnother warning sent.', 'Apr 05, 2021 20:04:35\\tWARNING\\tWarnings should be heeded.', 'Apr 05, 2021 20:04:41\\tWARNING\\tWatch for warnings.']

"""


def extract_and_parse_g2(full_log_path: Path, warning_log_path: Path) -> None:
    with warning_log_path.open("w", newline="") as target:
        writer = csv.writer(target, delimiter="\t")
        pattern = re.compile(r"(\w\w\w \d\d, \d\d\d\d \d\d:\d\d:\d\d) (\w+) (.*)")
        with full_log_path.open() as source:
            possible_match_iter = (pattern.match(line) for line in source)
            group_iter = (match.groups() for match in possible_match_iter if match)
            warnings_filter = (group for group in group_iter if "WARN" in group[1])
            writer.writerows(warnings_filter)


test_extract_and_parse_g2 = """
>>> from pathlib import Path
>>> full_log_path = Path.cwd() / "data" / "sample.log"
>>> warning_log_path = Path.cwd() / "data" / "warnings_g2.tab"
>>> extract_and_parse_g2(full_log_path, warning_log_path)

>>> list(filter(None, warning_log_path.read_text().splitlines()))  # sample
['Apr 05, 2021 20:03:53\\tWARNING\\tThis is a warning. It could be serious.', 'Apr 05, 2021 20:03:59\\tWARNING\\tAnother warning sent.', 'Apr 05, 2021 20:04:35\\tWARNING\\tWarnings should be heeded.', 'Apr 05, 2021 20:04:41\\tWARNING\\tWatch for warnings.']

>>> from pathlib import Path
>>> full_log_path = Path.cwd() / "data" / "multiline.log"
>>> warning_log_path = Path.cwd() / "data" / "warnings_g2f.tab"
>>> extract_and_parse_g2(full_log_path, warning_log_path)

>>> list(filter(None, warning_log_path.read_text().splitlines()))  # multiline
['Apr 05, 2021 20:05:25\\tWARNING\\tThis is a warning. It could be serious.', 'Apr 05, 2021 20:05:31\\tWARNING\\tAnother warning sent.', 'Apr 05, 2021 20:06:10\\tWARNING\\tWarnings should be heeded.', 'Apr 05, 2021 20:06:16\\tWARNING\\tWatch for warnings.']

"""

import datetime


def extract_and_parse_g3(full_log_path: Path, warning_log_path: Path) -> None:
    with warning_log_path.open("w", newline="") as target:
        writer = csv.writer(target, delimiter="\t")
        pattern = re.compile(
            r"(?P<dt>\w\w\w \d\d, \d\d\d\d \d\d:\d\d:\d\d)"
            r"\s+(?P<level>\w+)"
            r"\s+(?P<msg>.*)"
        )
        with full_log_path.open() as source:
            possible_match_iter = (pattern.match(line) for line in source)
            group_iter = (match.groupdict() for match in possible_match_iter if match)
            warnings_iter = (group for group in group_iter if "WARN" in group["level"])
            dt_iter = (
                (
                    datetime.datetime.strptime(g["dt"], "%b %d, %Y %H:%M:%S"),
                    g["level"],
                    g["msg"],
                )
                for g in warnings_iter
            )
            warnings_filter = ((g[0].isoformat(), g[1], g[2]) for g in dt_iter)
            writer.writerows(warnings_filter)


test_extract_and_parse_g3 = """
>>> from pathlib import Path
>>> full_log_path = Path.cwd() / "data" / "sample.log"
>>> warning_log_path = Path.cwd() / "data" / "warnings_g3.tab"
>>> extract_and_parse_g3(full_log_path, warning_log_path)

>>> list(filter(None, warning_log_path.read_text().splitlines()))
['2021-04-05T20:03:53\\tWARNING\\tThis is a warning. It could be serious.', '2021-04-05T20:03:59\\tWARNING\\tAnother warning sent.', '2021-04-05T20:04:35\\tWARNING\\tWarnings should be heeded.', '2021-04-05T20:04:41\\tWARNING\\tWatch for warnings.']

"""


def extract_and_parse_g4(full_log_path: Path, warning_log_path: Path) -> None:
    with warning_log_path.open("w") as target:
        writer = csv.writer(target, delimiter="\t")
        pattern = re.compile(
            r"(?P<dt>\w\w\w \d\d, \d\d\d\d \d\d:\d\d:\d\d)"
            r"\s+(?P<level>\w+)"
            r"\s+(?P<msg>.*)"
        )
        with full_log_path.open() as source:
            possible_match_iter = map(pattern.match, source)
            good_match_iter = filter(None, possible_match_iter)
            group_iter = map(lambda m: m.groupdict(), good_match_iter)
            warnings_iter = filter(lambda g: "WARN" in g["level"], group_iter)
            dt_iter = map(
                lambda g: (
                    datetime.datetime.strptime(g["dt"], "%b %d, %Y %H:%M:%S"),
                    g["level"],
                    g["msg"],
                ),
                warnings_iter,
            )
            warnings_filter = map(lambda g: (g[0].isoformat(), g[1], g[2]), dt_iter)
            writer.writerows(warnings_filter)


test_extract_and_parse_g4 = """
>>> from pathlib import Path
>>> full_log_path = Path.cwd() / "data" / "sample.log"
>>> warning_log_path = Path.cwd() / "data" / "warnings_g3.tab"
>>> extract_and_parse_g4(full_log_path, warning_log_path)

>>> list(filter(None, warning_log_path.read_text().splitlines()))
['2021-04-05T20:03:53\\tWARNING\\tThis is a warning. It could be serious.', '2021-04-05T20:03:59\\tWARNING\\tAnother warning sent.', '2021-04-05T20:04:35\\tWARNING\\tWarnings should be heeded.', '2021-04-05T20:04:41\\tWARNING\\tWatch for warnings.']

"""

__test__ = {name: case for name, case in globals().items() if name.startswith("test_")}
