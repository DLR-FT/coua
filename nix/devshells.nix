{ self, pkgs, cargo-requirements, fenix, nixpkgs, ... }@inputs:
let
  cargoreqs = import cargo-requirements {
    inherit pkgs;
    fenix = fenix.packages.${pkgs.system};
  };
  system = inputs.pkgs.system;
  pkgs = import nixpkgs {
    inherit system;
    overlays = [
      fenix.overlays.default
    ];
  };
  run-checks = pkgs.writeShellScriptBin "run-checks" ''
    cargo check
    cargo nextest run
    cargo llvm-cov
  '';
  rustToolchain = pkgs.fenix.latest.withComponents [
    "cargo"
    "clippy"
    "rust-src"
    "rustc-dev"
    "rustc"
    "rustfmt"
    "llvm-tools-preview"
  ];
in
{
  default = pkgs.mkShell {
    inputsFrom = [
      self.packages.${pkgs.system}.default
    ];

    packages = [
      cargoreqs

      # Rust toolchain
      rustToolchain

      # Runs cargo test and generate coverage reports
      pkgs.cargo-llvm-cov

      # Runs cargo test and generate JUnit reports
      pkgs.cargo-nextest

      # Check commit message styles
      pkgs.cocogitto

      # Converts clippy reports to GitLab Code Quality Reports
      pkgs.gitlab-clippy

      # More up-to-date version of rust-analyzer
      pkgs.rust-analyzer-nightly

      # For converting lcov to cobertura
      pkgs.python311Packages.lcov_cobertura

      # Conversion utils
      pkgs.python3

      # e.g. for running checks in commit hooks
      run-checks
    ];
  };
}
