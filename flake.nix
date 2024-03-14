{
  description = "Coua - Certification onthlogies using automation";

  inputs = {
    fenix = {
      url = "github:nix-community/fenix";
      inputs.nixpkgs.follows = "nixpkgs";
    };

    nixd = {
      url = "github:nix-community/nixd";
      inputs.nixpkgs.follows = "nixpkgs";
    };

    nixpkgs = {
      url = "github:NixOS/nixpkgs/nixos-23.11";
    };

    treefmt-nix = {
      url = "github:numtide/treefmt-nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs = { self, fenix, nixd, nixpkgs, treefmt-nix }@inputs:
    let
      systems = [ "aarch64-linux" "x86_64-linux" ];
      eachSystem = f: nixpkgs.lib.genAttrs systems (system: f (import nixpkgs { inherit system; }));
      treefmtEval = eachSystem (pkgs: treefmt-nix.lib.evalModule pkgs ./nix/treefmt.nix);
    in
    {
      checks = eachSystem (pkgs: import ./nix/checks.nix (inputs // { inherit pkgs treefmtEval; }));
      devShells = eachSystem (pkgs: import ./nix/devshells.nix (inputs // { inherit pkgs; }));
      formatter = eachSystem (pkgs: treefmtEval.${pkgs.system}.config.build.wrapper);
      packages = eachSystem (pkgs:
        let
          fenix' = fenix.packages.${pkgs.system};
          rustToolchain = with fenix'; combine (with latest; [ rustc cargo rustc-dev rust-src ]);
          rustPlatform = (pkgs.makeRustPlatform { cargo = rustToolchain; rustc = rustToolchain; });
        in
        rec {
          coua = pkgs.callPackage ./nix/coua.nix { inherit rustPlatform; };
          coua-cert = pkgs.callPackage ./nix/coua-cert.nix { inherit coua; };
          default = coua;
        });
    };
}
