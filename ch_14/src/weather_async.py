"""
Python 3 Object-Oriented Programming

Chapter 14.  Concurrency
"""
import asyncio
import httpx
import re
import time
from urllib.request import urlopen
from typing import Optional, NamedTuple


class Zone(NamedTuple):
    zone_name: str
    zone_code: str
    same_code: str  # Special Area Messaging Encoder

    @property
    def forecast_url(self) -> str:
        return (
            f"https://tgftp.nws.noaa.gov/data/forecasts"
            f"/marine/coastal/an/{self.zone_code.lower()}.txt"
        )


ZONES = [
    Zone("Chesapeake Bay from Pooles Island to Sandy Point, MD", "ANZ531", "073531"),
    Zone("Chesapeake Bay from Sandy Point to North Beach, MD", "ANZ532", "073532"),
    Zone("Chesapeake Bay from North Beach to Drum Point, MD", "ANZ533", "073533"),
    Zone("Chesapeake Bay from Drum Point to Smith Point, VA", "ANZ534", "073534"),
    Zone("Tidal Potomac from Key Bridge to Indian Head, MD", "ANZ535", "073535"),
    Zone("Tidal Potomac from Indian Head to Cobb Island, MD", "ANZ536", "073536"),
    Zone("Tidal Potomac from Cobb Island, MD to Smith Point, VA", "ANZ537", "073537"),
    Zone("Patapsco River including Baltimore Harbor", "ANZ538", "073538"),
    Zone("Chester River to Queenstown MD", "ANZ539", "073539"),
    Zone("Eastern Bay", "ANZ540", "073540"),
    Zone(
        "Choptank River to Cambridge MD and the Little Choptank River",
        "ANZ541",
        "073541",
    ),
    Zone("Patuxent River to Broome’s Island MD", "ANZ542", "073542"),
    Zone(
        "Tangier Sound and the Inland Waters surrounding Bloodsworth Island",
        "ANZ543",
        "073543",
    ),
]


class MarineWX:
    advisory_pat = re.compile(r"\n\.\.\.(.*?)\.\.\.\n", re.M | re.S)

    def __init__(self, zone: Zone) -> None:
        super().__init__()
        self.zone = zone
        self.doc = ""

    async def run(self) -> None:
        """
        Blocking IO assigned to a task.
        with urlopen(self.zone.forecast_url) as stream:
            self.doc = stream.read().decode("UTF-8")
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(self.zone.forecast_url)
        self.doc = response.text

    @property
    def advisory(self) -> str:
        if match := self.advisory_pat.search(self.doc):
            return match.group(1).replace("\n", " ")
        return ""

    def __repr__(self) -> str:
        return f"{self.zone.zone_name} {self.advisory}"


async def task_main() -> None:
    start = time.perf_counter()
    forecasts = [MarineWX(z) for z in ZONES]

    await asyncio.gather(*(asyncio.create_task(f.run()) for f in forecasts))

    for f in forecasts:
        print(f)

    print(
        f"Got {len(forecasts)} forecasts "
        f"in {time.perf_counter() - start:.3f} seconds"
    )


if __name__ == "__main__":
    asyncio.run(task_main())
