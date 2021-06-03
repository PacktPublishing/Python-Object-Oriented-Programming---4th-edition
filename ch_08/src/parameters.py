"""
Python 3 Object-Oriented Programming

Chapter 8. The Intersection of Object-Oriented and Functional Programming
"""
from __future__ import annotations
from typing import Any, Optional


def no_params() -> str:
    return "Hello, world!"


test_no_params = """
>>> no_params()
'Hello, world!'
"""

from typing import Any


def mandatory_params(x: Any, y: Any, z: Any) -> str:
    return f"{x=}, {y=}, {z=}"


test_mandatory_params = """
>>> a_variable = 42
>>> mandatory_params("a string", a_variable, True)
"x='a string', y=42, z=True"
"""


def default_params(
    x: Any, y: Any, z: Any, a: str = "Some String", b: bool = False
) -> str:
    return f"{x=}, {y=}, {z=}, {a=}, {b=}"
    pass


test_default_params = """
>>> variable = 3.14159
>>> default_params("a string", variable, 8, "", True) 
"x='a string', y=3.14159, z=8, a='', b=True"

>>> some_variable = 42
>>> default_params("a longer string", some_variable, 14) 
"x='a longer string', y=42, z=14, a='Some String', b=False"

>>> variable = 3.14159
>>> default_params("a string", variable, 14, b=True) 
"x='a string', y=3.14159, z=14, a='Some String', b=True"

>>> default_params(y=1, z=2, x=3, a="hi")
"x=3, y=1, z=2, a='hi', b=False"

"""


def latitude_dms(
    deg: float, min: float, sec: float = 0.0, dir: Optional[str] = None
) -> str:
    if dir is None:
        dir = "N"
    return f"{deg:02.0f}° {min+sec/60:05.3f}{dir}"


test_latitude = """
>>> latitude_dms(36, 51, 2.9, "N")
'36° 51.048N'
>>> latitude_dms(38, 58, dir="N")
'38° 58.000N'
>>> latitude_dms(38, 19, dir="N", sec=7)
'38° 19.117N'
"""


def kw_only(x: Any, y: str = "defaultkw", *, a: bool, b: str = "only") -> str:
    return f"{x=}, {y=}, {a=}, {b=}"


test_kw_only = """
This function fails if you don't pass a:
>>> kw_only('x')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: kw_only() missing 1 required keyword-only argument: 'a'

It also fails if you pass a as a positional argument:
>>> kw_only('x', 'y', 'a')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: kw_only() takes from 1 to 2 positional arguments but 3 were given

But you can pass a and b as keyword arguments:
>>> kw_only('x', a='a', b='b')
"x='x', y='defaultkw', a='a', b='b'"

"""


def pos_only(x: Any, y: str, /, z: Optional[Any] = None) -> str:
    return f"{x=}, {y=}, {z=}"


test_pos_only = """
>>> pos_only(x=2, y="three")
Traceback (most recent call last):
  ...
  File "<doctest hint_examples.__test__.test_pos_only[0]>", line 1, in <module>
    pos_only(x=2, y="three")
TypeError: pos_only() got some positional-only arguments passed as keyword arguments: 'x, y'

>>> pos_only(2, "three")
"x=2, y='three', z=None"

>>> pos_only(2, "three", 3.14159) 
"x=2, y='three', z=3.14159"

"""

number = 5


def funky_function(x: int = number) -> str:
    return f"{x=}, {number=}"


test_funky_function = """
>>> funky_function(42)
'x=42, number=5'

>>> number = 7
>>> funky_function()
'x=5, number=5'
"""


def better_function(x: Optional[int] = None) -> str:
    if x is None:
        x = number
    return f"better: {x=}, {number=}"


test_better_function = """
See the examples.md. This can't easily be tested
here because doctest examples don't set global variables.
"""


def better_function_2(x: Optional[int] = None) -> str:
    x = number if x is None else x
    return f"better: {x=}, {number=}"


def bad_default(tag: str, history: list[str] = []) -> list[str]:
    """A Very Bad Design (VBD™)."""
    history.append(tag)
    return history


