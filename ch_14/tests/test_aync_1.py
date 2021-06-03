"""
Python 3 Object-Oriented Programming

Chapter 14.  Concurrency
"""
from pytest import *
from unittest.mock import AsyncMock, Mock, call
import async_1
import asyncio


@fixture
def mock_random(monkeypatch):
    random = Mock(
        random=Mock(return_value=0.5)
    )
    monkeypatch.setattr(async_1, 'random', random)
    return random

@fixture
def mock_sleep(monkeypatch):
    sleep = AsyncMock()
    monkeypatch.setattr(asyncio, 'sleep', sleep)
    return sleep

def test_random_sleep(mock_random, mock_sleep, capsys):
    asyncio.run(async_1.random_sleep(42))
    assert mock_random.random.mock_calls == [call()]
    mock_sleep.assert_awaited()
    mock_sleep.assert_called_once_with(2.5)
    out, err = capsys.readouterr()
    assert out.splitlines() == [
        '42 sleeps for 2.50 seconds',
        '42 awakens, refreshed'
    ]

@fixture
def mock_random_sleep(monkeypatch):
    random_sleep = AsyncMock()
    monkeypatch.setattr(async_1, 'random_sleep', random_sleep)
    return random_sleep

def test_sleepers(mock_random_sleep, capsys):
    asyncio.run(async_1.sleepers(2))
    mock_random_sleep.mock_calls == [
        call(0),
        call(1)
    ]
    out, err = capsys.readouterr()
    assert out.splitlines() == [
        'Creating 2 tasks',
        'Waiting for 2 tasks'
    ]

