{ lib, rustPlatform, pkg-config, llvmPackages, openssl, stdenv, ... }:
rustPlatform.buildRustPackage {
  pname = "coua";
  version = "0.1.0";
  src = ../.;

  buildInputs = [
    stdenv.cc.cc # libstdc++.6
    llvmPackages.clang
    openssl
  ];

  nativeBuildInputs = [
    pkg-config
    rustPlatform.bindgenHook
  ];

  cargoLock = {
    lockFile = ../Cargo.lock;
  };

  meta = with lib; {
    description = "Coua - Certification onthlogies using automation";
    homepage = "https://gitlab.dlr.de/ft-ssy-avs/ap/coua";
    license = with licenses; [ mit /* or */ asl20 ];
    maintainers = [ ];
    mainProgram = "coua";
  };
}
