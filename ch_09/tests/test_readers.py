"""
Python 3 Object-Oriented Programming Case Study

Chapter 9. Strings and Serialization
"""
from pytest import *
import csv
import json
import yaml
from model import (
    CSVIrisReader, CSVIrisReader_2,
    JSONIrisReader, NDJSONIrisReader, ValidatingNDJSONIrisReader,
    IRIS_SCHEMA,
    YAMLIrisReader
)

@fixture
def sample_csv_file(tmp_path):
    test_data = tmp_path/"iris.data"
    with test_data.open('w', newline="") as tmpfile:
        tmpfile.write("5.0,3.3,1.4,0.2,Iris-setosa\r\n")
        tmpfile.write("7.0,3.2,4.7,1.4,Iris-versicolor\r\n")
    return test_data

def test_csv_iris_reader(sample_csv_file):
    rdr = CSVIrisReader(sample_csv_file)
    data = list(rdr.data_iter())
    assert data == [
        {'sepal_length': '5.0', 'sepal_width': '3.3', 'petal_length': '1.4', 'petal_width': '0.2', 'species': 'Iris-setosa'},
        {'sepal_length': '7.0', 'sepal_width': '3.2', 'petal_length': '4.7', 'petal_width': '1.4', 'species': 'Iris-versicolor'}
    ]

def test_csv_iris_reader_2(sample_csv_file):
    rdr = CSVIrisReader_2(sample_csv_file)
    data = list(rdr.data_iter())
    assert data == [
        {'sepal_length': '5.0', 'sepal_width': '3.3', 'petal_length': '1.4', 'petal_width': '0.2', 'species': 'Iris-setosa'},
        {'sepal_length': '7.0', 'sepal_width': '3.2', 'petal_length': '4.7', 'petal_width': '1.4', 'species': 'Iris-versicolor'}
    ]

@fixture
def sample_json_file(tmp_path):
    test_data = tmp_path/"iris.json"
    data = [
      {
        "sepal_length": 5.0,
        "sepal_width": 3.3,
        "petal_length": 1.4,
        "petal_width": 0.2,
        "species": "Iris-setosa"
      },
      {
        "sepal_length": 7.0,
        "sepal_width": 3.2,
        "petal_length": 4.7,
        "petal_width": 1.4,
        "species": "Iris-versicolor"
      }
    ]
    with test_data.open('w') as tmpfile:
        json.dump(data, tmpfile)
    return test_data

def test_json_iris_reader(sample_json_file):
    rdr = JSONIrisReader(sample_json_file)
    data = list(rdr.data_iter())
    assert data == [
        {'sepal_length': 5.0, 'sepal_width': 3.3, 'petal_length': 1.4, 'petal_width': 0.2, 'species': 'Iris-setosa'},
        {'sepal_length': 7.0, 'sepal_width': 3.2, 'petal_length': 4.7, 'petal_width': 1.4, 'species': 'Iris-versicolor'}
    ]


@fixture
def sample_ndjson_file(tmp_path):
    test_data = tmp_path/"iris.json"
    data = [
      {
        "sepal_length": 5.0,
        "sepal_width": 3.3,
        "petal_length": 1.4,
        "petal_width": 0.2,
        "species": "Iris-setosa"
      },
      {
        "sepal_length": 7.0,
        "sepal_width": 3.2,
        "petal_length": 4.7,
        "petal_width": 1.4,
        "species": "Iris-versicolor"
      }
    ]
    with test_data.open('w') as tmpfile:
        for sample in data:
            print(json.dumps(sample), file=tmpfile)
    return test_data

def test_ndjson_iris_reader(sample_ndjson_file):
    rdr = NDJSONIrisReader(sample_ndjson_file)
    data = list(rdr.data_iter())
    assert data == [
        {'sepal_length': 5.0, 'sepal_width': 3.3, 'petal_length': 1.4, 'petal_width': 0.2, 'species': 'Iris-setosa'},
        {'sepal_length': 7.0, 'sepal_width': 3.2, 'petal_length': 4.7, 'petal_width': 1.4, 'species': 'Iris-versicolor'}
    ]


def test_validating_ndjson_iris_reader(sample_ndjson_file):
    rdr = ValidatingNDJSONIrisReader(sample_ndjson_file, IRIS_SCHEMA)
    data = list(rdr.data_iter())
    assert data == [
        {'sepal_length': 5.0, 'sepal_width': 3.3, 'petal_length': 1.4, 'petal_width': 0.2, 'species': 'Iris-setosa'},
        {'sepal_length': 7.0, 'sepal_width': 3.2, 'petal_length': 4.7, 'petal_width': 1.4, 'species': 'Iris-versicolor'}
    ]

@fixture
def sample_yaml_file(tmp_path):
    test_data = tmp_path/"iris.yaml"
    data = [
      {
        "sepal_length": 5.0,
        "sepal_width": 3.3,
        "petal_length": 1.4,
        "petal_width": 0.2,
        "species": "Iris-setosa"
      },
      {
        "sepal_length": 7.0,
        "sepal_width": 3.2,
        "petal_length": 4.7,
        "petal_width": 1.4,
        "species": "Iris-versicolor"
      }
    ]
    with test_data.open('w') as tmpfile:
        yaml.dump_all(data, tmpfile)
    return test_data

def test_yaml_iris_reader(sample_yaml_file):
    rdr = YAMLIrisReader(sample_yaml_file)
    data = list(rdr.data_iter())
    assert data == [
        {'sepal_length': 5.0, 'sepal_width': 3.3, 'petal_length': 1.4, 'petal_width': 0.2, 'species': 'Iris-setosa'},
        {'sepal_length': 7.0, 'sepal_width': 3.2, 'petal_length': 4.7, 'petal_width': 1.4, 'species': 'Iris-versicolor'}
    ]
