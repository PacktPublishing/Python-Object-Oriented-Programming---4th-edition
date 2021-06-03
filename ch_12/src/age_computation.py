"""
Python 3 Object-Oriented Programming

Chapter 12. Advanced Python Design Patterns
"""
from __future__ import annotations
from typing import Optional


class AgeCalculator:
    def __init__(self, birthday: str) -> None:
        self.year, self.month, self.day = (int(x) for x in birthday.split("-"))

    def calculate_age(self, date: str) -> int:
        year, month, day = (int(x) for x in date.split("-"))
        age = year - self.year
        if (month, day) < (self.month, self.day):
            age -= 1
        return age


test_age_calc = """
>>> ac = AgeCalculator("2018-10-26")
>>> ac.calculate_age("2020-03-18")
1
>>> ac.calculate_age("2028-01-18")
9

"""

import datetime


class DateAgeAdapter:
    def _str_date(self, date: datetime.date) -> str:
        return date.strftime("%Y-%m-%d")

    def __init__(self, birthday: datetime.date) -> None:
        birthday_text = self._str_date(birthday)
        self.calculator = AgeCalculator(birthday_text)

    def get_age(self, date: datetime.date) -> int:
        date_text = self._str_date(date)
        return self.calculator.calculate_age(date_text)


test_date_age_adapter = """
>>> import datetime
>>> ac = DateAgeAdapter(datetime.date(2018, 10, 26))
>>> ac.get_age(datetime.date(2020, 3, 18))
1
>>> ac.get_age(datetime.date(2028, 1, 18))
9

"""


class TimeSince:
    """Expects time as six digits, no punctuation."""

    def parse_time(self, time: str) -> tuple[float, float, float]:
        return (
            float(time[0:2]),
            float(time[2:4]),
            float(time[4:]),
        )

    def __init__(self, starting_time: str) -> None:
        self.hr, self.min, self.sec = self.parse_time(starting_time)
        self.start_seconds = ((self.hr * 60) + self.min) * 60 + self.sec

    def interval(self, log_time: str) -> float:
        log_hr, log_min, log_sec = self.parse_time(log_time)
        log_seconds = ((log_hr * 60) + log_min) * 60 + log_sec
        return log_seconds - self.start_seconds


test_timesince = """
>>> ts = TimeSince("000123")  # Log started at 00:01:23
>>> ts.interval("020304")
7301.0
>>> ts.interval("030405")
10962.0

"""


class IntervalAdapter:
    def __init__(self) -> None:
        self.ts: Optional[TimeSince] = None

    def time_offset(self, start: str, now: str) -> float:
        if self.ts is None:
            self.ts = TimeSince(start)
        else:
            h_m_s = self.ts.parse_time(start)
            if h_m_s != (self.ts.hr, self.ts.min, self.ts.sec):
                self.ts = TimeSince(start)
        return self.ts.interval(now)


test_interval_adapter = """
>>> ia = IntervalAdapter()
>>> ia.time_offset("000123", "020304")
7301.0
>>> ia.time_offset("000123", "030405")
10962.0

"""


class LogProcessor:
    def __init__(self, log_entries: list[tuple[str, str, str]]) -> None:
        self.log_entries = log_entries
        self.time_convert = IntervalAdapter()

    def report(self) -> None:
        first_time, first_sev, first_msg = self.log_entries[0]
        for log_time, severity, message in self.log_entries:
            if severity == "ERROR":
                first_time = log_time
            interval = self.time_convert.time_offset(first_time, log_time)
            print(f"{interval:8.2f} | {severity:7s} {message}")


test_log_processor = """
>>> data = [
...     ("000123", "INFO", "Gila Flats 1959-08-20"),
...     ("000142", "INFO", "test block 15"),
...     ("004201", "ERROR", "intrinsic field chamber door locked"),
...     ("004210.11", "INFO", "generator power active"),
...     ("004232.33", "WARNING", "extra mass detected")
... ]
>>> lp = LogProcessor(data)
>>> lp.report()
    0.00 | INFO    Gila Flats 1959-08-20
   19.00 | INFO    test block 15
    0.00 | ERROR   intrinsic field chamber door locked
    9.11 | INFO    generator power active
   31.33 | WARNING extra mass detected

"""


__test__ = {name: case for name, case in globals().items() if name.startswith("test_")}
