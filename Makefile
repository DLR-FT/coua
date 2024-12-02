.PHONY: all check-formatting commit-check mypy check test doc clean cert serve

SOURCEDIRS := "coua"
PYTHON_SRCS := $(shell find $(SOURCEDIRS) -name '*.py')
PYTHON_SRCS += $(wildcard tests/*.py)

all: check test doc cert

check-format:
	nix fmt -- --fail-on-change --no-cache

commit-check:
	cog check

mypy:
	mypy coua

test:
	pytest --cov-branch --junit-xml=junit.xml --cov=coua --cov-report term --cov-report xml:coverage.xml

coverage.xml: test

junit.xml: test

traces.json: $(PYTHON_SRCS)
	coua trace $(PYTHON_SRCS) | jq -s '.' > traces.json

doc/source/imported.nt: coua/mappings/junit.ttl junit.xml coua/mappings/cobertura.ttl coverage.xml traces.json spec.ttl
	python -c "import pyoxigraph;  g = pyoxigraph.parse('spec.ttl', mime_type='text/turtle'); pyoxigraph.serialize(g, mime_type='application/n-triples', output='spec.nt')"
	coua check --output doc/source/imported.nt --extra-triples spec.nt

# Generates documentation from data items in doc/source/imported.nt
doc/build/html/index.html: doc/source/imported.nt
	$(MAKE) -C doc clean
	$(MAKE) -C doc html

# Checks data items in doc/source/imported.nt against DO-178C
cert: doc/source/imported.nt

doc: doc/build/html/index.html

check: check-format commit-check mypy

clean:
	rm -f junit.xml coverage.xml traces.json coua.nt spec.nt doc/source/imported.nt
	$(MAKE) -C doc clean

doc/build/html/coua_db: doc

serve: doc/build/html/coua_db
	oxigraph_server serve-read-only --location $<
