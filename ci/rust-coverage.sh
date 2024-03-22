#!/bin/sh

set -e
set -u
#set -o pipefail
set -x

# generate lcov and html report
nix develop --command cargo llvm-cov --no-report nextest --profile ci
nix develop --command cargo llvm-cov --no-report --doc
nix develop --command cargo llvm-cov report --doctests --lcov --output-path coverage-lcov.dat
nix develop --command cargo llvm-cov report --doctests --html

# convert lcov to cobertura
nix develop --command lcov_cobertura coverage-lcov.dat --output=coverage-cobertura.xml
