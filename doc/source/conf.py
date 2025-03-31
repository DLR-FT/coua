# pylint: skip-file

import os
import sys

from typing import List

sys.path.append(os.path.abspath("../.."))

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "Coua"
copyright = "2024, Tim Schubert"
author = "Tim Schubert"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "coua",
    "sphinx.ext.autodoc",
]

templates_path: List[str] = ["_templates"]
exclude_patterns: List[str] = []


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "alabaster"
html_static_path = ["_static"]

# -- Options for SPARQL extension --------------------------------------------

coua_load = [
    ("imported.nq", "application/n-quads"),
]