test_bad_default = """
>>> h = bad_default("tag1")
>>> h = bad_default("tag2", h)
>>> h
['tag1', 'tag2']

>>> h2 = bad_default("tag21")
>>> h2 = bad_default("tag22", h2)
>>> h2
['tag1', 'tag2', 'tag21', 'tag22']

>>> h
['tag1', 'tag2', 'tag21', 'tag22']
>>> h is h2
True

"""


def good_default(tag: str, history: Optional[list[str]] = None) -> list[str]:
    history = [] if history is None else history
    history.append(tag)
    return history


test_good_default = """
>>> h = good_default("tag1")
>>> h = good_default("tag2", h)
>>> h
['tag1', 'tag2']

>>> h2 = good_default("tag21")
>>> h2 = good_default("tag22", h2)
>>> h2
['tag21', 'tag22']

>>> h is h2
False

"""


from urllib.parse import urlparse
from pathlib import Path


def get_pages(*links: str) -> None:
    for link in links:
        url = urlparse(link)
        name = "index.html" if url.path in ("", "/") else url.path
        target = Path(url.netloc.replace(".", "_")) / name
        print(f"Create {target} from {link!r}")
        # etc.


test_get_pages = """
>>> get_pages()
 
>>> get_pages('https://www.archlinux.org') 
Create www_archlinux_org...index.html from 'https://www.archlinux.org'

>>> get_pages('https://www.archlinux.org', 
...        'https://dusty.phillips.codes',
...        'https://itmaybeahack.com'
... ) 
Create www_archlinux_org...index.html from 'https://www.archlinux.org'
Create dusty_phillips_codes...index.html from 'https://dusty.phillips.codes'
Create itmaybeahack_com...index.html from 'https://itmaybeahack.com'

"""


from typing import Dict, Any


class Options(Dict[str, Any]):
    default_options: dict[str, Any] = {
        "port": 21,
        "host": "localhost",
        "username": None,
        "password": None,
        "debug": False,
    }

    def __init__(self, **kwargs: Any) -> None:
        # super().__init__(self.default_options)
        # self.update(kwargs)
        super().__init__({**self.default_options, **kwargs})


test_options = """
>>> options = Options(username="dusty", password="Hunter2",
...     debug=True)
>>> options['debug']
True
>>> options['port']
21
>>> options['username']
'dusty'

>>> Options.default_options
{'port': 21, 'host': 'localhost', 'username': None, 'password': None, 'debug': False}

"""

import contextlib
import os
import subprocess
import sys
from typing import TextIO
from pathlib import Path


def doctest_everything(
    output: TextIO, *directories: Path, verbose: bool = False, **stems: str
) -> None:
    def log(*args: Any, **kwargs: Any) -> None:
        if verbose:
            print(*args, **kwargs)

    with contextlib.redirect_stdout(output):
        for directory in directories:
            log(f"Searching {directory}")
            for path in directory.glob("**/*.md"):
                if any(parent.stem == ".tox" for parent in path.parents):
                    continue
                log(f"File {path.relative_to(directory)}, " f"{path.stem=}")
                if stems.get(path.stem, "").upper() == "SKIP":
                    log("Skipped")
                    continue
                options = []
                if stems.get(path.stem, "").upper() == "ELLIPSIS":
                    options += ["ELLIPSIS"]
                search_path = directory / "src"
                print(
                    f"cd '{Path.cwd()}'; "
                    f"PYTHONPATH='{search_path}' doctest '{path}' -v"
                )
                option_args = ["-o", ",".join(options)] if options else []
                subprocess.run(
                    ["python3", "-m", "doctest", "-v"] + option_args + [str(path)],
                    cwd=directory,
                    env={"PYTHONPATH": str(search_path)},
                )


if __name__ == "__main__":
    doctest_everything(
        sys.stdout,
        Path.cwd() / "ch_02",
        Path.cwd() / "ch_03",
        examples="ELLIPSIS",
        examples_38="SKIP",
        case_study_2="SKIP",
        case_study_3="SKIP",
    )
    print()
    print("---REDIRECT---")
    doctest_log = Path("doctest.log")
    with doctest_log.open("w") as log:
        doctest_everything(
            log, Path.cwd() / "ch_04", Path.cwd() / "ch_05", verbose=True
        )
    print(doctest_log.read_text())

__test__ = {name: case for name, case in globals().items() if name.startswith("test_")}
