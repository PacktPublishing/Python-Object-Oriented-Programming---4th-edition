"""
Python 3 Object-Oriented Programming

Chapter 14.  Concurrency
"""
from threading import Thread
import time
from urllib.request import urlopen
from xml.etree import ElementTree
from typing import Optional, NamedTuple


class Station(NamedTuple):
    province: str
    code: str
    language: str = "e"  # "f" for French

    @property
    def path(self) -> str:
        return f"/{self.province}/{self.code}_{self.language}.xml"

    @property
    def url(self) -> str:
        return f"https://dd.weather.gc.ca/citypage_weather/xml{self.path}"


CITIES = {
    "Charlottetown": Station("PE", "s0000583"),
    "Edmonton": Station("AB", "s0000045"),
    "Fredericton": Station("NB", "s0000250"),
    "Halifax": Station("NS", "s0000318"),
    "Iqaluit": Station("NU", "s0000394"),
    "Québec City": Station("QC", "s0000620"),
    "Regina": Station("SK", "s0000788"),
    "St. John's": Station("NL", "s0000280"),
    "Toronto": Station("ON", "s0000458"),
    "Victoria": Station("BC", "s0000775"),
    "Whitehorse": Station("YT", "s0000825"),
    "Winnipeg": Station("MB", "s0000193"),
    "Yellowknife": Station("NT", "s0000366"),
}


class TempGetter(Thread):
    def __init__(self, city: str) -> None:
        super().__init__()
        self.city = city
        self.station = CITIES[self.city]
        self.temperature: Optional[str] = None

    def run(self) -> None:
        with urlopen(self.station.url) as stream:
            try:
                # xml = ElementTree.parse(stream)
                doc = stream.read()
                xml = ElementTree.fromstring(doc)
                temperature_tag = xml.find("currentConditions/temperature")
                if temperature_tag is not None:
                    self.temperature = temperature_tag.text
                else:
                    self.temperature = "(missing)"
            except ElementTree.ParseError as ex:
                print(ex)
                print(doc)
                raise


def main() -> None:
    threads = [TempGetter(c) for c in CITIES]
    start = time.time()
    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    for thread in threads:
        print(f"Currently {thread.temperature}°C in {thread.city}")
    print(f"Got {len(threads)} temps in {time.time() - start} seconds")


if __name__ == "__main__":
    main()
