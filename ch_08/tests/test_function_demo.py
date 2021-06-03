"""
Python 3 Object-Oriented Programming

Chapter 8. The Intersection of Object-Oriented and Functional Programming
"""

from pytest import *
import function_demo
from unittest.mock import Mock, call


def test_task_single(capsys):
    t_1 = function_demo.Task(scheduled=42, callback=lambda x: print(f"{x=}"))
    t_2 = t_1.repeat(42)
    assert t_2 is None
    t_1.callback(42)
    out, err = capsys.readouterr()
    assert out == "x=42\n"


def test_task_repeat(capsys):
    t_1 = function_demo.Task(scheduled=42, callback=lambda x: print(f"{x=}"), delay=13, limit=3)
    t_2 = t_1.repeat(42)
    assert t_2 == function_demo.Task(scheduled=55, callback=lambda x: print(f"{x=}"), delay=13, limit=2)
    t_1.callback(42)

    t_3 = t_2.repeat(55)
    assert t_3 == function_demo.Task(scheduled=68, callback=lambda x: print(f"{x=}"))
    t_2.callback(55)

    t_4 = t_3.repeat(68)
    assert t_4 is None
    t_3.callback(68)

    out, err = capsys.readouterr()
    assert out == "x=42\nx=55\nx=68\n"


@fixture
def mock_time(monkeypatch):
    time_module = Mock(sleep=Mock())
    monkeypatch.setattr(function_demo, "time", time_module)
    return time_module


@fixture
def mock_task():
    return Mock()


def test_scheduler_single(mock_time, mock_task):
    s = function_demo.Scheduler()
    s.enter(42, mock_task)
    s.run()
    assert mock_time.sleep.mock_calls == [call(42)]
    assert mock_task.mock_calls == [call(42)]


@fixture
def mock_task13():
    return Mock()


@fixture
def mock_task42():
    return Mock()


def test_scheduler_many(mock_time, mock_task13, mock_task42):
    s = function_demo.Scheduler()
    s.enter(13, mock_task13)
    s.enter(42, mock_task42)
    s.run()
    assert mock_time.sleep.mock_calls == [call(13), call(29)]
    assert mock_task13.mock_calls == [call(13)]
    assert mock_task42.mock_calls == [call(42)]


def test_scheduler_repeat(mock_time, mock_task):
    s = function_demo.Scheduler()
    s.enter(13, mock_task, 11, limit=3)
    s.run()
    assert mock_time.sleep.mock_calls == [call(13), call(11), call(11)]
    assert mock_task.mock_calls == [call(13), call(24), call(35)]


def test_full_demo(mock_time):
    task_one = Mock()
    task_two = Mock()
    task_three = Mock()
    task_repeater = Mock(four=Mock())
    s = function_demo.Scheduler()
    s.enter(1, task_one)
    s.enter(2, task_one)
    s.enter(2, task_two)
    s.enter(4, task_two)
    s.enter(3, task_three)
    s.enter(6, task_three)
    s.enter(5, task_repeater.four, delay=1, limit=5)
    s.run()
    assert task_one.mock_calls == [call(1), call(2)]
    assert task_two.mock_calls == [call(2), call(4)]
    assert task_three.mock_calls == [call(3), call(6)]
    assert task_repeater.four.mock_calls == [call(5), call(6), call(7), call(8), call(9)]
