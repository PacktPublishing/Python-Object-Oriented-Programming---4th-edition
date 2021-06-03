"""
Python 3 Object-Oriented Programming

Chapter 12. Advanced Python Design Patterns
"""
import images
from pytest import *
from pathlib import Path
from unittest.mock import Mock, call

@fixture
def mock_files(tmp_path):
    (tmp_path / ".tox").mkdir()
    (tmp_path / "f1.uml").write_text("@startuml\n")
    (tmp_path / "f2.uml").write_text("@startuml x.png\n@startuml y.png\n")
    (tmp_path / "x.png").write_bytes(bytes([137, 80, 78, 71, 13, 10, 26, 10]))
    return tmp_path

def test_find_uml(mock_files):
    finder = images.FindUML(mock_files)
    files = sorted(finder.uml_file_iter())
    assert files == [
        (Path("f1.uml"), Path("f1.png")),
        (Path("f2.uml"), Path("x.png")),
        (Path("f2.uml"), Path("y.png")),
    ]

@fixture
def mock_subprocess(monkeypatch):
    mock_module = Mock()
    monkeypatch.setattr(images, "subprocess", mock_module)
    return mock_module

def test_plant_uml(mock_subprocess, tmp_path):
    painter = images.PlantUML()
    painter.graphviz = "graphviz"
    painter.plantjar = "plantuml.jar"
    painter.process(Path("f2.uml"))
    assert mock_subprocess.run.mock_calls == [
        call(
            ["java", "-jar", "plantuml.jar", "-progress", "f2.uml"],
            env={"GRAPHVIZ_DOT": "graphviz"},
            check=True
        )
    ]

@fixture
def mock_finder():
    mock_uml = Mock(
        stat=Mock(
            return_value=Mock(
                st_mtime = 2
            )
        )
    )
    mock_png = Mock(
        stat=Mock(
            return_value=Mock(
                st_mtime = 1
            )
        )
    )
    return Mock(
        uml_file_iter=Mock(
            return_value=[(mock_uml,  mock_png)]
        )
    )

@fixture
def mock_painter():
    return Mock()

def test_generate_images(mock_finder, mock_painter, tmp_path):
    gen = images.GenerateImages(tmp_path)
    gen.finder = mock_finder
    gen.painter = mock_painter
    gen.make_all_images()
    assert mock_finder.uml_file_iter.mock_calls == [
        call()
    ]
    uml, png = mock_finder.uml_file_iter.return_value[0]
    assert mock_painter.process.mock_calls == [
        call(uml)
    ]
