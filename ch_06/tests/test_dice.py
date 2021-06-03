"""
Python 3 Object-Oriented Programming Case Study

Chapter 6, Abstract Base Classes and Operator Overloading
"""
import logging
from pytest import *
import random
from dice import D6L

@fixture
def fixed_random():
    random.seed(42)

def test_dice_logger(caplog, fixed_random):
    caplog.set_level(logging.INFO)
    d6l = D6L()
    assert d6l.face == 6
    assert caplog.messages == [
        'Rolled 6'
    ]
    assert D6L.roll.__doc__ == "Some documentation on D6L"
