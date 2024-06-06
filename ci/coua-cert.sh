#/!bin/sh

set -e
set -u
set -o pipefail
set -x

python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python utils/import-junit.py junit-release.xml > resources/junit.xml.ttl
cargo-requirements --format ttl --testns "http://coua" --reqns "http://coua"
cargo run -p coua -- -o report -s ontologies/do178c resources/*
