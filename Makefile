.PHONY: all check-formatting commit-check mypy check test doc clean cert serve

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

# Data item ingestion from CI artifacts into n-triples.
# Here morph-kgc is used, could also use RMLMapper or any other tool that produces N-Triples.
# Outputs to doc/source/imported.nt
doc/source/imported.nt: mappings.ini mappings/junit.ttl junit.xml mappings/cobertura.ttl coverage.xml
	python -m morph_kgc $<
	
    # Generates documentation from data items in doc/source/imported.nt
doc/build/html/index.html: doc/source/imported.nt
	$(MAKE) -C doc clean
	$(MAKE) -C doc html

# Checks data items in doc/source/imported.nt against DO-178C
cert: doc/source/imported.nt
	coua check --mode do178c $<

doc: doc/build/html/index.html

check: check-format commit-check mypy

clean:
	rm junit.xml coverage.xml
	$(MAKE) -C doc clean

doc/build/html/coua_db: doc

serve: doc/build/html/coua_db
	oxigraph_server serve-read-only --location $<
