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
  version = "2.8.1";
  src = fetchFromGitHub {
    owner = "morph-kgc";
    repo = "morph-kgc";
    rev = "${version}";
    hash = "sha256-Hoa0Ul2CgkAlStB0O/fvOsjI0DbKKwEjV6Sz/pdh31w=";
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
  pythonRelaxDeps = [
    "falcon"
    "ruamel-yaml"
    "pyoxigraph"
  ];
}
