
# Case Study for Chapter 9, Strings and Serialization

## Serialization

```
>>> from model import TrainingKnownSample
>>> s1 = TrainingKnownSample(
...     sepal_length=5.1, sepal_width=3.5, petal_length=1.4, petal_width=0.2, species="Iris-setosa")
>>> serialized = repr(s1)
>>> serialized
"TrainingKnownSample(sepal_length=5.1, sepal_width=3.5, petal_length=1.4, petal_width=0.2, species='Iris-setosa', )"
>>> s2 = eval(serialized)
>>> s1 == s2
True
>>> id(s1) == id(s2)
False


```

## Built-in Serialization

## CSV Format Designs

### CSV Dictionary Reader

```
>>> from model import CSVIrisReader
>>> from pathlib import Path
>>> test_data = Path.cwd().parent/"bezdekIris.data"
>>> rdr = CSVIrisReader(test_data)
>>> samples = list(rdr.data_iter())
>>> len(samples)
150
>>> samples[0]
{'sepal_length': '5.1', 'sepal_width': '3.5', 'petal_length': '1.4', 'petal_width': '0.2', 'species': 'Iris-setosa'}


```

```
>>> from model import TrainingData
>>> training_data = TrainingData("besdekIris")
>>> rdr = CSVIrisReader(test_data)
>>> training_data.load(rdr.data_iter())


```

### CSV Reader

### CSV Dialects

## JSON Serialization

### Newline Delimited JSON

### JSON Validation

## The YAML Variant

