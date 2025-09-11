{
  description = "Coua - Certification ontologies using automation";

  inputs = {
    flake-utils = {
      url = "github:numtide/flake-utils";
    };

    nixpkgs = {
      url = "github:NixOS/nixpkgs/nixos-25.05";
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
      url = "github:DLR-FT/sphinx-ext-sparql";
      inputs.nixpkgs.follows = "nixpkgs";
    };

    malkoha = {
      url = "github:DLR-FT/malkoha";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs =
    {
      self,
      flake-utils,
      malkoha,
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
          pkgs = nixpkgs.legacyPackages.${system};
          project = pyproject-nix.lib.project.loadPyproject { projectRoot = ./.; };
          python = pkgs.python3.override {
            packageOverrides = final: prev: {
              coua = self.packages.${system}.coua;
              malkoha = self.packages.${system}.malkoha;
              morph-kgc = self.packages.${system}.morph-kgc;
              sphinx-sparql = self.packages.${system}.sphinx-sparql;
            };
          };
          treefmtEval = treefmt-nix.lib.evalModule pkgs ./nix/treefmt.nix;
        in
        {
          packages = {
            coua =
              let
                attrs = project.renderers.buildPythonPackage { inherit python; };
              in
              python.pkgs.buildPythonPackage attrs;
            malkoha = pkgs.python3Packages.callPackage malkoha { };
            morph-kgc = pkgs.python3Packages.callPackage ./nix/morph-kgc.nix { };
            sphinx-sparql = pkgs.python3Packages.callPackage sphinx-sparql { };
          };

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
                self.packages.${system}.coua # for testing itself
                self.packages.${system}.coua.passthru.optional-dependencies.test
                pythonEnv
                pkgs.ruff
                python
              ];
            };
          formatter = treefmtEval.config.build.wrapper;
        }
      );
}
