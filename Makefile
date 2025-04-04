.PHONY: all check-formatting commit-check mypy check clean serve

SOURCEDIRS := "coua"
PYTHON_SRCS := $(shell find $(SOURCEDIRS) -name '*.py')
PYTHON_SRCS += $(wildcard tests/*.py)
RDF_SRCS := $(shell find $(SOURCEDIRS) -name '*.ttl')
QUERIES := $(shell find $(SOURCEDIRS) -name '*.rq')
DOC := $(shell find doc -name '*.rst')
DOC += $(shell find doc -name '*.py')
SRCS := $(PYTHON_SRCS)
SRCS += $(RDF_SRCS)
SRCS += $(DOC_SRCS)
SRCS += $(QUERIES)

all: check test cert

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

traces.json: $(SRCS)
	malkoha . > traces.json

spec.nq: spec.ttl
	python -c "import pyoxigraph;  g = pyoxigraph.parse(open('spec.ttl'), format=pyoxigraph.RdfFormat.TURTLE); pyoxigraph.serialize(g, format=pyoxigraph.RdfFormat.N_QUADS, output='spec.nq')"
	
doc/source/imported.nq: spec.nq $(SRCS) junit.xml coverage.xml traces.json
	coua check --output doc/source/imported.nq --extra-triples spec.nq

# Generates documentation from data items in doc/source/imported.nq
doc/build/html/index.html: doc/source/imported.nq $(DOC)
	$(MAKE) -C doc clean
	$(MAKE) -C doc html

doc/build/html/coua_db: doc/build/html/index.html

test: junit.xml

cert: doc/build/html/index.html

check: check-format commit-check mypy pylint cert

clean:
	rm -f junit.xml coverage.xml traces.json spec.nq doc/source/imported.nq
	$(MAKE) -C doc clean

serve: doc/build/html/coua_db
	oxigraph serve-read-only --location $<
