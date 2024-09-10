from __future__ import annotations

from typing import TYPE_CHECKING, Type, List, cast

import sphinx_sparql
from coua.ontologies import load_ontologies

from pyoxigraph import Store
from sphinx.domains import Domain
from sphinx.environment import BuildEnvironment
from sphinx.util.docutils import SphinxDirective
from os import path

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

    def run(self) -> List[Node]:
        domain: CouaDomain = cast(CouaDomain, self.env.get_domain("coua"))
        store: Store = domain.store
        solutions = self.ontology.select(store, self.query_path_seqment)

        return [sphinx_sparql.render_table(solutions)]


class CouaCrosstabDirective(SphinxDirective):
    has_content = False
    required_arguments = 0
    ontology: Type[Ontology]
    query_path_seqment: str
    dimension_x: str
    dimension_y: str

    def run(self) -> List[Node]:
        domain: CouaDomain = cast(CouaDomain, self.env.get_domain("coua"))
        store: Store = domain.store
        solutions = self.ontology.select(store, self.query_path_seqment)

        return [
            sphinx_sparql.render_crosstab(solutions, self.dimension_x, self.dimension_y)
        ]


# TODO render as paragraphs instead
class CouaDO178CRequirementsList(CouaTableDirective):
    ontology = DO178C
    query_path_seqment = "requirements_list.rq"


class CouaDO178CTracabilityMatrix(CouaCrosstabDirective):
    ontology = DO178C
    query_path_seqment = "tracability_matrix.rq"
    dimension_x = "Requirement"
    dimension_y = "TestCase"


class CouaDomain(Domain):
    """Coua domain"""

    name = "coua"
    label = "Coua domain"
    data_version = 0
    directives = {
        "requirements_list": CouaDO178CRequirementsList,
        "tracability_matrix": CouaDO178CTracabilityMatrix,
    }

    @property
    def store(self) -> Store:
        return Store.read_only(path.join(self.env.app.outdir, "coua_db"))


def load_store(app: Sphinx, env: BuildEnvironment, docnames: list[str]):
    sparql_store_path = path.join(app.outdir, "coua_db")
    store: Store = Store(path=sparql_store_path)

    for input, mime in app.config["coua_load"]:
        if not path.isabs(input):
            input = path.join(app.srcdir, input)
        store.bulk_load(input, mime)

    load_ontologies(store)

    store.flush()


def setup(app: Sphinx) -> ExtensionMetadata:
    app.add_domain(CouaDomain)
    app.add_config_value("coua_load", default=[], rebuild="html")
    app.connect("env-before-read-docs", load_store)

    return {
        "version": "0.1",
        "parallel_read_safe": True,
    }
