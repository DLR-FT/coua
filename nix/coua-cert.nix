{ lib
, stdenvNoCC
, coua
  # TODO add data items here
, ...
}:
stdenvNoCC.mkDerivation rec {
  pname = "coua-cert";
  description = "Certification Package for Coua";
  version = "0.1.0";
  src = ../.;
  buildPhase = ''
    ${lib.getExe coua} > $out
  '';
  meta = with lib; {
    inherit description;
    homepage = "https://gitlab.dlr.de/ft-ssy-avs/ap/coua";
    license = with licenses; [ mit /* or */ asl20 ];
    maintainers = [ ];
  };
}
