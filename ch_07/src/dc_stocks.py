"""
Python 3 Object-Oriented Programming

Chapter 7. Python Data Structures
"""

from dataclasses import dataclass


@dataclass
class Stock:
    symbol: str
    current: float
    high: float
    low: float


test_stock = """
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
"""


@dataclass
class StockDefaults:
    name: str
    current: float = 0.0
    high: float = 0.0
    low: float = 0.0


test_stock_defaults = """
>>> StockDefaults("GOOG")
StockDefaults(name='GOOG', current=0.0, high=0.0, low=0.0)
>>> StockDefaults("GOOG", 1826.77, 1847.20, 1013.54)
StockDefaults(name='GOOG', current=1826.77, high=1847.2, low=1013.54)

"""


@dataclass(order=True)
class StockOrdered:
    name: str
    current: float = 0.0
    high: float = 0.0
    low: float = 0.0


test_stock_ordered = """
>>> stock_ordered1 = StockOrdered("GOOG", 1826.77, 1847.20, 1013.54)
>>> stock_ordered2 = StockOrdered("GOOG")
>>> stock_ordered3 = StockOrdered("GOOG", 1728.28, high=1733.18, low=1666.33)

>>> stock_ordered1 < stock_ordered2
False
>>> stock_ordered1 > stock_ordered2
True
>>> from pprint import pprint
>>> pprint(sorted([stock_ordered1, stock_ordered2, stock_ordered3]))
[StockOrdered(name='GOOG', current=0.0, high=0.0, low=0.0),
 StockOrdered(name='GOOG', current=1728.28, high=1733.18, low=1666.33),
 StockOrdered(name='GOOG', current=1826.77, high=1847.2, low=1013.54)]

"""

test_stock_defaultdict = """
>>> import collections
>>> from dataclasses import dataclass
>>> @dataclass
... class Prices:
...     current: float = 0.0
...     high: float = 0.0
...     low: float = 0.0
...
>>> Prices() 
Prices(current=0.0, high=0.0, low=0.0)

>>> portfolio = collections.defaultdict(Prices)
>>> portfolio["GOOG"]
Prices(current=0.0, high=0.0, low=0.0)
>>> portfolio["AAPL"] = Prices(current=122.25, high=137.98, low=53.15)

>>> from pprint import pprint
>>> pprint(portfolio)
defaultdict(<class 'dc_stocks.Prices'>,
            {'AAPL': Prices(current=122.25, high=137.98, low=53.15),
             'GOOG': Prices(current=0.0, high=0.0, low=0.0)})

>>> by_month = collections.defaultdict(
...     lambda : collections.defaultdict(Prices)
... )
>>> by_month["APPL"]["Jan"] = Prices(current=122.25, high=137.98, low=53.15)
>>> by_month
defaultdict(<function <lambda> at 0x...>, {'APPL': defaultdict(<class 'dc_stocks.Prices'>, {'Jan': Prices(current=122.25, high=137.98, low=53.15)})})

"""


__test__ = {name: case for name, case in globals().items() if name.startswith("test_")}
