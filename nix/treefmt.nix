{ pkgs, ... }:
{
  projectRootFile = "flake.nix";
  programs = {
    nixpkgs-fmt.enable = true;
    rustfmt.enable = true;
  };
}
