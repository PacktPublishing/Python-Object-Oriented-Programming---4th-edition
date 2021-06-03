"""
Python 3 Object-Oriented Programming Case Study

Chapter 9. Strings and Serialization

This is run in the ch_09 directory::

    python tests/data_conversion.py

It copies the root-level bezdekIris.data to create bezdekIris.json.
"""
import csv
import json
from pathlib import Path
import yaml

header = [
    "sepal_length",  # in cm
    "sepal_width",  # in cm
    "petal_length",  # in cm
    "petal_width",  # in cm
    "species",  # Iris-setosa, Iris-versicolour, Iris-virginica
]

def csv_to_json_list(source: Path, target: Path) -> None:
    """Write in standard JSON notation."""
    with source.open() as source_file, target.open('w') as target_file:
        dict_iter = csv.DictReader(source_file, header)
        conversion_iter = (
            dict(
                sepal_length=float(row["sepal_length"]),
                sepal_width=float(row["sepal_width"]),
                petal_length=float(row["petal_length"]),
                petal_width=float(row["petal_width"]),
                species=row["species"]
            )
            for row in dict_iter
        )
        dataset = list(conversion_iter)
        json.dump(dataset, target_file, indent=2)

def csv_to_ndjson(source: Path, target: Path) -> None:
    """This uses newline-delimited JSON, see http://ndjson.org."""
    with source.open() as source_file, target.open('w') as target_file:
        dict_iter = csv.DictReader(source_file, header)
        conversion_iter = (
            dict(
                sepal_length=float(row["sepal_length"]),
                sepal_width=float(row["sepal_width"]),
                petal_length=float(row["petal_length"]),
                petal_width=float(row["petal_width"]),
                species=row["species"]
            )
            for row in dict_iter
        )
        for document in conversion_iter:
            line = json.dumps(document)
            print(line, file=target_file)

def csv_to_yaml(source: Path, target: Path) -> None:
    """Write in YAML notation"""
    with source.open() as source_file, target.open('w') as target_file:
        dict_iter = csv.DictReader(source_file, header)
        conversion_iter = (
            dict(
                sepal_length=float(row["sepal_length"]),
                sepal_width=float(row["sepal_width"]),
                petal_length=float(row["petal_length"]),
                petal_width=float(row["petal_width"]),
                species=row["species"]
            )
            for row in dict_iter
        )
        yaml.dump_all(conversion_iter, target_file)

def main():
    csv_to_json_list(
        source=Path.cwd().parent/"bezdekIris.data",
        target=Path.cwd().parent/"bezdekIris.json",
    )
    csv_to_ndjson(
        source=Path.cwd().parent/"bezdekIris.data",
        target=Path.cwd().parent/"bezdekIris.ndjson",
    )
    csv_to_yaml(
        source=Path.cwd().parent/"bezdekIris.data",
        target=Path.cwd().parent/"bezdekIris.yaml",
    )

if __name__ == "__main__":
    main()
