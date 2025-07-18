"""Sphinx module for accessing Coua database"""

from __future__ import annotations

from typing import TYPE_CHECKING, List, cast, Iterator

import sphinx_sparql

from dataclasses import dataclass
from docutils import nodes
from malkoha import trace_requirements
from pyoxigraph import Store, QuerySolutions
from sphinx.domains import Domain
from sphinx.environment import BuildEnvironment
from sphinx.util.docutils import SphinxDirective
from os import path

from coua.ontologies import load_ontologies

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
@dataclass
class Requirement:
    id: str
    description: str
    rationale: str
    level: str | None

    requirement_traces: set[str]
    # TODO make actual link to code in documentation
    source_locations: set[str]
    test_cases: set[str]


@trace_requirements("Req60")
class CouaDO178CRequirementsSection(SphinxDirective):
    has_content = False
    required_arguments = 0
    ontology = DO178C()

    def run(self) -> List[Node]:
        domain: CouaDomain = cast(CouaDomain, self.env.get_domain("coua"))
        store: Store = domain.store
        solutions = self.ontology.select(store, "requirements_list.rq")

        # FIXME: do aggregation in SPARQL
        return [
            self.render_requirements_paragraphs(self.aggregate_requirements(solutions))
        ]

    def aggregate_requirements(
        self, solutions: QuerySolutions
    ) -> Iterator[Requirement]:
        id = None
        description = ""
        rationale = ""
        level = None
        requirement_traces = set()
        source_locations = set()
        test_cases = set()
        for s in solutions:
            if id and s["Requirement"].value != id:
                yield Requirement(
                    id,
                    description,
                    rationale,
                    level,
                    requirement_traces,
                    source_locations,
                    test_cases,
                )
                id = None
                description = ""
                rationale = ""
                level = None
                requirement_traces = set()
                source_locations = set()
                test_cases = set()
            id = s["Requirement"].value
            description = s["Description"].value
            if s["Rationale"]:
                rationale = s["Rationale"].value
            if s["Level"]:
                level = s["Level"].value
            if s["Trace"]:
                requirement_traces.add(s["Trace"].value)
            if s["SourceCode"]:
                source_locations.add(s["SourceCode"].value)
            if s["TestCase"]:
                test_cases.add(s["TestCase"].value)
        if id:
            yield Requirement(
                id,
                description,
                rationale,
                level,
                requirement_traces,
                source_locations,
                test_cases,
            )

    # TODO merge all solutions for a requirement into one section
    def render_requirements_paragraphs(
        self, requirements: Iterator[Requirement]
    ) -> nodes.section:
        section = nodes.section(ids=["Requirements"])
        section += [nodes.title(text="Requirements")]
        for r in requirements:
            id = r.id
            req = nodes.section(ids=[id])
            req += [nodes.title(text=id)]
            for label, content in [
                ("Level", r.level),
                ("Description", r.description),
                ("Rationale", r.rationale),
            ]:
                part = nodes.paragraph()
                t: nodes.Text | nodes.strong
                if content and len(content) > 1:
                    t = nodes.Text(content)
                else:
                    t = nodes.strong(text="Missing")
                part += [nodes.emphasis(text=label), nodes.Text(": "), t]
                req += [part]
            for name, thing in [
                ("Traces", r.requirement_traces),
                ("Source Code", r.source_locations),
                ("Test Cases", r.test_cases),
            ]:
                if thing:
                    req += [ref_thing(thing, name)]
            section += [req]

        return section


@trace_requirements("Req60")
def ref_thing(things: set[str], title: str) -> nodes.paragraph:
    srcs = nodes.paragraph()
    srcs += [nodes.emphasis(text=title), nodes.Text(": ")]
    ts = list(things)
    for source in ts[:-1]:
        srcs += [
            nodes.reference(text=source, refuri=f"#{source}"),
            nodes.Text(", "),
        ]
    if ts:
        s = ts[-1]
        srcs += [nodes.reference(text=s, refuri=f"#{s}")]

    return srcs


@trace_requirements("Req66")
class CouaUseCaseSection(SphinxDirective):
    has_content = False
    required_arguments = 0
    ontology = Coua()

    def run(self) -> List[Node]:
        domain: CouaDomain = cast(CouaDomain, self.env.get_domain("coua"))
        store: Store = domain.store
        section = nodes.section(ids=["Use cases"])
        section += [nodes.title(text="Use cases")]
        ucs = self.ontology.select(store, "use_cases.rq")
        for uc in ucs:
            sub = nodes.section(ids=[str(uc["ID"].value)])
            sub += [nodes.title(text=str(uc["Title"].value))]
            for var in ucs.variables:
                if uc[var]:
                    par = nodes.paragraph()
                    par += [
                        nodes.Text(var.value),
                        nodes.Text(": "),
                        nodes.Text(str(uc[var].value)),
                    ]
                    sub += [par]
            section += [sub]

        return [section]


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


@trace_requirements("Req38")
class CouaNotImplemented(CouaTableDirective):
    ontology = Coua()
    query_path_segment = "not_implemented.rq"


@trace_requirements("Req62")
class CouaDO178CRequirementsTestCoverageMatrix(CouaCrosstabDirective):
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


@trace_requirements("Req34", "Req37", "Req43", "Req63")
class CouaCheckTable(CouaTableDirective):
    ontology = Coua()
    query_path_segment = "checks.rq"


@trace_requirements("Req78", "Req79", "Req35")
class CouaDO178CWithIndependence(CouaTableDirective):
    has_content = False
    required_arguments = 0
    ontology = DO178C()

    def run(self) -> List[Node]:
        domain: CouaDomain = cast(CouaDomain, self.env.get_domain("coua"))
        store: Store = domain.store
        solutions = self.ontology.select(store, "requires_independence.rq")
        p = nodes.paragraph()
        sol = list(solutions)
        if not sol:
            return [p]
        for s in sol[:-1]:
            p += [nodes.Text(s["Objective"]), nodes.Text(", ")]
        s = sol[-1]
        p += [nodes.Text(s["Objective"])]
        disclaimer = nodes.paragraph()
        disclaimer += [
            nodes.Text(
                " This report is machine-generated and is only binding once signed by a human."
            )
        ]

        return [p, disclaimer]


@trace_requirements("Req77")
class CouaDO178CSoftwareLevelDirective(SphinxDirective):
    has_content = False
    required_arguments = 0
    ontology = DO178C()

    def run(self) -> List[Node]:
        domain: CouaDomain = cast(CouaDomain, self.env.get_domain("coua"))
        store: Store = domain.store
        solutions = self.ontology.select(store, "software_levels.rq")

        return [sphinx_sparql.render_table(solutions)]


@trace_requirements("Req64")
class CouaDomain(Domain):
    """Coua domain"""

    name = "coua"
    label = "Coua domain"
    data_version = 0
    directives = {
        "check_list": CouaCheckTable,
        "requires_independence": CouaDO178CWithIndependence,
        "requirements_list": CouaDO178CRequirementsList,
        "requirements": CouaDO178CRequirementsSection,
        "source_code_tracability_matrix": CouaDO178CTracabilityMatrix,
        "requirements_test_coverage_matrix": CouaDO178CRequirementsTestCoverageMatrix,
        "use_cases_coverage_matrix": CouaUseCaseCoverageMatrix,
        "software_level_list": CouaDO178CSoftwareLevelDirective,
        "not_implemented": CouaNotImplemented,
        "use_cases": CouaUseCaseSection,
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
        with open(input) as f:
            store.bulk_load(f, mime)

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
