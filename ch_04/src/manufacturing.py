"""
Python 3 Object-Oriented Programming Case Study

Chapter 4, Expecting the Unexpected
"""
from __future__ import annotations


def divide_with_exception(dividend: int, divisor: int) -> None:
    try:
        print(f"{dividend / divisor=}")
    except ZeroDivisionError:
        print("You can't divide by zero")


def divide_with_if(dividend: int, divisor: int) -> None:
    if divisor == 0:
        print("You can't divide by zero")
    else:
        print(f"{dividend / divisor=}")


class ItemType:
    def __init__(self, name: str) -> None:
        self.name = name
        self.on_hand = 0


class OutOfStock(Exception):
    pass


class InvalidItemType(Exception):
    pass


class Inventory:
    def __init__(self, stock: list[ItemType]) -> None:
        pass

    def lock(self, item_type: ItemType) -> None:
        """Context Entry.
        Lock the item type so nobody else can manipulate the
        inventory while we're working."""
        pass

    def unlock(self, item_type: ItemType) -> None:
        """Context Exit.
        Unlock the item type."""
        pass

    def purchase(self, item_type: ItemType) -> int:
        """If the item is not locked, raise an
        ValueError because someting went wrong.
        If the item_type does not exist,
          raise InvalidItemType.
        If the item is currently out of stock,
          raise OutOfStock.
        If the item is available,
          subtract one item; return the number of items left.
        """
        # Mocked results.
        if item_type.name == "Widget":
            raise OutOfStock(item_type)
        elif item_type.name == "Gadget":
            return 42
        else:
            raise InvalidItemType(item_type)


test_inventory = """
>>> widget = ItemType("Widget")
>>> gadget = ItemType("Gadget")
>>> inv = Inventory([widget, gadget])

>>> item_to_buy = widget
>>> inv.lock(item_to_buy)
>>> try:
...     num_left = inv.purchase(item_to_buy)
... except InvalidItemType:
...     print(f"Sorry, we don't sell {item_to_buy.name}")
... except OutOfStock:
...     print("Sorry, that item is out of stock.")
... else:
...     print(f"Purchase complete. There are {num_left} {item_to_buy.name}s left")
... finally:
...     inv.unlock(item_to_buy)
...
Sorry, that item is out of stock.

>>> item_to_buy = gadget
>>> inv.lock(item_to_buy)
>>> try:
...     num_left = inv.purchase(item_to_buy)
... except InvalidItemType:
...     print(f"Sorry, we don't sell {item_to_buy.name}")
... except OutOfStock:
...     print("Sorry, that item is out of stock.")
... else:
...     print(f"Purchase complete. There are {num_left} {item_to_buy.name}s left")
... finally:
...     inv.unlock(item_to_buy)
...
Purchase complete. There are 42 Gadgets left

>>> item_to_buy = ItemType("Sprocket")
>>> inv.lock(item_to_buy)
>>> try:
...     num_left = inv.purchase(item_to_buy)
... except InvalidItemType:
...     print(f"Sorry, we don't sell {item_to_buy.name}")
... except OutOfStock:
...     print("Sorry, that item is out of stock.")
... else:
...     print(f"Purchase complete. There are {num_left} {item_to_buy.name}s left")
... finally:
...     inv.unlock(item_to_buy)
...
Sorry, we don't sell Sprocket

"""

__test__ = {name: case for name, case in globals().items() if name.startswith("test_")}


if __name__ == "__main__":
    # A comparison of EAFP and LBYL performance.
    import timeit
    import sys

    eafp_pure_happy = timeit.timeit(
        setup="from manufacturing import divide_with_exception; import io; import sys; sys.stdout=io.StringIO()",
        stmt="divide_with_exception(355, 113)",
    )
    eafp_pure_sad = timeit.timeit(
        setup="from manufacturing import divide_with_exception; import io; import sys; sys.stdout=io.StringIO()",
        stmt="divide_with_exception(355, 0)",
    )
    eafp_90_10 = timeit.timeit(
        setup="from manufacturing import divide_with_exception; import io; import sys; sys.stdout=io.StringIO()",
        stmt="for i in range(10): divide_with_exception(355, i)",
        number=100_000,
    )
    eafp_99_1 = timeit.timeit(
        setup="from manufacturing import divide_with_exception; import io; import sys; sys.stdout=io.StringIO()",
        stmt="for i in range(100): divide_with_exception(355, i)",
        number=10_000,
    )

    lbyl_pure_happy = timeit.timeit(
        setup="from manufacturing import divide_with_if; import io; import sys; sys.stdout=io.StringIO()",
        stmt="divide_with_if(355, 113)",
    )
    lbyl_pure_sad = timeit.timeit(
        setup="from manufacturing import divide_with_if; import io; import sys; sys.stdout=io.StringIO()",
        stmt="divide_with_if(355, 0)",
    )
    lbyl_90_10 = timeit.timeit(
        setup="from manufacturing import divide_with_if; import io; import sys; sys.stdout=io.StringIO()",
        stmt="for i in range(10): divide_with_if(355, i)",
        number=100_000,
    )
    lbyl_99_1 = timeit.timeit(
        setup="from manufacturing import divide_with_if; import io; import sys; sys.stdout=io.StringIO()",
        stmt="for i in range(100): divide_with_if(355, i)",
        number=10_000,
    )

    sys.stdout = sys.__stdout__
    print("EAFP - Easier to Ask Forgiveness than Permission")
    print(f"Pure Happy       {eafp_pure_happy:.3f}")
    print(f"Pure Exceptional {eafp_pure_sad:.3f}")
    print(f" 90% Happy       {eafp_90_10:.3f}")
    print(f"  1% Happy       {eafp_99_1:.3f}")

    print("LBYL - Look Before You Leap")
    print(f"Pure Happy       {lbyl_pure_happy:.3f}")
    print(f"Pure Exceptional {lbyl_pure_sad:.3f}")
    print(f" 90% Happy       {lbyl_90_10:.3f}")
    print(f"  1% Happy       {lbyl_99_1:.3f}")
