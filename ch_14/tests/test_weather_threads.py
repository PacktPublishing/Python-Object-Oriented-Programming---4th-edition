"""
Python 3 Object-Oriented Programming

Chapter 14.  Concurrency
"""
from pytest import *
from unittest.mock import Mock, mock_open, call
import weather_threads

def test_station():
    halifax = weather_threads.Station("NS", "s0000318")
    assert halifax.path == "/NS/s0000318_e.xml"
    assert halifax.url == "https://dd.weather.gc.ca/citypage_weather/xml/NS/s0000318_e.xml"

@fixture
def temp_getter():
    return weather_threads.TempGetter("Halifax")

@fixture
def mock_urlopen(monkeypatch):
    urlopen = mock_open(
        read_data="""<?xml version='1.0'?><siteData><currentConditions><temperature unitType="metric" units="C">42</temperature></currentConditions></siteData>"""
    )
    monkeypatch.setattr(weather_threads, 'urlopen', urlopen)
    return urlopen

def test_temp_getter(temp_getter, mock_urlopen):
    temp_getter.run()
    assert temp_getter.temperature == "42"
    mock_urlopen.assert_called_once_with(
        'https://dd.weather.gc.ca/citypage_weather/xml/NS/s0000318_e.xml'
    )
