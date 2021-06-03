"""
Python 3 Object-Oriented Programming

Chapter 11. Common Design Patterns
"""
import image_filler
from pytest import *
from unittest.mock import Mock, call, sentinel

@fixture
def mock_image(monkeypatch):
    input_image = Mock(
        size=(512, 384),
        resize=Mock()
    )
    output_image = Mock(
        paste=Mock(),
        size=(1920, 1080)
    )
    image_class = Mock(
        open=Mock(return_value=input_image),
        new=Mock(return_value=output_image)
    )
    monkeypatch.setattr(image_filler, 'Image', image_class)
    return image_class

def test_tiled_strategy(mock_image, tmp_path):
    ts = image_filler.TiledStrategy()
    result = ts.make_background(tmp_path, (1920, 1080))
    assert mock_image.open.mock_calls == [call(tmp_path)]
    assert mock_image.new.mock_calls == [call("RGB", (1920, 1080))]
    assert result == mock_image.new.return_value
    assert mock_image.new.return_value.paste.mock_calls == [
        call(mock_image.open.return_value, (0, 0, 512, 384)),
        call(mock_image.open.return_value, (0, 384, 512, 768)),
        call(mock_image.open.return_value, (0, 768, 512, 1152)),
        call(mock_image.open.return_value, (512, 0, 1024, 384)),
        call(mock_image.open.return_value, (512, 384, 1024, 768)),
        call(mock_image.open.return_value, (512, 768, 1024, 1152)),
        call(mock_image.open.return_value, (1024, 0, 1536, 384)),
        call(mock_image.open.return_value, (1024, 384, 1536, 768)),
        call(mock_image.open.return_value, (1024, 768, 1536, 1152)),
        call(mock_image.open.return_value, (1536, 0, 2048, 384)),
        call(mock_image.open.return_value, (1536, 384, 2048, 768)),
        call(mock_image.open.return_value, (1536, 768, 2048, 1152))
    ]

def test_centered_strategy(mock_image, tmp_path):
    cs = image_filler.CenteredStrategy()
    result = cs.make_background(tmp_path, (1920, 1080))
    assert mock_image.open.mock_calls == [call(tmp_path)]
    assert mock_image.new.mock_calls == [call("RGB", (1920, 1080))]
    assert result == mock_image.new.return_value
    assert mock_image.new.return_value.paste.mock_calls == [
        call(mock_image.open.return_value, (704, 348, 1216, 732))
    ]

def test_scaled_strategy(mock_image, tmp_path):
    ss = image_filler.ScaledStrategy()
    result = ss.make_background(tmp_path, (1920, 1080))
    assert mock_image.open.mock_calls == [call(tmp_path)]
    assert result == mock_image.open.return_value.resize.return_value
    assert mock_image.open.return_value.resize.mock_calls == [
        call((1920, 1080))
    ]
