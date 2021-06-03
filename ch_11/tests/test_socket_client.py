"""
Python 3 Object-Oriented Programming

Chapter 11. Common Design Patterns
"""
import socket_client
from unittest.mock import Mock, call, sentinel
from pytest import *

@fixture
def mock_socket(monkeypatch):
    mock_instance = Mock(
        connect=Mock(),
        send=Mock(),
        recv=Mock(return_value=b'server reply'),
        close=Mock()
    )
    socket_module = Mock(
        socket=Mock(return_value=mock_instance),
        AF_INET=sentinel.AF_INET,
        SOCK_STREAM=sentinel.SOCK_STREAM
    )
    monkeypatch.setattr(socket_client, 'socket', socket_module)
    return socket_module

@fixture
def mock_input(monkeypatch):
    input_function = Mock(
        side_effect=["42", "4d6d1"]
    )
    monkeypatch.setitem(
        socket_client.__builtins__, 'input',
        input_function
    )

def test_client(mock_socket, mock_input, capsys):
    socket_client.main()
    out, err = capsys.readouterr()
    assert out == "server reply\n"
    assert mock_socket.socket.mock_calls == [
        call(sentinel.AF_INET, sentinel.SOCK_STREAM)
    ]
    instance = mock_socket.socket.return_value
    assert instance.connect.mock_calls == [
        call(('localhost', 2401))
    ]
    assert instance.send.mock_calls == [
        call(b'Dice 42 4d6d1')
    ]
    assert instance.recv.mock_calls == [
        call(1024)
    ]
    assert instance.close.mock_calls == [
        call()
    ]
