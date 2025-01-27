.PHONY: all check-formatting commit-check mypy check test doc clean cert serve

SOURCEDIRS := "coua"
PYTHON_SRCS := $(shell find $(SOURCEDIRS) -name '*.py')
PYTHON_SRCS += $(wildcard tests/*.py)
RDF_SRCS := $(shell find $(SOURCEDIRS) -name '*.ttl')
QUERIES := $(shell find $(SOURCEDIRS) -name '*.rq')
SRCS := $(PYTHON_SRCS)
SRCS += $(RDF_SRCS)
SRCS += $(QUERIES)

all: check test doc cert

check-format:
	nix fmt -- --fail-on-change --no-cache

commit-check:
	cog check

mypy:
	mypy .

pylint:
	pylint .

junit.xml: coverage.xml

coverage.xml: $(SRCS)
	pytest --cov-branch --junit-xml=junit.xml --cov=coua --cov-report term --cov-report xml:coverage.xml

traces.xml: $(SRCS)
	coua trace .

spec.nt: spec.ttl
	python -c "import pyoxigraph;  g = pyoxigraph.parse('spec.ttl', mime_type='text/turtle'); pyoxigraph.serialize(g, mime_type='application/n-triples', output='spec.nt')"
	
doc/source/imported.nt: spec.nt $(SRCS) junit.xml coverage.xml traces.xml
	coua check --output doc/source/imported.nt --extra-triples spec.nt

# Generates documentation from data items in doc/source/imported.nt
doc/build/html/index.html: doc/source/imported.nt
	$(MAKE) -C doc clean
	$(MAKE) -C doc html

doc/build/html/coua_db: doc/build/html/index.html

test: junit.xml

cert: doc/build/html/index.html

check: check-format commit-check mypy pylint cert

clean:
	rm -f junit.xml coverage.xml traces.xml coua.nt spec.nt doc/source/imported.nt
	$(MAKE) -C doc clean

serve: doc/build/html/coua_db
	oxigraph_server serve-read-only --location $<
