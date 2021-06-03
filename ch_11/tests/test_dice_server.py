"""
Python 3 Object-Oriented Programming

Chapter 11. Common Design Patterns
"""
import gzip
import io
import random
import dice_server
from unittest.mock import Mock, call, sentinel
from pytest import *


def test_zip_roller():
    roller = Mock(return_value=b'response bytes')
    zr = dice_server.ZipRoller(roller)
    zipped_response = io.BytesIO(zr(b'request'))
    with gzip.GzipFile(fileobj=zipped_response) as zipfile:
        response = zipfile.read()
    assert response == b'response bytes'
    assert roller.mock_calls == [call(b'request')]


def test_log_roller(capsys):
    roller = Mock(return_value=b'response bytes')
    lr = dice_server.LogRoller(roller, ('remote', 4021))
    response = lr(b'request')
    assert response == b'response bytes'
    assert roller.mock_calls == [call(b'request')]
    out, err = capsys.readouterr()
    assert out == "Receiving b'request' from ('remote', 4021)\nSending b'response bytes' to ('remote', 4021)\n"


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
    monkeypatch.setattr(dice_server, 'socket', socket_module)
    return socket_module

@fixture
def mock_dice(monkeypatch):
    dice_module = Mock(
        dice_roller=Mock(return_value=b'response')
    )
    monkeypatch.setattr(dice_server, 'dice', dice_module)
    return dice_module

@fixture
def mock_ZipRoller(monkeypatch):
    mock_instance = Mock(return_value=b'response')
    mock_class = Mock(return_value=mock_instance)
    monkeypatch.setattr(dice_server, 'ZipRoller', mock_class)
    return mock_class


def test_dice_response(mock_ZipRoller, mock_socket, mock_dice):
    listen_instance = mock_socket.socket.return_value
    accept_instance, addr = listen_instance.accept.return_value
    dice_server.dice_response(accept_instance)

    assert accept_instance.recv.mock_calls == [
        call(1024),
    ]
    assert accept_instance.send.mock_calls == [
        call(b'response')
    ]

