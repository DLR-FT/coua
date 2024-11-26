.PHONY: check-formatting commit-check mypy check test doc clean

check-format:
	nix fmt -- --fail-on-change --no-cache

commit-check:
	nix develop --command cog check

mypy:
	nix develop --command mypy coua

test:
	nix develop --command pytest --cov-branch --junit-xml=junit.xml --cov=coua --cov-report term --cov-report xml:coverage.xml

coverage.xml: test

junit.xml: test

# Data item ingestion from CI artifacts into n-triples.
# Here morph-kgc is used, could also use RMLMapper or any other tool that produces N-Triples.
# Outputs to doc/source/imported.nt
doc/source/imported.nt: mappings/junit.ttl junit.xml mappings/cobertura.ttl coverage.xml mappings.ini
	nix develop --command python -m morph_kgc mappings.ini
	
    # Generates documentation from data items in doc/source/imported.nt
doc/build/html/index.html: doc/source/imported.nt
	$(MAKE) -C doc clean
	$(MAKE) -C doc html

# Checks data items in doc/source/imported.nt against DO-178C
cert-check: doc/source/imported.nt
	nix develop --command coua check --mode do178c $<

doc: doc/build/html/index.html

check: check-format commit-check mypy cert-check

clean:
	rm junit.xml coverage.xml
	$(MAKE) -C doc clean
