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
    PKG_CONFIG_PATH = "${pkgs.openssl.dev}/lib/pkgconfig";

    packages = [
      # For producing requirement graphs
      pkgs.graphviz

      # Nix language server
      nixd.packages.${system}.nixd

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

      # Openssl-sys
      pkgs.openssl
      pkgs.pkg-config

      # Conversion utils
      pkgs.python3

      # Oxigraph
      pkgs.llvmPackages.libclang
      pkgs.openssl
      pkgs.pkg-config
      pkgs.rustPlatform.bindgenHook

      # e.g. for running checks in commit hooks
      run-checks
    ];
  };
}
