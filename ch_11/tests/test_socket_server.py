"""
Python 3 Object-Oriented Programming

Chapter 11. Common Design Patterns
"""
import random
import socket_server
from unittest.mock import Mock, call, sentinel
from pytest import *

@fixture
def fixed_seed():
    random.seed(42)

def test_dice_roller_ex(fixed_seed):
    response_1 = socket_server.dice_roller_ex(b"Dice 6 1d6")
    assert response_1 == "Dice 6 1d6 = [6, 1, 1, 6, 3, 2]".encode("utf-8")


@fixture
def mock_socket(monkeypatch):
    accept_instance = Mock(
        send=Mock(),
        recv=Mock(side_effect=(b'Dice2 2 4d6d1', KeyboardInterrupt)),
        close=Mock()
    )
    listen_instance = Mock(
        bind=Mock(),
        listen=Mock(),
        accept=Mock(return_value=(accept_instance, "address")),
        close=Mock()
    )
    socket_module = Mock(
        socket=Mock(return_value=listen_instance),
        AF_INET=sentinel.AF_INET,
        SOCK_STREAM=sentinel.SOCK_STREAM
    )
    monkeypatch.setattr(socket_server, 'socket', socket_module)
    return socket_module

@fixture
def mock_dice(monkeypatch):
    dice_module = Mock(
        dice_roller=Mock(return_value=b'response')
    )
    monkeypatch.setattr(socket_server, 'dice', dice_module)
    return dice_module

def test_dice_response(mock_socket, mock_dice):
    listen_instance = mock_socket.socket.return_value
    accept_instance, addr = listen_instance.accept.return_value

    socket_server.dice_response(accept_instance)
    assert accept_instance.recv.mock_calls == [
        call(1024),
    ]
    assert accept_instance.send.mock_calls == [
        call(b'response')
    ]


@fixture
def mock_response():
    return Mock(return_value="some response")

def test_main_1(mock_socket, mock_response, fixed_seed):
    with raises(KeyboardInterrupt):
        socket_server.main_1()
    assert mock_socket.socket.mock_calls == [
        call(sentinel.AF_INET, sentinel.SOCK_STREAM)
    ]
    listen_instance = mock_socket.socket.return_value
    assert listen_instance.bind.mock_calls == [
        call(('localhost', 2401))
    ]
    assert listen_instance.close.mock_calls == [
        call()
    ]
    accept_instance, address = listen_instance.accept.return_value
    assert address == "address"
    assert accept_instance.recv.mock_calls == [
        call(1024), call(1024),
    ]
    assert accept_instance.send.mock_calls == [
        call(b'Dice2 2 4d6d1 = [7, 7]')
    ]

def test_main_2(mock_socket, mock_response, fixed_seed, capsys):
    with raises(KeyboardInterrupt):
        socket_server.main_1()
    out, err = capsys.readouterr()
    assert out == ""
    assert mock_socket.socket.mock_calls == [
        call(sentinel.AF_INET, sentinel.SOCK_STREAM)
    ]
    listen_instance = mock_socket.socket.return_value
    assert listen_instance.bind.mock_calls == [
        call(('localhost', 2401))
    ]
    assert listen_instance.close.mock_calls == [
        call()
    ]
    accept_instance, address = listen_instance.accept.return_value
    assert address == "address"
    assert accept_instance.recv.mock_calls == [
        call(1024), call(1024),
    ]
    assert accept_instance.send.mock_calls == [
        call(b'Dice2 2 4d6d1 = [7, 7]')
    ]

