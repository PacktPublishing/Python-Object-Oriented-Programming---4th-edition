"""
Python 3 Object-Oriented Programming

Chapter 14.  Concurrency
"""
from pathlib import Path
from pytest import *
from unittest.mock import MagicMock, Mock, sentinel, call
import code_search


def test_import_result(tmp_path):
    i1 = code_search.ImportResult(tmp_path, {"math"})
    assert not i1.focus
    i2 = code_search.ImportResult(tmp_path, {"math", "typing"})
    assert i2.focus

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
    files = list(code_search.all_source(mock_directory, "*.py"))
    assert files == [
        mock_directory / "file1.py"
    ]

@fixture
def mock_code_1(tmp_path):
    source = tmp_path / "code_1.py"
    source.write_text("import math\nprint(math.pi)\n")
    return source

@fixture
def mock_code_2(tmp_path):
    source = tmp_path / "code_2.py"
    source.write_text("import math\nfrom typing import Callable\nprint(math.pi)\n")
    return source

def test_no_typing(mock_code_1):
    actual = code_search.find_imports(mock_code_1)
    assert actual == code_search.ImportResult(mock_code_1, {"math"})

def test_typing(mock_code_2):
    actual = code_search.find_imports(mock_code_2)
    assert actual == code_search.ImportResult(mock_code_2, {"math", "typing"})

@fixture
def mock_futures_pool(tmp_path, monkeypatch):
    future = Mock(
        result=Mock(
            return_value=code_search.ImportResult(tmp_path/"code.py", {"typing"}))
    )
    context = MagicMock(
        submit=Mock(return_value=future)
    )
    pool = MagicMock(
        __enter__=Mock(return_value=context)
    )
    pool_class = Mock(
        return_value=pool
    )
    monkeypatch.setattr(code_search.futures, 'ThreadPoolExecutor', pool_class)
    as_completed = Mock(
        side_effect=lambda futures: futures
    )
    monkeypatch.setattr(code_search.futures, 'as_completed', as_completed)
    return pool_class

@fixture
def mock_all_source(tmp_path, monkeypatch):
    paths = [tmp_path / "file1.py"]
    function = Mock(return_value=paths)
    monkeypatch.setattr(code_search, 'all_source', function)
    return paths

@fixture
def mock_time(monkeypatch):
    time = Mock(
        perf_counter=Mock(side_effect=[0.0, 0.42])
    )
    monkeypatch.setattr(code_search, 'time', time)
    return time

def test_main(mock_all_source, mock_futures_pool, mock_time, tmp_path, capsys, monkeypatch):
    monkeypatch.chdir(tmp_path)
    code_search.main(tmp_path)
    assert mock_futures_pool.mock_calls == [call(24)]
    context = mock_futures_pool.return_value.__enter__.return_value
    assert context.submit.mock_calls == [
        call(code_search.find_imports, tmp_path/"file1.py")
    ]
    future = context.submit.return_value
    assert future.result.mock_calls == [call()]
    out, err = capsys.readouterr()
    target_path = "code.py"
    assert out.splitlines() == [
        '',
        str(tmp_path),
        f"-> {str(target_path)} {{'typing'}}",
        f"Searched 1 files in {str(tmp_path)} at 420.000ms/file",
    ]
