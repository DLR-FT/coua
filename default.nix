{
  buildPythonPackage,
  hatchling,
  morph-kgc,
  pyoxigraph,
  sphinx,
  sphinx-sparql,
  rdflib,
}:
buildPythonPackage {
  pname = "sphinx-sparql";
  pyproject = true;
  version = "0.1";
  src = ./.;
  build-system = [ hatchling ];
  dependencies = [
    sphinx
    pyoxigraph
    morph-kgc
    rdflib
    sphinx-sparql
  ];
}
