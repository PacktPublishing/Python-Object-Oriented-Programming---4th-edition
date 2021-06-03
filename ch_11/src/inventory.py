"""
Python 3 Object-Oriented Programming

Chapter 11. Common Design Patterns
"""
from __future__ import annotations
import random
import json
import time
from dice import Dice
from typing import List, Protocol


class Observer(Protocol):
    def __call__(self) -> None:
        ...


class Observable:
    def __init__(self) -> None:
        self._observers: list[Observer] = []

    def attach(self, observer: Observer) -> None:
        self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        self._observers.remove(observer)

    def _notify_observers(self) -> None:
        for observer in self._observers:
            observer()


Hand = List[int]


class ZonkHandHistory(Observable):
    def __init__(self, player: str, dice_set: Dice) -> None:
        super().__init__()
        self.player = player
        self.dice_set = dice_set
        self.rolls: list[Hand]

    def start(self) -> Hand:
        self.dice_set.roll()
        self.rolls = [self.dice_set.dice]
        self._notify_observers()  # State change
        return self.dice_set.dice

    def roll(self) -> Hand:
        self.dice_set.roll()
        self.rolls.append(self.dice_set.dice)
        self._notify_observers()  # State change
        return self.dice_set.dice


class SaveZonkHand(Observer):
    def __init__(self, hand: ZonkHandHistory) -> None:
        self.hand = hand
        self.count = 0

    def __call__(self) -> None:
        self.count += 1
        message = {
            "player": self.hand.player,
            "sequence": self.count,
            "hands": json.dumps(self.hand.rolls),
            "time": time.time(),
        }
        print(f"SaveZonkHand {message}")


class ThreePairZonkHand:
    """Observer of ZonkHandHistory"""

    def __init__(self, hand: ZonkHandHistory) -> None:
        self.hand = hand
        self.zonked = False

    def __call__(self) -> None:
        last_roll = self.hand.rolls[-1]
        distinct_values = set(last_roll)
        self.zonked = len(distinct_values) == 3 and all(
            last_roll.count(v) == 2 for v in distinct_values
        )
        if self.zonked:
            print("3 Pair Zonk!")


test_hand_history = """
>>> from unittest.mock import Mock, call
>>> mock_observer = Mock()
>>> import random
>>> random.seed(42)

>>> d = Dice.from_text("6d6")
>>> player = ZonkHandHistory("Bo", d)
>>> player.attach(mock_observer)
>>> player.start()
[1, 1, 2, 3, 6, 6]

>>> player.roll()
[1, 2, 2, 6, 6, 6]

>>> player.rolls
[[1, 1, 2, 3, 6, 6], [1, 2, 2, 6, 6, 6]]

>>> mock_observer.mock_calls
[call(), call()]
"""

test_zonk_observer = """
>>> import random
>>> random.seed(42)

>>> d = Dice.from_text("6d6")
>>> player = ZonkHandHistory("Bo", d)

>>> save_history = SaveZonkHand(player)
>>> player.attach(save_history)
>>> r1 = player.start()
SaveZonkHand {'player': 'Bo', 'sequence': 1, 'hands': '[[1, 1, 2, 3, 6, 6]]', 'time': ...}
>>> r1
[1, 1, 2, 3, 6, 6]

>>> r2 = player.roll()
SaveZonkHand {'player': 'Bo', 'sequence': 2, 'hands': '[[1, 1, 2, 3, 6, 6], [1, 2, 2, 6, 6, 6]]', 'time': ...}
>>> r2
[1, 2, 2, 6, 6, 6]

>>> player.rolls
[[1, 1, 2, 3, 6, 6], [1, 2, 2, 6, 6, 6]]

"""

test_zonk_observer_2 = """
>>> import random
>>> random.seed(21)

>>> d = Dice.from_text("6d6")
>>> player = ZonkHandHistory("David", d)

>>> save_history = SaveZonkHand(player)
>>> player.attach(save_history)
>>> find_3_pair = ThreePairZonkHand(player)
>>> player.attach(find_3_pair)

>>> r1 = player.start()
SaveZonkHand {'player': 'David', 'sequence': 1, 'hands': '[[2, 3, 4, 4, 6, 6]]', 'time': ...}
>>> r1
[2, 3, 4, 4, 6, 6]

>>> r2 = player.roll()
SaveZonkHand {'player': 'David', 'sequence': 2, 'hands': '[[2, 3, 4, 4, 6, 6], [2, 2, 4, 4, 5, 5]]', 'time': ...}
3 Pair Zonk!
>>> r2
[2, 2, 4, 4, 5, 5]

>>> player.rolls
[[2, 3, 4, 4, 6, 6], [2, 2, 4, 4, 5, 5]]

"""


def find_seed() -> None:
    d = Dice.from_text("6d6")
    player = ZonkHandHistory("David", d)

    find_3_pair = ThreePairZonkHand(player)
    player.attach(find_3_pair)

    for s in range(10_000):
        random.seed(s)
        player.start()
        if find_3_pair.zonked:
            print(f"with {s}, roll {player.rolls} ")
        player.roll()
        if find_3_pair.zonked:
            print(f"with {s}, roll {player.rolls} ")


__test__ = {name: case for name, case in globals().items() if name.startswith("test_")}

if __name__ == "__main__":
    find_seed()
