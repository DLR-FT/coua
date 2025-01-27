{
  buildPythonPackage,
  flit-core,
  morph-kgc,
  pyoxigraph,
  sphinx,
  sphinx-sparql,
  rdflib,
}:
buildPythonPackage {
  pname = "coua";
  pyproject = true;
  src = ./.;
  build-system = [ flit-core ];
  dependencies = [
    sphinx
    pyoxigraph
    morph-kgc
    rdflib
    sphinx-sparql
  ];
}
