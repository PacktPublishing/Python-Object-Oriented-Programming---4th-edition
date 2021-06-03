# Python 3 Object-Oriented Programming

Chapter 7. Python Data Structures

## Empty Objects

```python
>>> o = object()
>>> o.x = 5
Traceback (most recent call last):
  ...
  File "<stdin>", line 1, in <module>
AttributeError: 'object' object has no attribute 'x'

```

```python
>>> class MyObject: 
...     pass 
>>> m = MyObject()
>>> m.x = "hello"
>>> m.x
'hello'

```

## Tuples and named tuples

```python
>>> stock = "AAPL", 123.52, 137.98, 53.15
>>> stock2 = ("AAPL", 123.52, 137.98, 53.15)
>>> stock == stock2
True
>>> stock
('AAPL', 123.52, 137.98, 53.15)

>>> a = 42,
>>> a
(42,)

>>> b = (42, 3.14), (2.718, 2.618), 
>>> b
((42, 3.14), (2.718, 2.618))

>>> import datetime
>>> def middle(stock, date):
...     symbol, current, high, low = stock
...     return ((high + low) / 2), date
>>> middle(("AAPL", 123.52, 137.98, 53.15), datetime.date(2020, 12, 4))
(95.565, datetime.date(2020, 12, 4))

>>> s = "AAPL", 132.76, 134.80, 130.53
>>> high = s[2]
>>> high
134.8
>>> s[1:3]
(132.76, 134.8)

>>> def high(stock):
...     symbol, current, high, low = stock
...     return high
>>> high(s)
134.8

```

## Named tuples via typing.NamedTuple

```python
>>> from typing import NamedTuple
>>> class Stock(NamedTuple):
...     symbol: str
...     current: float
...     high: float
...     low: float
>>> s = Stock("AAPL", 123.52, 137.98, 53.15)
>>> s.high
137.98
>>> s[2]
137.98
>>> symbol, current, high, low = s
>>> current
123.52

>>> s = Stock("AAPL", 123.52, high=137.98, low=53.15)
>>> s.current = 122.25
Traceback (most recent call last):
  ...
  File "<doctest examples.md[27]>", line 1, in <module>
    s2.current = 122.25
AttributeError: can't set attribute


```

```python
>>> t = ("Relayer", ["Gates of Delirium", "Sound Chaser"])
>>> t[1].append("To Be Over")
>>> t
('Relayer', ['Gates of Delirium', 'Sound Chaser', 'To Be Over'])

>>> hash(t)
Traceback (most recent call last):
  ...
  File "<doctest examples.md[31]>", line 1, in <module>
    hash(t)
TypeError: unhashable type: 'list'

```

```python
>>> from typing import NamedTuple
>>> class Stock(NamedTuple):
...     symbol: str
...     current: float
...     high: float
...     low: float
...     @property
...     def middle(self) -> float:
...         return (self.high + self.low)/2
>>> s = Stock("AAPL", 123.52, 137.98, 53.15)
>>> s.middle
95.565

```

## Dataclasses

```python
>>> from dataclasses import dataclass
>>> @dataclass
... class Stock:
...     symbol: str
...     current: float
...     high: float
...     low: float
...
>>> s = Stock("AAPL", 123.52, 137.98, 53.15)
>>> s
Stock(symbol='AAPL', current=123.52, high=137.98, low=53.15)

>>> s.current
123.52
>>> s.current = 122.25
>>> s
Stock(symbol='AAPL', current=122.25, high=137.98, low=53.15)

>>> s.unexpected_attribute = 'allowed'
>>> s.unexpected_attribute
'allowed'

>>> stock2 = Stock(symbol='AAPL', current=122.25, high=137.98, low=53.15)
>>> s == stock2
True


```

```python
>>> class StockOrdinary:
...     def __init__(self, name: str, current: float, high: float, low: float) -> None:
...         self.name = name
...         self.current = current
...         self.high = high
...         self.low = low

>>> s_ord = StockOrdinary("AAPL", 123.52, 137.98, 53.15)
>>> s_ord
<__main__.StockOrdinary object at ...>

>>> s_ord_2 = StockOrdinary("AAPL", 123.52, 137.98, 53.15)
>>> s_ord == s_ord_2
False

```

## Dictionaries

```python
>>> stocks = {
...     "GOOG": (1235.20, 1242.54, 1231.06),
...     "MSFT": (110.41, 110.45, 109.84),
... }

>>> stocks["GOOG"]
(1235.2, 1242.54, 1231.06)
>>> stocks["RIMM"]
Traceback (most recent call last):
  ...
  File "<doctest examples.md[56]>", line 1, in <module>
    stocks.get("RIMM", "NOT FOUND")
KeyError: 'RIMM'

>>> print(stocks.get("RIMM"))
None
>>> stocks.get("RIMM", "NOT FOUND")
'NOT FOUND'


>>> stocks.setdefault("GOOG", "INVALID")
(1235.2, 1242.54, 1231.06)
>>> stocks.setdefault("BB", (10.87, 10.76, 10.90))
(10.87, 10.76, 10.9)
>>> stocks["BB"]
(10.87, 10.76, 10.9)


>>> for stock, values in stocks.items():
...     print(f"{stock} last value is {values[0]}")
...
GOOG last value is 1235.2
MSFT last value is 110.41
BB last value is 10.87


>>> stocks["GOOG"] = (1245.21, 1252.64, 1245.18)
>>> stocks['GOOG']
(1245.21, 1252.64, 1245.18)

```

