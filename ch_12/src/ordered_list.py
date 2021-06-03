"""
Python 3 Object-Oriented Programming

Chapter 12. Advanced Python Design Patterns
"""
from __future__ import annotations
import string
import textwrap
from typing import Union, List, Optional


class ListStyleType:
    @staticmethod
    def format(value: int) -> str:
        return f"{value:d}. "


class Decimal(ListStyleType):
    pass


class DecimalLeadingZero(ListStyleType):
    @staticmethod
    def format(value: int) -> str:
        return f"{value:02d}. "


class LowerAlpha(ListStyleType):
    @staticmethod
    def format(value: int) -> str:
        return f"{string.ascii_lowercase[value-1]}. "


class UpperAlpha(ListStyleType):
    @staticmethod
    def format(value: int) -> str:
        return f"{string.ascii_uppercase[value-1]}. "


test_styles = """
>>> l = ListStyleType()
>>> l.format(1)
'1. '
>>> l = Decimal()
>>> l.format(1)
'1. '
>>> l = DecimalLeadingZero()
>>> l.format(1)
'01. '
>>> l = LowerAlpha()
>>> l.format(1)
'a. '
>>> l = UpperAlpha()
>>> l.format(1)
'A. '


"""


class OrderedList:
    def __init__(
        self,
        *children: "Node",
        formatter: type[ListStyleType] = ListStyleType,
    ) -> None:
        self.formatter = formatter
        self.children = list(children)

    def render(self, prefix: str = "") -> str:
        text = []
        for n, c in enumerate(self.children, start=1):
            text.append(c.render(" " * len(prefix) + self.formatter.format(n)))
        return "\n" + ("\n".join(text))


class ListItem:
    def __init__(self, *children: "Node") -> None:
        self.children = list(children)

    def render(self, prefix: str = "") -> str:
        children_iter = iter(self.children)
        first = next(children_iter)
        first_body = [first.render(prefix)]
        item_body = first_body + [c.render(" " * len(prefix)) for c in children_iter]
        return "".join(item_body)


class Text:
    def __init__(self, content: str = "") -> None:
        self.content = content

    def render(self, prefix: str = "") -> str:
        line_iter = iter(self.content.splitlines())
        first = next(line_iter)
        first_body = [f"{prefix}{first}"]
        item_body = first_body + [f"{' '*len(prefix)}{l}" for l in line_iter]
        return "\n".join(item_body) + "\n"


Node = Union[OrderedList, ListItem, Text]

test_text = """
>>> t = Text("nothing special")
>>> t.render(" +-- ")
' +-- nothing special\\n'

>>> t2 = Text("Line 1\\nLine 2")
>>> t2.render(" +-- ")
' +-- Line 1\\n     Line 2\\n'

"""


test_list_item = """
>>> li = ListItem(Text("Nothing Special"))
>>> li.render("1. ")
'1. Nothing Special\\n'

"""

test_ordered_list = """
>>> ol = OrderedList(ListItem(Text("Item 1")), ListItem(Text("Item 2")))
>>> ol.render()
'\\n1. Item 1\\n\\n2. Item 2\\n'

"""

__test__ = {name: case for name, case in globals().items() if name.startswith("test_")}

if __name__ == "__main__":
    doc = OrderedList(
        ListItem(Text("Leaf 1")),
        ListItem(
            Text("Composite 1a\n"),
            OrderedList(
                ListItem(Text("Leaf 2a")),
                ListItem(
                    Text("Composite 2b\n"),
                    OrderedList(
                        ListItem(Text("Leaf 3a")),
                        ListItem(Text("Leaf 3b")),
                        ListItem(Text("Leaf 3c")),
                        ListItem(Text("Leaf 3d")),
                    ),
                ),
                ListItem(Text("Leaf 2c")),
                formatter=LowerAlpha,
            ),
        ),
        ListItem(
            Text("Composite 1b\n"),
            OrderedList(
                ListItem(Text("Leaf 2d")),
                ListItem(
                    Text("Composite 2e\n"),
                    OrderedList(
                        ListItem(Text("Leaf 3e")),
                        ListItem(Text("Leaf 3f")),
                    ),
                ),
                formatter=UpperAlpha,
            ),
        ),
    )
    print(doc.render())
