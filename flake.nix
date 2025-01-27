{
  description = "Coua - Certification ontologies using automation";

  inputs = {
    flake-utils = {
      url = "github:numtide/flake-utils";
    };

    nixpkgs = {
      url = "github:NixOS/nixpkgs/nixos-24.05";
    };

    treefmt-nix = {
      url = "github:numtide/treefmt-nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };

    pyproject-nix = {
      url = "github:nix-community/pyproject.nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };

    sphinx-sparql = {
      url = "git+ssh://git@gitlab.dlr.de/ft-ssy-avs/ap/sphinx-sparql";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs =
    {
      self,
      flake-utils,
      nixpkgs,
      pyproject-nix,
      sphinx-sparql,
      treefmt-nix,
      ...
    }@inputs:
    flake-utils.lib.eachSystem
      [
        "aarch64-linux"
        "x86_64-linux"
      ]
      (
        system:
        let
          pkgs = import nixpkgs {
            inherit system;
            overlays = [
              sphinx-sparql.overlays.default
              self.overlays.default
            ];
          };
          project = pyproject-nix.lib.project.loadPyproject { projectRoot = ./.; };
          python = pkgs.python3;
          treefmtEval = treefmt-nix.lib.evalModule pkgs ./nix/treefmt.nix;
        in
        rec {
          packages.default =
            let
              attrs = project.renderers.buildPythonPackage { inherit python; };
            in
            python.pkgs.buildPythonPackage attrs;

          checks = import ./nix/checks.nix (inputs // { inherit pkgs treefmtEval; });
          devShells.default =
            let
              arg = project.renderers.withPackages { inherit python; };
              pythonEnv = python.withPackages arg;
            in
            pkgs.mkShell {
              packages = [
                pkgs.gnumake
                pkgs.nodePackages.prettier
                pkgs.nixpkgs-fmt
                pkgs.cocogitto
                pkgs.jq
                pkgs.python3
                pkgs.pylint
                pkgs.oxigraph
                packages.default # for testing itself
                packages.default.passthru.optional-dependencies.test
                pythonEnv
                pkgs.ruff-lsp
                pkgs.ruff
                python.pkgs.pythonPackages.morph-kgc
                python.pkgs.pythonPackages.pylsp-rope
                python.pkgs.pythonPackages.python-lsp-ruff
                python.pkgs.pythonPackages.python-lsp-server
              ];
            };
          formatter = treefmtEval.config.build.wrapper;
        }
      )
    // {
      overlays.default = final: prev: {
        coua = self.packages.${prev.system}.default;
        python3 = prev.python3.override {
          packageOverrides = final: prev: {
            coua = prev.pythonPackages.callPackage ./default.nix { };
            jsonpath-python = prev.pythonPackages.callPackage ./nix/jsonpath-python.nix { };
            morph-kgc = prev.pythonPackages.callPackage ./nix/morph-kgc.nix { };
            pyoxigraph = prev.pythonPackages.callPackage ./nix/pyoxigraph.nix { };
            sphinx-sparql = prev.pythonPackages.callPackage sphinx-sparql { };
          };
        };
      };
    };
}
