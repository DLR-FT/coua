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

Before Coua can process the data-items, they first need to be be converted
into N-Triples (`.nt`). There are many different tools which can do this using
mapping specifications in RML format (RMLMapper, morph-kgc). Coua provides a
number of these mappings from the data-item formats in the `mappings` directory
of the source distribution.

Provided mappings for data-item are:

* JUnit
* Cobertura
* Needy
* Mantra
* Coua trace format
* Coua requirements and use-cases

For morph-kgc, first specify your mappings in a file `mappings.ini` and then run
it like so:

.. code-block:: bash

   python -m morph_kgc mappings.ini

The remainder of this section assumes you used morph-kgc to produce the file
`ingested.nt` containing all N-Triples that contain the ingested data.

Coua can run certification checks on this data.

.. code-block:: bash

   coua check --mode do178c ingested.nt

For this to work, your data needs to contain additional N-Triples declaring
which data is to be used as DO-178C data items. For the mapped data-items
listed above, this information already is declared by Coua. To manually add the
items, simply declare `rdfs:subClass` and `rdfs:subProperty` relations from your
classes and properties to the DO-178C ontology of Coua. See `coua/ontologies/junit/junit.ttl`
for an example.

Coua also contains a Sphinx extension that you can use to render information
from the data-items into a human-readable documentation. The extension contains
a set of pre-defined directives for common documentation required by DO-178C.
You need to configure the extension so that it knows where to find the data to render.
Here we use the same N-Triples from `ingested.nt` as before.

.. code-block:: python

   # doc/source/conf.py
   extensions = [ "coua" ]
   coua_load = [("imported.nt", "application/n-triples")]


You can use the directives inside a reStructuredText document like so

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
