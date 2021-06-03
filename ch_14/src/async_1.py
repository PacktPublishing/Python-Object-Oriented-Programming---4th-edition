"""
Python 3 Object-Oriented Programming

Chapter 14.  Concurrency
"""
import asyncio
import random


async def random_sleep(counter: float) -> None:
    delay = random.random() * 5
    print(f"{counter} sleeps for {delay:.2f} seconds")
    await asyncio.sleep(delay)
    print(f"{counter} awakens, refreshed")


async def sleepers(how_many: int = 5) -> None:
    print(f"Creating {how_many} tasks")
    tasks = [asyncio.create_task(random_sleep(i)) for i in range(how_many)]
    print(f"Waiting for {how_many} tasks")
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(sleepers(5))
    print("Done with the sleepers")
