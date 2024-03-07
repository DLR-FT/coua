{ pkgs, fenix, nixd, nixpkgs, ... }@inputs:
let
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
    cargo llvm-cov nextest run
  '';
in
{
  default = pkgs.mkShell {
    packages = [
      # Nix language server
      nixd.packages.${system}.nixd

      # Rust toolchain
      (pkgs.fenix.complete.withComponents [
        "cargo"
        "clippy"
        "rust-src"
        "rustc"
        "rustfmt"
        "llvm-tools-preview"
      ])

      # Runs cargo test and generate coverage reports
      pkgs.cargo-llvm-cov

      # Runs cargo test and generate JUnit reports
      pkgs.cargo-nextest

      # Check commit message styles
      pkgs.cocogitto

      # Nightly version of rust-analyzer
      pkgs.fenix.rust-analyzer

      # Converts clippy reports to GitLab Code Quality Reports
      pkgs.gitlab-clippy

      # For converting lcov to cobertura
      pkgs.python311Packages.lcov_cobertura

      # e.g. for running checks in commit hooks
      run-checks
    ];
  };
}
