"""
Python 3 Object-Oriented Programming Case Study

Chapter 5, When to Use Object-Oriented Programming
"""
from __future__ import annotations


class Color:
    def __init__(self, rgb_value: int, name: str) -> None:
        self._rgb_value = rgb_value
        self._name = name

    def set_name(self, name: str) -> None:
        self._name = name

    def get_name(self) -> str:
        return self._name

    def set_rgb_value(self, rgb_value: int) -> None:
        self._rgb_value = rgb_value

    def get_rgb_value(self) -> int:
        return self._rgb_value


test_color = """
>>> c = Color(0xff0000, "bright red")
>>> c.get_name()
'bright red'
>>> c.set_name("red")
>>> c.get_name()
'red'

"""


class Color_Py:
    def __init__(self, rgb_value: int, name: str) -> None:
        self.rgb_value = rgb_value
        self.name = name


test_color_py = """
>>> c = Color_Py(0xff0000, "bright red")
>>> c.name
'bright red'
>>> c.name = "red"
>>> c.name
'red'

"""


class Color_V:
    def __init__(self, rgb_value: int, name: str) -> None:
        self._rgb_value = rgb_value
        if not name:
            raise ValueError(f"Invalid name {name!r}")
        self._name = name

    def set_name(self, name: str) -> None:
        if not name:
            raise ValueError(f"Invalid name {name!r}")
        self._name = name

    def get_name(self) -> str:
        return self._name

    def set_rgb_value(self, rgb_value: int) -> None:
        self._rgb_value = rgb_value

    def get_rgb_value(self) -> int:
        return self._rgb_value


class Color_VP:
    def __init__(self, rgb_value: int, name: str) -> None:
        self._rgb_value = rgb_value
        if not name:
            raise ValueError(f"Invalid name {name!r}")
        self._name = name

    def _set_name(self, name: str) -> None:
        if not name:
            raise ValueError(f"Invalid name {name!r}")
        self._name = name

    def _get_name(self) -> str:
        return self._name

    def _set_rgb_value(self, rgb_value: int) -> None:
        self._rgb_value = rgb_value

    def _get_rgb_value(self) -> int:
        return self._rgb_value

    name = property(_get_name, _set_name)
    rgb_value = property(_get_rgb_value, _set_rgb_value)


test_color_vp = """
>>> c = Color_VP(0x0000ff, "bright red")
>>> c.name
'bright red'
>>> c.name = "red"
>>> c.name
'red'
>>> c.name = ""
Traceback (most recent call last):
...
  File "src/colors.py", line 85, in _set_name
    raise ValueError(f"Invalid name {name!r}")
ValueError: Invalid name ''


"""


class NorwegianBlue:
    def __init__(self, name: str) -> None:
        self._name = name
        self._state: str

    def _get_state(self) -> str:
        print(f"Getting {self._name}'s State")
        return self._state

    def _set_state(self, state: str) -> None:
        print(f"Setting {self._name}'s State to {state!r}")
        self._state = state

    def _del_state(self) -> None:
        print(f"{self._name} is pushing up daisies!")
        del self._state

    silly = property(_get_state, _set_state, _del_state, "This is a silly property")


test_norwegian_blue = """
>>> p = NorwegianBlue("Polly")
>>> p.silly = "Pining for the fjords"
Setting Polly's State to 'Pining for the fjords'
>>> p.silly
Getting Polly's State
'Pining for the fjords'
>>> del p.silly
Polly is pushing up daisies!
 
>>> help(NorwegianBlue)
Help on class NorwegianBlue in module colors:
<BLANKLINE>
class NorwegianBlue(builtins.object)
 |  NorwegianBlue(name: 'str') -> 'None'
 |  
 |  Methods defined here:
 |  
 |  __init__(self, name: 'str') -> 'None'
 |      Initialize self.  See help(type(self)) for accurate signature.
 |  
 |  ----------------------------------------------------------------------
 |  Data descriptors defined here:
 |  
 |  __dict__
 |      dictionary for instance variables (if defined)
 |  
 |  __weakref__
 |      list of weak references to the object (if defined)
 |  
 |  silly
 |      This is a silly property
<BLANKLINE>

>>> help(NorwegianBlue.silly)
Help on property:
<BLANKLINE>
    This is a silly property
<BLANKLINE>

"""


class NorwegianBlue_P:
    def __init__(self, name: str) -> None:
        self._name = name
        self._state: str

    @property
    def silly(self) -> str:
        """This is a silly property"""
        print(f"Getting {self._name}'s State")
        return self._state

    @silly.setter
    def silly(self, state: str) -> None:
        print(f"Setting {self._name}'s State to {state!r}")
        self._state = state

    @silly.deleter
    def silly(self) -> None:
        print(f"{self._name} is pushing up daisies!")
        del self._state


test_norwegian_blue_p = """
>>> p = NorwegianBlue_P("Polly")
>>> p.silly = "Pining for the fjords"
Setting Polly's State to 'Pining for the fjords'
>>> p.silly
Getting Polly's State
'Pining for the fjords'
>>> del p.silly
Polly is pushing up daisies!

>>> help(NorwegianBlue_P.silly)
Help on property:
<BLANKLINE>
    This is a silly property
<BLANKLINE>

"""

from urllib.request import urlopen
from typing import Optional, cast, List
from bs4 import BeautifulSoup, Tag  # type: ignore [import]


class WebPage:
    def __init__(self, url: str) -> None:
        self.url = url
        self._content: Optional[bytes] = None

    @property
    def content(self) -> bytes:
        if self._content is None:
            print("Retrieving New Page...")
            with urlopen(self.url) as response:
                self._content = response.read()
        return self._content


class GetColors(WebPage):
    @property
    def colors(self) -> list[tuple[str, str, str]]:
        colors = []
        soup = BeautifulSoup(self.content, "html.parser")
        for table in soup.find_all("table", class_="color-chart-x11-table"):
            for row in table.find_all("tr"):
                fields = [col.string for col in row.find_all("td")]
                if len(fields) == 3:
                    color = cast(
                        tuple[str, str, str],
                        tuple(v.strip().replace("\xa0", "") for v in fields),
                    )
                    colors.append(color)
        return colors


def color_demo() -> None:
    gc = GetColors("https://en.wikipedia.org/wiki/Web_colors")
    print(gc.colors)


class AverageList(List[int]):
    @property
    def average(self) -> float:
        return sum(self) / len(self)


test_average_list = """
>>> a = AverageList([10, 8, 13, 9, 11, 14, 6, 4, 12, 7, 5])
>>> a.average
9.0
"""


__test__ = {name: case for name, case in globals().items() if name.startswith("test_")}

if __name__ == "__main__":
    import time

    webpage = WebPage("http://ccphillips.net/")

    now = time.perf_counter()
    content1 = webpage.content
    first_fetch = time.perf_counter() - now

    now = time.perf_counter()
    content2 = webpage.content
    second_fetch = time.perf_counter() - now

    assert content2 == content1, "Problem: Pages were different"
    print(f"Initial Request     {first_fetch:.6f}")
    print(f"Subsequent Requests {second_fetch:.6f}")
