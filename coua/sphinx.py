"""Sphinx module for accessing Coua database"""

from __future__ import annotations

from typing import TYPE_CHECKING, List, cast

import sphinx_sparql

from docutils import nodes
from pyoxigraph import Store, QuerySolutions
from sphinx.domains import Domain
from sphinx.environment import BuildEnvironment
from sphinx.util.docutils import SphinxDirective
from os import path

from coua.ontologies import load_ontologies
from coua.traces import trace_requirements

if TYPE_CHECKING:
    from docutils.nodes import Node
    from sphinx.application import Sphinx
    from sphinx.util.typing import ExtensionMetadata

from coua.ontologies import DO178C, Coua
from coua.ontologies.ontology import Ontology


@trace_requirements("Req60")
class CouaTableDirective(SphinxDirective):
    has_content = False
    required_arguments = 0
    ontology: Ontology
    query_path_segment: str

    def run(self) -> List[Node]:
        domain: CouaDomain = cast(CouaDomain, self.env.get_domain("coua"))
        store: Store = domain.store
        solutions = self.ontology.select(store, self.query_path_segment)

        return [sphinx_sparql.render_table(solutions)]


@trace_requirements("Req61", "Req62")
class CouaCrosstabDirective(SphinxDirective):
    has_content = False
    required_arguments = 0
    ontology: Ontology
    query_path_segment: str
    dimension_x: str
    dimension_y: str

    def run(self) -> List[Node]:
        domain: CouaDomain = cast(CouaDomain, self.env.get_domain("coua"))
        store: Store = domain.store
        solutions = self.ontology.select(store, self.query_path_segment)

        return [
            sphinx_sparql.render_crosstab(solutions, self.dimension_x, self.dimension_y)
        ]


@trace_requirements("Req60")
class CouaDO178CRequirementsSection(SphinxDirective):
    has_content = False
    required_arguments = 0
    ontology = DO178C()

    def run(self) -> List[Node]:
        domain: CouaDomain = cast(CouaDomain, self.env.get_domain("coua"))
        store: Store = domain.store
        solutions = self.ontology.select(store, "requirements_list.rq")

        return [self.render_requirements_paragraphs(solutions)]

    def render_requirements_paragraphs(
        self, solutions: QuerySolutions
    ) -> nodes.section:
        section = nodes.section(ids=["Requirements"])
        section += [nodes.title(text="Requirements")]
        for s in solutions:
            reqid = s["Requirement"].value
            req = nodes.section(ids=[reqid])
            req += [nodes.title(text=reqid)]
            for par in ["Description", "Rationale"]:
                if s[par]:
                    req += [nodes.paragraph(text=s[par].value)]
            if s["Trace"]:
                trace = s["Trace"].value
                references = nodes.paragraph(text="References: ")
                references += [nodes.reference(text=trace, refuri=f"#{trace}")]
                req += [references]
            section += [req]

        return section


@trace_requirements("Req60")
class CouaDO178CRequirementsList(CouaTableDirective):
    ontology = DO178C()
    query_path_segment = "requirements_list.rq"


@trace_requirements("Req61")
class CouaDO178CTracabilityMatrix(CouaCrosstabDirective):
    ontology = DO178C()
    query_path_segment = "tracability_matrix.rq"
    dimension_x = "Requirement"
    dimension_y = "Location"


@trace_requirements("Req62")
class CouaDO178CCoverageMatrix(CouaCrosstabDirective):
    ontology = DO178C()
    query_path_segment = "coverage_matrix.rq"
    dimension_x = "Requirement"
    dimension_y = "TestCase"


@trace_requirements("Req66")
class CouaUseCaseCoverageMatrix(CouaCrosstabDirective):
    ontology = DO178C()
    query_path_segment = "use_case_coverage.rq"
    dimension_x = "Req"
    dimension_y = "UC"


@trace_requirements("Req34")
class CouaCheckTable(CouaTableDirective):
    ontology = Coua()
    query_path_segment = "checks.rq"


@trace_requirements("Req64")
class CouaDomain(Domain):
    """Coua domain"""

    name = "coua"
    label = "Coua domain"
    data_version = 0
    directives = {
        "check_list": CouaCheckTable,
        "requirements_list": CouaDO178CRequirementsList,
        "requirements_section": CouaDO178CRequirementsSection,
        "source_code_tracability_matrix": CouaDO178CTracabilityMatrix,
        "requirements_test_coverage_matrix": CouaDO178CCoverageMatrix,
        "use_cases_coverage_matrix": CouaUseCaseCoverageMatrix,
    }

    @property
    def store(self) -> Store:
        return Store.read_only(path.join(self.env.app.outdir, "coua_db"))


@trace_requirements("Req65")
def load_store(app: Sphinx, env: BuildEnvironment, docnames: list[str]):
    sparql_store_path = path.join(app.outdir, "coua_db")
    store: Store = Store(path=sparql_store_path)

    for input, mime in app.config["coua_load"]:
        if not path.isabs(input):
            input = path.join(app.srcdir, input)
        store.bulk_load(input, mime)

    load_ontologies(store)

    store.flush()


@trace_requirements("Req64")
def setup(app: Sphinx) -> ExtensionMetadata:
    app.add_domain(CouaDomain)
    app.add_config_value("coua_load", default=[], rebuild="html")
    app.connect("env-before-read-docs", load_store)

    return {
        "version": "0.1",
        "parallel_read_safe": True,
    }
