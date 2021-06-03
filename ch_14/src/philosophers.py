"""
Python 3 Object-Oriented Programming

Chapter 14.  Concurrency
"""
from __future__ import annotations
import asyncio
import collections
import random
from typing import List, DefaultDict, Iterator

FORKS: List[asyncio.Lock]


async def philosopher(id: int, footman: asyncio.Semaphore) -> tuple[int, float, float]:
    async with footman:
        async with FORKS[id], FORKS[(id + 1) % len(FORKS)]:
            eat_time = 1 + random.random()
            print(f"{id} eating")
            await asyncio.sleep(eat_time)
        think_time = 1 + random.random()
        print(f"{id} philosophizing")
        await asyncio.sleep(think_time)
    return id, eat_time, think_time


async def main(faculty: int = 5, servings: int = 5) -> None:
    global FORKS
    FORKS = [asyncio.Lock() for i in range(faculty)]
    footman = asyncio.BoundedSemaphore(faculty - 1)
    for serving in range(servings):
        department = (philosopher(p, footman) for p in range(faculty))
        results = await asyncio.gather(*department)
        print(results)


if __name__ == "__main__":
    asyncio.run(main())
