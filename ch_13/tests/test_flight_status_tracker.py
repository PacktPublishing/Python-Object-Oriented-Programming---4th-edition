"""
Python 3 Object-Oriented Programming

Chapter 13.  Testing Object-Oriented Programs.
"""
import datetime
import flight_status_redis
from unittest.mock import Mock, patch, call
import pytest


@pytest.fixture
def mock_redis() -> Mock:
    mock_redis_instance = Mock(set=Mock(return_value=True))
    return mock_redis_instance


@pytest.fixture
def tracker(
    monkeypatch: pytest.MonkeyPatch, mock_redis: Mock
) -> flight_status_redis.FlightStatusTracker:
    """Depending on the test scenario, this may require a running REDIS server."""
    fst = flight_status_redis.FlightStatusTracker()
    monkeypatch.setattr(fst, "redis", mock_redis)
    return fst


def test_monkeypatch_class(
    tracker: flight_status_redis.FlightStatusTracker, mock_redis: Mock
) -> None:
    # with patch.object(tracker, "redis", mock_redis):
    with pytest.raises(ValueError) as ex:
        tracker.change_status("AC101", "lost")  # type: ignore [arg-type]
    assert ex.value.args[0] == "'lost' is not a valid Status"
    assert mock_redis.set.call_count == 0


def test_patch_class(
    tracker: flight_status_redis.FlightStatusTracker, mock_redis: Mock
) -> None:
    fake_now = datetime.datetime(2020, 10, 26, 23, 24, 25)
    utc = datetime.timezone.utc
    # with patch.object(tracker, "redis", mock_redis):
    with patch("flight_status_redis.datetime") as mock_datetime:
        mock_datetime.datetime = Mock(now=Mock(return_value=fake_now))
        mock_datetime.timezone = Mock(utc=utc)
        tracker.change_status("AC101", flight_status_redis.Status.ON_TIME)
    mock_datetime.datetime.now.assert_called_once_with(tz=utc)
    expected = f"2020-10-26T23:24:25|ON TIME"
    mock_redis.set.assert_called_once_with("flightno:AC101", expected)
    # Also
    assert mock_datetime.datetime.now.mock_calls == [call(tz=utc)]
    assert mock_redis.set.mock_calls == [call("flightno:AC101", expected)]


def test_patch_class_2(
    tracker: flight_status_redis.FlightStatusTracker, mock_redis: Mock
) -> None:
    """More focused patch"""
    mock_datetime_now = Mock(return_value=datetime.datetime(2020, 10, 26, 23, 24, 25))
    with patch("flight_status_redis.datetime.datetime", now=mock_datetime_now):
        tracker.change_status("AC101", flight_status_redis.Status.ON_TIME)
    mock_datetime_now.assert_called_once_with(tz=datetime.timezone.utc)
    expected = f"2020-10-26T23:24:25|ON TIME"
    mock_redis.set.assert_called_once_with("flightno:AC101", expected)
    # Also
    assert mock_datetime_now.mock_calls == [call(tz=datetime.timezone.utc)]
    assert mock_redis.set.mock_calls == [call("flightno:AC101", expected)]
