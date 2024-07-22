"""
Coua certification utility.

Run coua-conv-* to convert data gathered from a CI run.
Run coua-check-do178c to perform certification checks on the collected data
using the queries defined for the DO178C ontology.
"""

# TODO hide behind feature
from coua.sphinx import setup
from coua.cli import *  # noqa: F403

__all__ = ["setup"]
