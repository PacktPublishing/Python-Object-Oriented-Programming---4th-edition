"""
Python 3 Object-Oriented Programming

Chapter 12. Advanced Python Design Patterns
"""
import csv
import datetime
import io
from pathlib import Path
from pytest import *
import sys
from unittest.mock import Mock

import car_sales

def test_new_vehicles_query(capsys, monkeypatch):
    connection = car_sales.test_setup(":memory:")
    monkeypatch.setattr(car_sales.sqlite3, 'connect', Mock(return_value=connection))
    nvq = car_sales.NewVehiclesQuery(":memory:")
    nvq.process_format()
    out, err = capsys.readouterr()
    reader = csv.DictReader(io.StringIO(out))
    assert list(reader) == [
        {'salesperson': 'Tim', 'amt': '16000', 'year': '2010', 'model': 'Honda Fit', 'new': 'true'},
        {'salesperson': 'Hannah', 'amt': '28000', 'year': '2009', 'model': 'Ford Mustang', 'new': 'true'},
        {'salesperson': 'Hannah', 'amt': '50000', 'year': '2010', 'model': 'Lincoln Navigator', 'new': 'true'},
    ]


@fixture
def mock_datetime(monkeypatch):
    module = Mock(
        date=Mock(
            today=Mock(
                return_value=datetime.date(2019, 10, 26)
            )
        )
    )
    monkeypatch.setattr(car_sales, 'datetime', module)
    return module

def test_sales_gross_query(mock_datetime, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    connection = car_sales.test_setup(":memory:")
    monkeypatch.setattr(car_sales.sqlite3, 'connect', Mock(return_value=connection))
    sgq = car_sales.SalesGrossQuery(":memory:")
    sgq.process_format()
    with Path("gross_sales_20191026.csv").open() as input:
        reader = csv.DictReader(input)
        data = list(reader)
    data.sort(key=lambda item: item['salesperson'])
    assert data == [
        {'salesperson': 'Hannah', 'total sales': '86000'},
        {'salesperson': 'Jason', 'total sales': '20000'},
        {'salesperson': 'Tim', 'total sales': '25000'},
    ]


