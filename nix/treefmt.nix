{ pkgs, ... }:
{
  projectRootFile = "flake.nix";
  programs = {
    black.enable = true;
    nixfmt = {
      enable = true;
      package = pkgs.nixfmt-rfc-style;
    };
    rustfmt.enable = true;
  };
}
