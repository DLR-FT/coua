#!/bin/sh

set -e
set -u
#set -o pipefail
set -x

# pre-seed build cache
nix develop --command cargo build
nix develop --command cargo build --release

# generate docs
nix develop --command cargo doc --document-private-items

# generate clippy report
nix develop --command cargo clippy --message-format=json > clippy-lints.json
nix develop --command gitlab-clippy clippy-lints.json --output code-quality-report.json

# run tests
nix develop --command cargo nextest run --profile ci
mv target/nextest/ci/junit.xml junit-debug.xml
nix develop --command cargo nextest run --profile ci --release
mv target/nextest/ci/junit.xml junit-release.xml
