"""
Python 3 Object-Oriented Programming

Chapter 14.  Concurrency
"""
import asyncio
import pickle
from pytest import *
import struct
from unittest.mock import AsyncMock, Mock, call
import log_catcher

@fixture
def mock_target(monkeypatch):
    open_file = Mock()
    log_catcher.TARGET = open_file
    return open_file

def test_log_writer(mock_target, capsys):
    payload = pickle.dumps("message")
    asyncio.run(log_catcher.log_writer(payload))
    assert mock_target.write.mock_calls == [
        call('"message"'),
        call('\n')
    ]


@fixture
def mock_log_writer(monkeypatch):
    log_writer = AsyncMock()
    monkeypatch.setattr(log_catcher, 'log_writer', log_writer)
    return log_writer

@fixture
def mock_stream():
    mock_socket = Mock(
        getpeername=Mock(return_value=['127.0.0.1', 12342])
    )
    payload = pickle.dumps("message")
    size = struct.pack(">L", len(payload))
    stream = Mock(
        read=AsyncMock(side_effect=[size, payload, None]),
        get_extra_info=Mock(return_value=mock_socket)
    )
    return payload, stream


def test_log_catcher(mock_log_writer, mock_stream):
    payload, stream = mock_stream
    asyncio.run(log_catcher.log_catcher(stream, stream))
    # Depends on len(payload)
    assert stream.read.mock_calls == [call(4), call(22), call(4)]
    mock_log_writer.assert_awaited_with(payload)
