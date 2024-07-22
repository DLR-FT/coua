from __future__ import annotations

from typing import TYPE_CHECKING, Type

import sphinx_sparql
from pyoxigraph import Store
from sphinx.domains import Domain
from sphinx.util.docutils import SphinxDirective

if TYPE_CHECKING:
    from docutils.nodes import Node
    from sphinx.application import Sphinx
    from sphinx.util.typing import ExtensionMetadata

from coua.ontologies import DO178C
from coua.ontologies.ontology import Ontology


class CouaTableDirective(SphinxDirective):
    has_content = False
    required_arguments = 0
    ontology: Type[Ontology]
    query_path_seqment: str

    def run(self) -> list(Node):
        store: Store = self.env.get_domain("sparql").store
        solutions = self.module.select(store, self.query_path_seqment)

        return [sphinx_sparql.render_table(self, solutions)]


# TODO render as paragraphs instead
class CouaDO178CRequirementsList(CouaTableDirective):
    module = DO178C
    query_path_seqment = "requirements_list.rq"


class CouaDomain(Domain):
    """Coua domain"""

    name = "coua"
    label = "Coua domain"
    data_version = 0
    directives = {"requirements_list": CouaDO178CRequirementsList}


def setup(app: Sphinx) -> ExtensionMetadata:
    app.add_domain(CouaDomain)

    return {
        "version": "0.1",
        "parallel_read_safe": True,
    }
