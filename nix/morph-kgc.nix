{
  buildPythonPackage,
  fetchFromGitHub,
  hatchling,
  duckdb,
  elementpath,
  falcon,
  jsonpath-python,
  pandas,
  pyoxigraph,
  pythonRelaxDepsHook,
  rdflib,
  ruamel-yaml,
  sqlalchemy,
}:
buildPythonPackage rec {
  pname = "morph-kgc";
  pyproject = true;
  version = "2.8.0";
  src = fetchFromGitHub {
    owner = "morph-kgc";
    repo = "morph-kgc";
    rev = "${version}";
    hash = "sha256-jualqkAUwAvKOiv2XzHLZl3owUiV6sjnCZ5Iz40E6Ps=";
  };
  nativeBuildInputs = [ pythonRelaxDepsHook ];
  build-system = [ hatchling ];
  propagatedBuildInputs = [
    duckdb
    elementpath
    falcon
    jsonpath-python
    pandas
    pyoxigraph
    rdflib
    ruamel-yaml
    sqlalchemy
  ];
  pythonRelaxDeps = [ "ruamel-yaml" ];
}
