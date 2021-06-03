"""
Python 3 Object-Oriented Programming

Chapter 14. Concurrency
"""
from threading import Thread, Lock
import time
from typing import Optional


class Food:
    pass


class Sandwich(Food):
    def __init__(self, name: str) -> None:
        self.name = name

    def __repr__(self) -> str:
        return self.name


class Pickle(Food):
    def __repr__(self) -> str:
        return "Crispy Dill Pickle"


class Creation:
    def __init__(self, signature: str, *item: Food) -> None:
        self.chef = signature
        self.items = list(item)

    def __repr__(self) -> str:
        return f"{' & '.join(repr(i) for i in self.items)} from {self.chef}"


class Tray:
    def __init__(self) -> None:
        self.content: Optional[Creation] = None
        self.chef_station: "Chef"

    def ready_for_chef(self, chef: "Chef") -> None:
        self.chef_station = chef

    def prepare(self, creation: Creation) -> None:
        self.content = creation

    def present(self) -> None:
        # Handed off to the diner's table -- not implemented
        self.content = None


THE_TRAY = Tray()

THE_ORDERS = [
    "Reuben",
    "Ham and Cheese",
    "Monte Cristo",
    "Tuna Melt",
    "Cuban",
    "Grilled Cheese",
    "French Dip",
    "BLT",
]


class Owner(Thread):
    def __init__(self, *chefs: "Chef") -> None:
        super().__init__()
        self.flag = Lock()
        self.chefs = chefs
        self.next_chef = 0
        self.move_tray()

    def move_tray(self) -> None:
        THE_TRAY.ready_for_chef(self.chefs[self.next_chef])
        self.next_chef = (self.next_chef + 1) % len(self.chefs)

    def order_up(self) -> None:
        self.flag.acquire()

    def run(self) -> None:
        while any(c.is_alive() for c in self.chefs):
            if self.flag.locked():
                print(THE_TRAY.content)
                THE_TRAY.present()
                self.move_tray()
                self.flag.release()
            # Is it sensible to move the tray here?
            # What state is the chef in?
        print(THE_TRAY.content)


class Chef(Thread):
    def __init__(self, name: str) -> None:
        super().__init__(name=name)

    def get_order(self) -> None:
        self.order = THE_ORDERS.pop(0)

    def prepare(self) -> None:
        time.sleep(1)
        sandwich = Sandwich(self.order)
        pickle = Pickle()
        creation = Creation(self.name, sandwich, pickle)
        while THE_TRAY.chef_station is not self:
            time.sleep(1)
        THE_TRAY.prepare(creation)
        OWNER.order_up()

    def run(self) -> None:
        while True:
            try:
                self.get_order()
                self.prepare()
            except IndexError:
                break  # No more orders


Mo = Chef("Michael")
Constantine = Chef("Constantine")
OWNER = Owner(Mo, Constantine)

if __name__ == "__main__":
    Mo.start()
    Constantine.start()
    OWNER.start()
