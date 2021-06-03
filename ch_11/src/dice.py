"""
Python 3 Object-Oriented Programming

Chapter 11. Common Design Patterns
"""
from __future__ import annotations
import abc
import re
import random
from typing import cast, Optional, Union, Sequence


class Adjustment(abc.ABC):
    def __init__(self, amount: int) -> None:
        self.amount = amount

    @abc.abstractmethod
    def apply(self, dice: "Dice") -> None:
        ...


class Roll(Adjustment):
    def __init__(self, n: int, d: int) -> None:
        self.n = n
        self.d = d

    def apply(self, dice: "Dice") -> None:
        dice.dice = sorted(random.randint(1, self.d) for _ in range(self.n))
        dice.modifier = 0


class Drop(Adjustment):
    def apply(self, dice: "Dice") -> None:
        dice.dice = dice.dice[self.amount :]


class Keep(Adjustment):
    def apply(self, dice: "Dice") -> None:
        dice.dice = dice.dice[: self.amount]


class Plus(Adjustment):
    def apply(self, dice: "Dice") -> None:
        dice.modifier += self.amount


class Minus(Adjustment):
    def apply(self, dice: "Dice") -> None:
        dice.modifier -= self.amount


class Dice:
    def __init__(self, n: int, d: int, *adj: Adjustment) -> None:
        self.adjustments = [cast(Adjustment, Roll(n, d))] + list(adj)
        self.dice: list[int]
        self.modifier: int

    def roll(self) -> int:
        for a in self.adjustments:
            a.apply(self)
        return sum(self.dice) + self.modifier

    @classmethod
    def from_text(cls, dice_text: str) -> "Dice":
        dice_pattern = re.compile(r"(?P<n>\d*)d(?P<d>\d+)(?P<a>[dk+-]\d+)*")
        adjustment_pattern = re.compile(r"([dk+-])(\d+)")
        adj_class: dict[str, type[Adjustment]] = {
            "d": Drop,
            "k": Keep,
            "+": Plus,
            "-": Minus,
        }

        if (dice_match := dice_pattern.match(dice_text)) is None:
            raise ValueError(f"Error in {dice_text!r}")

        n = int(dice_match.group("n")) if dice_match.group("n") else 1
        d = int(dice_match.group("d"))
        adjustment_matches = adjustment_pattern.finditer(dice_match.group("a") or "")
        adjustments = [
            adj_class[a.group(1)](int(a.group(2))) for a in adjustment_matches
        ]
        return cls(n, d, *adjustments)


D4 = 4
D6 = 6
D8 = 8
D12 = 12
D20 = 20


class Dice2:
    """A version of Dice that doesn't parse the definition string.
    It always implements 2d6.
    """

    @staticmethod
    def from_text(dice_text: str) -> "Dice2":
        return Dice2(2, 6)

    def __init__(self, n: int, d: int) -> None:
        self.n = n
        self.d = d
        self.dice: list[int]

    def roll(self) -> int:
        self.dice = [random.randint(1, self.d) for _ in range(self.n)]
        return sum(self.dice)


# Instead of an abstract class, rely on duck typing...
DiceRoller = Union[Dice2, Dice]
implementations: dict[str, type[DiceRoller]] = {"Dice2": Dice2, "Dice": Dice}


def dice_roller(request: bytes) -> bytes:
    request_text = request.decode("utf-8")
    request_pattern = re.compile(r"(\w+) (\d+) (.*)")
    if (request_match := request_pattern.match(request_text)) is None:
        raise ValueError(f"Error in {request!r}")
    model_class = implementations[request_match.group(1)]
    count = int(request_match.group(2))
    dice = model_class.from_text(request_match.group(3))
    numbers = [dice.roll() for _ in range(count)]
    response = f"{request_text} = {numbers}"
    return response.encode("utf-8")


test_dice = """
>>> import random
>>> random.seed(42)
>>> d_1 = Dice.from_text("4d6k3")
>>> d_1.roll()
8

"""

test_dice_roller = """
>>> import random
>>> random.seed(42)
>>> dice_roller(b"Dice 6 4d6d1")
b'Dice 6 4d6d1 = [13, 7, 18, 14, 4, 12]'

"""

__test__ = {name: case for name, case in globals().items() if name.startswith("test_")}