```python

>>> random_keys = {} 
>>> random_keys["astring"] = "somestring" 
>>> random_keys[5] = "aninteger" 
>>> random_keys[25.2] = "floats work too" 
>>> random_keys[("abc", 123)] = "so do tuples" 
 
>>> class AnObject: 
...     def __init__(self, avalue): 
...         self.avalue = avalue 

>>> my_object = AnObject(14) 
>>> random_keys[my_object] = "We can even store objects" 
>>> my_object.avalue = 12

>>> random_keys[[1,2,3]] = "we can't use lists as keys" 
Traceback (most recent call last):
  ...
  File "<doctest examples.md[72]>", line 1, in <module>
    random_keys[[1,2,3]] = "we can't use lists as keys"
TypeError: unhashable type: 'list'

 
>>> for key in random_keys: 
...     print(f"{key!r} has value {random_keys[key]!r}") 
'astring' has value 'somestring'
5 has value 'aninteger'
25.2 has value 'floats work too'
('abc', 123) has value 'so do tuples'
<__main__.AnObject object at ...> has value 'We can even store objects'


```

```python

>>> x = 2020
>>> y = 2305843009213695971
>>> hash(x) == hash(y)
True
>>> x == y
False
>>> {x: "x", y: "y"}
{2020: 'x', 2305843009213695971: 'y'}

```

### Dictionary use cases

```python
>>> data = {
...     "name": "GOOG",
...     "current": 1245.21, 
...     "range": (1252.64, 1245.18)
... }
>>> data
{'name': 'GOOG', 'current': 1245.21, 'range': (1252.64, 1245.18)}

>>> from typing import TypedDict, Tuple
>>> class StockTD(TypedDict):
...     name: str
...     current: float
...     range: Tuple[float, float]
>>> data_td = StockTD(
...     {'name': 'GOOG', 'current': 1245.21, 'range': (1252.64, 1245.18)}
... )
>>> data_td
{'name': 'GOOG', 'current': 1245.21, 'range': (1252.64, 1245.18)}

```

### Using defaultdict

```python
>>> import collections
>>> names = {"GOOG": "Alphabet Inc.", "AAPL": "Apple Inc."}
>>> lookup = collections.defaultdict(lambda: "N/A", names)
>>> lookup["GOOG"]
'Alphabet Inc.'
>>> lookup["COF"]
'N/A'

```


### Counter

```python
>>> import collections
>>> responses = [
...     "vanilla", 
...     "chocolate", 
...     "vanilla", 
...     "vanilla", 
...     "caramel", 
...     "strawberry", 
...     "vanilla" 
... ]

>>> favorites = collections.Counter(responses).most_common(1)
>>> name, frequency = favorites[0]
>>> name
'vanilla'

```

## Lists


## Sets

```python
>>> song_library = [
...     ("Phantom Of The Opera", "Sarah Brightman"),
...     ("Knocking On Heaven's Door", "Guns N' Roses"),
...     ("Captain Nemo", "Sarah Brightman"),
...     ("Patterns In The Ivy", "Opeth"),
...     ("November Rain", "Guns N' Roses"),
...     ("Beautiful", "Sarah Brightman"),
...     ("Mal's Song", "Vixy and Tony"),
... ]

>>> artists = set()
>>> for song, artist in song_library:
...     artists.add(artist)

>>> artists == {"Guns N' Roses", 'Vixy and Tony', 'Sarah Brightman', 'Opeth'}
True

>>> artists = set(artist for song, artist in song_library)
>>> artists == {"Guns N' Roses", 'Vixy and Tony', 'Sarah Brightman', 'Opeth'}
True

>>> "Opeth" in artists
True
>>> alphabetical = list(artists)
>>> alphabetical.sort()
>>> alphabetical
["Guns N' Roses", 'Opeth', 'Sarah Brightman', 'Vixy and Tony']


```

```python
>>> dusty_artists = {
...     "Sarah Brightman",
...     "Guns N' Roses",
...     "Opeth",
...     "Vixy and Tony",
... }

>>> steve_artists = {"Yes", "Guns N' Roses", "Genesis"}

>>> print(f"All: {dusty_artists | steve_artists}")
All: {'Genesis', "Guns N' Roses", 'Yes', 'Sarah Brightman', 'Opeth', 'Vixy and Tony'}
>>> print(f"Both: {dusty_artists.intersection(steve_artists)}")
Both: {"Guns N' Roses"}
>>> print(
...    f"Either but not both: {dusty_artists ^ steve_artists}"
... )
Either but not both: {'Genesis', 'Sarah Brightman', 'Opeth', 'Yes', 'Vixy and Tony'}

>>> dusty_artists.union(steve_artists) == steve_artists.union(dusty_artists)
True

```

```python
>>> artists = {"Guns N' Roses", 'Vixy and Tony', 'Sarah Brightman', 'Opeth'}
>>> bands = {"Opeth", "Guns N' Roses"}

>>> artists.issuperset(bands)
True
>>> artists.issubset(bands)
False
>>> artists - bands
{'Sarah Brightman', 'Vixy and Tony'}

>>> bands.issuperset(artists)
False
>>> bands.issubset(artists)
True
>>> bands.difference(artists)
set()
>>> bands - artists
set()

```
