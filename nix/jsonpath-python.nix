{
  buildPythonPackage,
  fetchPypi,
  setuptools,
}:
buildPythonPackage rec {
  pname = "jsonpath-python";
  pyproject = true;
  version = "1.0.6";
  src = fetchPypi {
    inherit pname version;
    hash = "sha256-3Vvkpy2KKZXD9YPPgr880alUTP2r8tIllbZ6/wc0lmY=";
  };
  build-system = [ setuptools ];
}
