"""
Python 3 Object-Oriented Programming Case Study

Chapter 5, When to Use Object-Oriented Programming
"""
from pytest import *
import csv
from model import SampleReader, BadSampleRow, Sample

@fixture
def good_sample_csv_file(tmp_path):
    test_data = tmp_path/"iris.data"
    with test_data.open('w', newline="") as tmpfile:
        tmpfile.write("5.0,3.3,1.4,0.2,Iris-setosa\r\n")
        tmpfile.write("7.0,3.2,4.7,1.4,Iris-versicolor\r\n")
    return test_data

@fixture
def bad_sample_csv_file(tmp_path):
    test_data = tmp_path/"iris.data"
    with test_data.open('w', newline="") as tmpfile:
        tmpfile.write("5.0,3.3,1.4,0.2,Iris-setosa\r\n")
        tmpfile.write("7.0,Nope,4.7,1.4,Iris-versicolor\r\n")
        tmpfile.write("7.0,3.2,4.7,1.4,Wrong\r\n")
    return test_data

def test_good_simple_reader(good_sample_csv_file):
    rdr = SampleReader(good_sample_csv_file)
    samples = list(rdr.sample_iter())
    assert samples == [
        Sample(sepal_length=5.0, sepal_width=3.3, petal_length=1.4, petal_width=0.2, ),
        Sample(sepal_length=7.0, sepal_width=3.2, petal_length=4.7, petal_width=1.4, ),
    ]

def test_bad_simple_reader(bad_sample_csv_file):
    rdr = SampleReader(bad_sample_csv_file)
    with raises(BadSampleRow) as ex:
        samples = list(rdr.sample_iter())
    assert ex.value.args == (
        "Invalid {'sepal_length': '7.0', 'sepal_width': 'Nope', 'petal_length': "
        "'4.7', 'petal_width': '1.4', 'class': 'Iris-versicolor'}",
    )
