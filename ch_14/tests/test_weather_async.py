"""
Python 3 Object-Oriented Programming

Chapter 14.  Concurrency
"""
import asyncio
from httpx import URL
from pytest import *
from unittest.mock import Mock, AsyncMock, mock_open, call
import weather_async

def test_zone():
    eb = weather_async.Zone("Eastern Bay", "ANZ540", "073540")
    assert eb.forecast_url == "https://tgftp.nws.noaa.gov/data/forecasts/marine/coastal/an/anz540.txt"

@fixture
def marine_wx():
    z = weather_async.Zone("Eastern Bay", "ANZ540", "073540")
    return weather_async.MarineWX(z)

@fixture
def mock_urlopen(monkeypatch):
    urlopen = mock_open(
        read_data="""Heading\n...Advisory...\n.DAY...details.\n""".encode("utf-8")
    )
    monkeypatch.setattr(weather_async, 'urlopen', urlopen)
    return urlopen

@fixture
def mock_httpx_client(httpx_mock):
    httpx_mock.add_response(
        method="GET",
        data="""Heading\n...Advisory...\n.DAY...details.\n"""
    )
    return httpx_mock

def test_marine_wx(marine_wx, mock_httpx_client, httpx_mock):
    async def when():
        return await marine_wx.run()
    result_0 = asyncio.run(when())
    assert marine_wx.advisory == "Advisory"
    # mock_urlopen.assert_called_once_with(
    #     marine_wx.zone.forecast_url
    # )
    assert (
        httpx_mock.get_request().url == URL('https://tgftp.nws.noaa.gov/data/forecasts/marine/coastal/an/anz540.txt')
    )
