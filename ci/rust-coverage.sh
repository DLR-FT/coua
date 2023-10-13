#!/bin/sh

set -e
set -u
set -o pipefail
set -x

# run tests
nix develop --command cargo llvm-cov nextest run --profile ci

# generate lcov and html report
nix develop --command cargo llvm-cov --no-run --html
nix develop --command cargo llvm-cov --no-run --lcov --output-path coverage-lcov.dat

# convert lcov to cobertura
nix develop --command lcov_cobertura coverage-lcov.dat --base-dir=$(pwd) --output=coverage-cobertura.xml
