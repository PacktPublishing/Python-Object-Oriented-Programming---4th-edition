"""
Python 3 Object-Oriented Programming

Chapter 14.  Concurrency
"""
from pytest import *
from unittest.mock import Mock, sentinel, call
import directory_search

@fixture
def mock_query_queue():
    return Mock(
        get=Mock(side_effect=["xyzzy", None])
    )

@fixture
def mock_result_queue():
    return Mock(
        put=Mock()
    )

@fixture
def mock_paths(tmp_path):
    f1 = tmp_path / "file1"
    f1.write_text("not in file1\n")
    f2 = tmp_path / "file2"
    f2.write_text("file2 contains xyzzy\n")
    return [f1, f2]


def test_search(mock_paths, mock_query_queue, mock_result_queue):
    directory_search.search(mock_paths, mock_query_queue, mock_result_queue)
    assert mock_query_queue.get.mock_calls == [call(), call()]
    assert mock_result_queue.put.mock_calls == [
        call(['file2 contains xyzzy'])
    ]


@fixture
def mock_directory(tmp_path):
    f1 = tmp_path / "file1.py"
    f1.write_text("# file1.py\n")
    d1 = tmp_path / ".tox"
    d1.mkdir()
    f2 = tmp_path / ".tox" / "file2.py"
    f2.write_text("# file2.py\n")
    return tmp_path

def test_all_source(mock_directory):
    files = list(directory_search.all_source(mock_directory, "*.py"))
    assert files == [
        mock_directory / "file1.py"
    ]


@fixture
def mock_queue(monkeypatch):
    mock_instance = Mock(
        name="mock Queue",
        put=Mock(),
        get=Mock(return_value=["line with text"])
    )
    mock_queue_class = Mock(
        return_value=mock_instance
    )
    monkeypatch.setattr(directory_search, "Queue", mock_queue_class)
    return mock_queue_class


@fixture
def mock_process(monkeypatch):
    mock_instance = Mock(
        name="mock Process",
        start=Mock(),
        join=Mock()
    )
    mock_process_class = Mock(
        return_value=mock_instance
    )
    monkeypatch.setattr(directory_search, "Process", mock_process_class)
    return mock_process_class

def test_directory_search(mock_queue, mock_process, mock_paths):
    ds_instance = directory_search.DirectorySearch()
    ds_instance.setup_search(mock_paths, cpus=2)

    assert mock_queue.mock_calls == [call(), call(), call()]
    assert mock_process.mock_calls == [
        call(
            target=directory_search.search,
            args=(mock_paths[0::2], mock_queue.return_value, mock_queue.return_value)
        ),
        call(
            target=directory_search.search,
            args=(mock_paths[1::2], mock_queue.return_value, mock_queue.return_value)
        )
    ]
    assert mock_process.return_value.start.mock_calls == [call(), call()]
    assert ds_instance.query_queues == [mock_queue.return_value, mock_queue.return_value]
    assert ds_instance.results_queue == mock_queue.return_value
    assert ds_instance.search_workers == [mock_process.return_value, mock_process.return_value ]

    result = list(ds_instance.search("text"))

    assert result == ['line with text', 'line with text']
    assert mock_queue.return_value.put.mock_calls == [call("text"), call("text")]
    assert mock_queue.return_value.get.mock_calls == [call(), call()]

    ds_instance.teardown_search()
    assert mock_queue.return_value.put.mock_calls == [call("text"), call("text"), call(None), call(None)]
    assert mock_process.return_value.join.mock_calls == [call(), call()]
