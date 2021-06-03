"""
Python 3 Object-Oriented Programming

Chapter 11. Common Design Patterns
"""
import random
import dice
from unittest.mock import Mock, call, sentinel
from pytest import *

@fixture
def fixed_seed():
    random.seed(42)

def test_dice(fixed_seed):
    d_1 = dice.Dice.from_text("3d6+1")
    assert d_1.adjustments[0].n == 3
    assert d_1.adjustments[0].d == 6
    assert d_1.roll() == 9
    assert d_1.dice == [1, 1, 6]
    d_2 = dice.Dice.from_text("4d6k3")
    assert d_2.adjustments[0].n == 4
    assert d_2.adjustments[0].d == 6
    assert d_2.roll() == 7
    assert d_2.dice == [2, 2, 3]
    d_3 = dice.Dice.from_text("4d6d1")
    assert d_3.adjustments[0].n == 4
    assert d_3.adjustments[0].d == 6
    assert d_3.roll() == 14
    assert d_3.dice == [2, 6, 6]

    d_4 = dice.Dice(4, dice.D6, dice.Keep(3))
    assert d_4.roll() == 11
    assert d_4.dice == [1, 5, 5]


def test_dice_2(fixed_seed):
    d = dice.Dice2.from_text("3d6")
    assert d.n == 2
    assert d.d == 6
    assert d.roll() == 7


def test_dice_roller(fixed_seed):
    response_1 = dice.dice_roller(b"Dice2 2 2d6")
    assert response_1 == b"Dice2 2 2d6 = [7, 7]"
    response_2 = dice.dice_roller(b"Dice 2 4d6d1")
    assert response_2 == b"Dice 2 4d6d1 = [7, 18]"
    with raises(ValueError):
        dice.dice_roller(b"nothing recognizable")
    with raises(KeyError):
        dice.dice_roller(b"bad 2 2d6")
