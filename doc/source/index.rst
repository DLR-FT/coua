.. Coua documentation master file, created by
   sphinx-quickstart on Mon Jul 22 17:51:14 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Coua's documentation!
================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:


Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. automodule:: coua

Usage
-----

Coua checks your data items against a certification standard.

Currently, only DO-178C is supported and only partially. To be able to check
your data items, Coua requires `subClass` and `subProperty` relations from the
imported triple data to the certification ontology it is performing checks
for.

If your data items already adhere to one of the formats supported by Coua,
these relations are already defined.

Supported data-item formats are:

* JUnit.
* Cobertura.
* Needy.
* Mantra.
* Coua trace format.
* Coua requirements and use-cases.

Before Coua can process the data-item formats, they first need to be be
converted into N-Triples (`.nt`). There are many different tools which can do
this using mapping specifications in RML format (RMLMapper, morph-kgc). Coua
provides a number of these mappings from the data-item formats into N-Triples.

.. code-block:: bash

   python -m morph_kgc mappings.ini

`coua check` then runs the checks provided by an ontology against the data-item data in the N-Triples.

.. code-block: bash

   coua check --mode do178c ingested.nt

Coua contains a Sphinx extension that can be used to render information from the
data-items into a human-readable documentation. The extension contains a set of
pre-defined directives for common documentation for DO-178C. Custom queries can
be defined and run using the `sphinx-sparql` extension or using the Python API
of `coua`.

The extension takes some Sphinx configuration, specifying which triples to consider.

.. code-block:: python

   coua_load = [("imported.nt", "application/n-triples")]


Directives are invoked inside an reStructuredText document like so

.. code-block:: rst

  .. coua:source_code_coverage_matrix::


Adding support for new data formats
-----------------------------------

#. Add a new mapping file to `mappings/` that specifies how to ingest the data.
#. Add a new ontology to `coua/ontologies/` that describes the properties and classes of the ingested data.
#. *(optional)* In this ontology, specify which classes and properties will be used in queries for DO-178C by using `subClass` and `subProperty`.
#. *(optional)* Add custom queries for your ontology to `coua/ontologies/<your-ontology>/select` and `coua/ontologies/<your-ontology>/ask`. They are available as `YourOntology.select()` and as part of `YourOntology.check()` respectively.

Requirements
------------
.. coua:requirements_list::


Source Code Tracability Matrix
------------------------------
.. coua:source_code_tracability_matrix::


Requirements Test Coverage Matrix
---------------------------------
.. coua:requirements_test_coverage_matrix::

Use-Cases Coverage Matrix
-------------------------
.. coua:use_cases_coverage_matrix::
