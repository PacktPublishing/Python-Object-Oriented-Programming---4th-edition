"""
Python 3 Object-Oriented Programming

Chapter 14.  Concurrency

How long does a "simple" write take?
"""
import timeit
from textwrap import dedent
import random
import string
from pathlib import Path

repeat_count = 5_000_000
for message_size in (128, 256, 512, 1024):
    log_message = ''.join(random.choice(string.printable) for _ in range(message_size))
    t = timeit.timeit(
        stmt="some_file.write(log_message)",
        setup=dedent(
            """
            some_path = Path("temp_file.log")
            some_file = some_path.open('w')
            """
        ),
        number=repeat_count,
        globals=globals()
    )
    print(f"Time to write {message_size} character line {t/repeat_count*1_000_000:.6f}μs")
