{
  buildPythonPackage,
  fetchFromGitHub,
  pkg-config,
  rustPlatform,
}:
buildPythonPackage rec {
  pname = "pyoxigraph";
  pyproject = true;
  version = "0.3.22";
  src = fetchFromGitHub {
    owner = "oxigraph";
    repo = "oxigraph";
    rev = "v${version}";
    fetchSubmodules = true;
    hash = "sha256-zwUiUDWdrmLF+Qj9Jy6JGXHaBskRnm+pMKW2GKGGeN8=";
  };
  buildAndTestSubdir = "python";
  cargoDeps = rustPlatform.fetchCargoTarball {
    inherit src;
    name = "${pname}-${version}";
    hash = "sha256-ukmcFHc+NLRtLtrTmF07N7XVQG/TU6Pw/yKtKh+BFIw=";
  };
  nativeBuildInputs = [
    pkg-config
    rustPlatform.bindgenHook
    rustPlatform.cargoSetupHook
    rustPlatform.maturinBuildHook
  ];
}
