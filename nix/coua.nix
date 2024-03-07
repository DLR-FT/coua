{ lib, rustPlatform, ... }:
rustPlatform.buildRustPackage rec {
  pname = "coua";
  description = "Coua - Certification onthlogies using automation";
  version = "0.1.0";
  src = ../.;
  cargoLock = {
    lockFile = ../Cargo.lock;
  };
  meta = with lib; {
    inherit description;
    homepage = "https://gitlab.dlr.de/ft-ssy-avs/ap/coua";
    license = with licenses; [ mit /* or */ asl20 ];
    maintainers = [ ];
    mainProgram = "coua";
  };
}
