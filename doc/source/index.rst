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
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. automodule:: coua

Adding new import commands
==========================

#. Add new CLI command similar to `coua-conv-junit`.

   * Add new entrypoint function to `coua/cli.py`.

   * Add function name to list in `pyproject.toml`.

#. Add mapping file to `coua/mappings/`.

#. Add name of generated TTL file in `doc/source/conf.py`.

Requirements
============
.. coua:requirements_list::


Tracability Matrix
==================
.. coua:tracability_matrix::
