"""
Python 3 Object-Oriented Programming

Chapter 6, Abstract Base Classes and Operator Overloading
"""
from __future__ import annotations
from contextlib import AbstractContextManager
from io import StringIO
import sys
from typing import Type, Literal, Optional
from types import TracebackType


if sys.version_info >= (3, 9):
    # Python 3.9 with revised generics
    class DebuggingOnly(AbstractContextManager["DebuggingOnly"]):
        """Similar to contextlib.redirect_stdout"""

        def __enter__(self) -> "DebuggingOnly":
            self.previous = sys.stdout
            self.buffer = StringIO()
            sys.stdout = self.buffer
            return self

        def __exit__(
            self,
            exc_class: Optional[Type[BaseException]],
            exc: Optional[BaseException],
            exc_tb: Optional[TracebackType],
        ) -> Literal[False]:
            sys.stdout = self.previous
            if exc:
                print(f"--EX-->{exc!r}")
                for line in self.buffer.getvalue().splitlines():
                    print(f"       {line}")
            return False


else:
    # Python 3.8 expected this.
    from typing import ContextManager

    class DebuggingOnly(ContextManager["DebuggingOnly"]):
        """Similar to contextlib.redirect_stdout"""

        def __enter__(self) -> "DebuggingOnly":
            self.previous = sys.stdout
            self.buffer = StringIO()
            sys.stdout = self.buffer
            return self

        def __exit__(
            self,
            exc_class: Optional[Type[BaseException]],
            exc: Optional[BaseException],
            exc_tb: Optional[TracebackType],
        ) -> Literal[False]:
            sys.stdout = self.previous
            if exc:
                print(f"--EX-->{exc!r}")
                for line in self.buffer.getvalue().splitlines():
                    print(f"       {line}")
            return False
