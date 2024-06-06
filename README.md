# Coua

Coua means **c**ertification **o**nthologies **u**sing **a**utomation or a type of [bird](https://en.wikipedia.org/wiki/Coua).

```sh
cargo run -p coua -- -s ontologies/do178c resources/*
```

## Importing data

RML is recommended for importing data as resources to Coua.
Example mappings from data files to RDF can be found in `mappings`.

### Example

This takes a JUnit XML output file as an input and converts it into Turtle notation.
The output file can then be specified as an input to `coua`.

```sh
python utils/import-junit.py target/nextest/ci/junit.xml > out.ttl
```
