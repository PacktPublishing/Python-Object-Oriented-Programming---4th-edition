"""
Python 3 Object-Oriented Programming

Chapter 9. Strings and Serialization
"""
from __future__ import annotations
from threading import Timer
import datetime
from urllib.request import urlopen


class URLPolling:
    def __init__(self, url: str) -> None:
        self.url = url
        self.contents = ""
        self.last_updated: datetime.datetime
        self.timer: Timer
        self.update()

    def update(self) -> None:
        self.contents = urlopen(self.url).read()
        self.last_updated = datetime.datetime.now()
        self.schedule()

    def schedule(self) -> None:
        self.timer = Timer(3600, self.update)
        self.timer.setDaemon(True)
        self.timer.start()


test_broken = """
>>> import pickle
>>> poll = URLPolling("http://dusty.phillips.codes")
>>> pickle.dumps(poll)
Traceback (most recent call last):
  ...
  File "<doctest url_poll.__test__.test_broken[2]>", line 1, in <module>
    pickle.dumps(poll)
TypeError: cannot pickle '_thread.lock' object


"""


from typing import Any


class URLPolling_2:
    def __init__(self, url: str) -> None:
        self.url = url
        self.contents = ""
        self.last_updated: datetime.datetime
        self.timer: Timer
        self.update()

    def update(self) -> None:
        self.contents = urlopen(self.url).read()
        self.last_updated = datetime.datetime.now()
        self.schedule()

    def schedule(self) -> None:
        self.timer = Timer(3600, self.update)
        self.timer.setDaemon(True)
        self.timer.start()

    def __getstate__(self) -> dict[str, Any]:
        pickleable_state = self.__dict__.copy()
        if "timer" in pickleable_state:
            del pickleable_state["timer"]
        return pickleable_state

    def __setstate__(self, pickleable_state: dict[str, Any]) -> None:
        self.__dict__ = pickleable_state
        self.schedule()


test_better = """
>>> import pickle
>>> poll = URLPolling_2("http://dusty.phillips.codes")
>>> pickle_bytes = pickle.dumps(poll)

>>> del poll

>>> recovered_poller = pickle.loads(pickle_bytes)
>>> recovered_poller.contents
b'...'

"""

__test__ = {name: case for name, case in globals().items() if name.startswith("test_")}
