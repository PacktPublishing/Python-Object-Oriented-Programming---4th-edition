"""
Python 3 Object-Oriented Programming

Chapter 11. Common Design Patterns
"""
import logging
import time
from typing import Callable, Any
from functools import reduce
from operator import mul
from functools import wraps


def log_args(function: Callable[..., Any]) -> Callable[..., Any]:
    @wraps(function)
    def wrapped_function(*args: Any, **kwargs: Any) -> Any:
        print(f"Calling {function.__name__}(*{args}, **{kwargs})")
        result = function(*args, **kwargs)
        return result

    return wrapped_function


def log_time(function: Callable[..., Any]) -> Callable[..., Any]:
    @wraps(function)
    def wrapped_function(*args: Any, **kwargs: Any) -> Any:
        start = time.perf_counter()
        result = function(*args, **kwargs)
        microseconds = (time.perf_counter() - start) * 1_000_000
        print(f"Executed {function.__name__} in {microseconds:.1f}μs")
        return result

    return wrapped_function


def test1(a: int, b: int, c: int) -> float:
    return sum(range(a, b + 1)) / c


def test2(a: float, b: int) -> float:
    if b == 0:
        return 1.0
    elif b % 2 == 0:
        x = test2(a, b // 2)
        return x * x
    else:
        return a * test2(a, b - 1)


def test3(a: float, b: int) -> float:
    return reduce(mul, (a for _ in range(1, b + 1)), 1)


test_log_args = """
>>> test1 = log_args(test1)
>>> test1(1, 9, 2)
Calling test1(*(1, 9, 2), **{})
22.5

>>> @log_args
... def test1(a: int, b: int, c: int) -> float:
...     return sum(range(a, b + 1)) / c
>>> test1(1, 9, 2)
Calling test1(*(1, 9, 2), **{})
22.5

"""

test_log_time = """
>>> test1 = log_time(test1)
>>> test1(1, 2, 3)
Executed test1 in ...μs
1.0

"""

test_log_time_args = """
>>> test1 = log_time(log_args(test1))
>>> test1(1, 2, 3)
Calling test1(*(1, 2, 3), **{})
Executed test1 in ...μs
1.0

"""


class NamedLogger:
    def __init__(self, logger_name: str) -> None:
        self.logger = logging.getLogger(logger_name)

    def __call__(self, function: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(function)
        def wrapped_function(*args: Any, **kwargs: Any) -> Any:
            start = time.perf_counter()
            try:
                result = function(*args, **kwargs)
                μs = (time.perf_counter() - start) * 1_000_000
                self.logger.info(f"{function.__name__}, {μs:.1f}μs")
                return result
            except Exception as ex:
                μs = (time.perf_counter() - start) * 1_000_000
                self.logger.error(f"{ex}, {function.__name__}, {μs:.1f}μs")
                raise

        return wrapped_function


test_named_log = """
>>> @NamedLogger("log4")
... def test4(median: float, sample: float) -> float:
...     return abs(sample-median)

>>> test4(12, 14)
2
>>> test4("hello", "world")
Traceback (most recent call last):
...
  File "<doctest decorations.__test__.test_named_log[0]>", line 3, in test4
    return abs(sample-median)
TypeError: unsupported operand type(s) for -: 'str' and 'str'

"""


def test4(median: float, sample: float) -> float:
    return abs(sample - median)


__test__ = {name: case for name, case in globals().items() if name.startswith("test_")}

if __name__ == "__main__":
    test1 = log_args(test1)
    test2 = log_args(test2)
    test3 = log_args(test3)

    test1(1, 2, 3)
    test2(4, b=5)
    test3(6, 7)

    test1 = log_time(test1)
    test2 = log_time(test2)
    test3 = log_time(test3)

    test1(1, 2, 3)
    test2(4, b=5)
    test3(6, 7)

    test4 = NamedLogger("log4")(test4)
    test4(12, 14)
    test4("hello", "world")
