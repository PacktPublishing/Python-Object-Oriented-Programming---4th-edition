# Python 3 Object-Oriented Programming

Chapter 10. The Iterator Pattern

## Design patterns in brief

## Iterators

## Comprehensions

### List comprehensions

```python

>>> input_strings = ["1", "5", "28", "131", "3"]
 
>>> output_integers = [] 
>>> for num in input_strings: 
...    output_integers.append(int(num)) 
>>> output_integers
[1, 5, 28, 131, 3]

```

```python

>>> input_strings = ["1", "5", "28", "131", "3"]
 
>>> output_integers = [int(num) for num in input_strings] 
>>> output_integers
[1, 5, 28, 131, 3]

```

```python
>>> input_strings = ["1", "5", "28", "131", "3"]
>>> output_integers = [int(num) for num in input_strings if len(num) < 3]
>>> output_integers
[1, 5, 28, 3]

```

```python
>>> from pathlib import Path, PosixPath, WindowsPath

>>> chapter = Path.cwd()
>>> paths = [path.relative_to(chapter) 
...     for path in chapter.glob("src/*.py") 
...     if ">>>" in path.read_text()
... ]
>>> paths.sort()
>>> import sys
>>> assert (
...     paths == [Path('src/iterator_protocol.py'), Path('src/log_analysis.py'), Path('src/model.py')]
... ), f"Invalid {paths!r} for {sys.platform!r}"

>>> source_path = Path('src') / 'iterator_protocol.py'
>>> with source_path.open() as source:
...     examples = [line.rstrip() 
...         for line in source 
...         if ">>>" in line]
>>> examples
[">>> iterable = CapitalIterable('the quick brown fox jumps over the lazy dog')", '>>> iterator = iter(iterable)', '>>> while True:', '>>> for i in iterable:', '>>> iterator = iter(iterable)', '>>> for i in iter(iterator):']

>>> source_path = Path('src') / 'iterator_protocol.py'
>>> with source_path.open() as source:
...     examples = [(number, line.rstrip()) 
...         for number, line in enumerate(source, start=1) 
...         if ">>>" in line]
>>> examples
[(35, ">>> iterable = CapitalIterable('the quick brown fox jumps over the lazy dog')"), (36, '>>> iterator = iter(iterable)'), (37, '>>> while True:'), (53, '>>> for i in iterable:'), (66, '>>> iterator = iter(iterable)'), (67, '>>> for i in iter(iterator):')]

>>> import doctest
>>> import iterator_protocol
>>> test_finder = doctest.DocTestFinder()
>>> [test.name for test in test_finder.find(iterator_protocol)]
['iterator_protocol', 'iterator_protocol.__test__.test_iterable']


```

### Set and dictionary comprehensions

```python

>>> from typing import NamedTuple

>>> class Book(NamedTuple):
...     author: str
...     title: str
...     genre: str

>>> books = [
...     Book("Pratchett", "Nightwatch", "fantasy"),
...     Book("Pratchett", "Thief Of Time", "fantasy"),
...     Book("Le Guin", "The Dispossessed", "scifi"),
...     Book("Le Guin", "A Wizard Of Earthsea", "fantasy"),
...     Book("Jemisin", "The Broken Earth", "fantasy"),
...     Book("Turner", "The Thief", "fantasy"),
...     Book("Phillips", "Preston Diamond", "western"),
...     Book("Phillips", "Twice Upon A Time", "scifi"),
... ]

>>> fantasy_authors = {b.author for b in books if b.genre == "fantasy"}
>>> fantasy_authors == {'Pratchett', 'Le Guin', 'Turner', 'Jemisin'}
True

>>> fantasy_titles = {b.title: b for b in books if b.genre == "fantasy"}
>>> fantasy_titles
{'Nightwatch': Book(author='Pratchett', title='Nightwatch', genre='fantasy'), 'Thief Of Time': Book(author='Pratchett', title='Thief Of Time', genre='fantasy'), 'A Wizard Of Earthsea': Book(author='Le Guin', title='A Wizard Of Earthsea', genre='fantasy'), 'The Broken Earth': Book(author='Jemisin', title='The Broken Earth', genre='fantasy'), 'The Thief': Book(author='Turner', title='The Thief', genre='fantasy')}
>>> fantasy_titles['Nightwatch']
Book(author='Pratchett', title='Nightwatch', genre='fantasy')


```

## Generator expressions

```python
>>> from pathlib import Path

>>> full_log_path = Path.cwd() / "data" / "sample.log"
>>> warning_log_path = Path.cwd() / "data" / "warnings.log"

>>> with full_log_path.open() as source:
...     warning_lines = (line for line in source if "WARN" in line)
...     with warning_log_path.open('w') as target:
...         for line in warning_lines:
...             _ = target.write(line)

>>> with warning_log_path.open() as warnings:
...     for line in warnings:
...         print(line.rstrip())
Apr 05, 2021 20:03:53 WARNING This is a warning. It could be serious.
Apr 05, 2021 20:03:59 WARNING Another warning sent.
Apr 05, 2021 20:04:35 WARNING Warnings should be heeded.
Apr 05, 2021 20:04:41 WARNING Watch for warnings.



```
