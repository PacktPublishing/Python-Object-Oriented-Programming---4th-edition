"""
Python 3 Object-Oriented Programming

Chapter 14.  Concurrency
"""
import asyncio
from pytest import *
from unittest.mock import AsyncMock, Mock, call, sentinel
import philosophers

@fixture
def mock_random(monkeypatch):
    random = Mock(
        random=Mock(side_effect=[0.2, 0.3])
    )
    monkeypatch.setattr(philosophers, 'random', random)
    return random

@fixture
def mock_sleep(monkeypatch):
    sleep = AsyncMock()
    monkeypatch.setattr(asyncio, 'sleep', sleep)
    return sleep

def test_philosopher(mock_sleep, mock_random, capsys):
    async def when():
        philosophers.FORKS = [asyncio.Lock() for i in range(2)]
        footman = asyncio.BoundedSemaphore(1)
        return await philosophers.philosopher(0, footman)

    result_0 = asyncio.run(when())
    assert result_0 == (0, 1.2, 1.3)
    mock_sleep.assert_has_awaits(
        [
            call(1.2),
            call(1.3)
        ]
    )
    out, err = capsys.readouterr()
    assert out.splitlines() == [
        "0 eating",
        "0 philosophizing"
    ]

@fixture
def mock_philosopher(monkeypatch):
    philosopher = AsyncMock()
    monkeypatch.setattr(philosophers, 'philosopher', philosopher)
    return philosopher

@fixture
def mock_bounded_semaphore(monkeypatch):
    mock_class = Mock(
        return_value=sentinel.mock_bounded_semaphore
    )
    monkeypatch.setattr(asyncio, 'BoundedSemaphore', mock_class)
    return mock_class

def test_main(mock_philosopher, mock_bounded_semaphore):
    asyncio.run(philosophers.main(5, 1))
    mock_philosopher.assert_has_awaits(
        [
            call(0, sentinel.mock_bounded_semaphore),
            call(1, sentinel.mock_bounded_semaphore),
            call(2, sentinel.mock_bounded_semaphore),
            call(3, sentinel.mock_bounded_semaphore),
            call(4, sentinel.mock_bounded_semaphore),
        ]
    )
    mock_bounded_semaphore.assert_called_once_with(4)
