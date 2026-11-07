# Mechanical Design Intelligence — Research, Taxonomy, Corpus & Agent Architecture Plan

**Version:** 0.1 · **Date:** 7 November 2026 · **Status:** Execution plan, not a record of completed implementation  
**Companion:** [`01_PROJECT_SPECIFICATION.md`](01_PROJECT_SPECIFICATION.md)

---

## 1. Goal and sequencing

Produce a **credible, rights-aware, agent-native mechanism database** spanning the 18 families identified in the project specification. A working agent should be able to find, compare and justify mechanisms under requirements, independent of AI platform. Start with an initial source reconnaissance already recorded; **systematic per-source audits, bulk data extraction rights checks, technical record creation and implementation remain to be done**.

Recommended order:

1. Deeply survey sources and competing catalogs.
2. Audit each for what can legally be **linked, independently annotated, indexed, imported or hosted**, versus what it teaches us about taxonomy, keywords, presentation or selection logic.
3. Define and test the 18-family taxonomy, subfamilies, facets, identity policy and relationship ontology.
4. Build a genuinely representative, technically reviewed seed corpus **across core families**, not only compliant mechanisms.
5. Build canonical search/index/storage + REST and MCP from the same source of truth.
6. Benchmark with real AI design tasks and independent human review.
7. Grow community, assets and evidence; defer future paid engineering computation to a later strategic phase.

Do not begin by scraping thousands of animations. Quality of engineering choices, licensing and programmatic usability matter first.

---

## 2. Workstream A — Detailed source discovery and competitive audit

### A1. Search strategy

Explore six source classes systematically:

| Class | Example search terms | Intended output |
|---|---|---|
| Classical and kinematics | mechanical movement atlas; linkage repository; kinematic chain database; cam mechanism catalog; gear mechanism animation | Named archetypes, structural dimensions, synonyms |
| Compliant/flexure | compliant mechanism library; topology-optimized compliant design; flexure hinge CAD; constant force compliant; bistable compliant; compliant parallel-guiding | Rich F01 inventory, comparison/limitations |
| Robotic subsystems | underactuated gripper CAD; robotic leg linkage; tendon differential; series elastic actuator; robot joint reducers | Robot-specific examples, composition links |
| Soft/precision/MEMS | soft robotics toolkit files; PneuNet fabrication; continuum manipulator; folded beam MEMS; piezo stage | F13 and F18, fabrication and operating constraints |
| Quantitative engineering datasets | linkage path dataset; force displacement compliant dataset; tested mechanism CAD/FEA; S–N test archive | Candidate validated implementations and evidence |
| Standards and practical design guides | NASA mechanism standard; engineering constraints; joint tolerance design; fabrication guides | Claim/evidence requirements for future expansion |

Supplement with cross-reference mining: extract bibliographies of reputable surveys, research group projects, university course resources, CAD repositories and dataset landing pages. Search patent records as a separate IP diligence track, not as a source of casually reusable designs.

### A2. Priority sites and exact audit agenda

| Priority | Source | Main questions | What to learn / candidate fields |
|---|---|---|---|
| **P0** | [IISc M2D2 Collection](https://mecheng.iisc.ac.in/m2d2/CMcollection/) | How many working pages? What are function labels? Which pages have literature, CAD, FEM, video? What are file rights? | Gripper/clamp/clutch/crimper; DaCM; direction/path/shape change; suspensions; contact-aided; bistability; topology vs implementation |
| **P0** | [IISc Model 16](https://mecheng.iisc.ac.in/m2d2/CMcollection/16.html) | What topology and boundary conditions? Original paper? What is linked CAD format/license? Which simpler alternatives? | Topology-optimized gripper; central input, convergent fingers; **complexity vs benefit** |
| **P0** | [mechanisms.ln.gy](https://mechanisms.ln.gy/) and [taxonomy](https://mechanisms.ln.gy/taxonomy/) | Which of ~24 facets are implemented, searchable, downloadable? Is there an API? Which rights and taxonomy corrections? How strong is function-based search? | Necessary baseline for our facet design and differentiation; aliases, motion input/output, roles |
| **P0** | [Atlas Mechanica](https://atlasmechanica.com/) / [GitHub](https://github.com/atlasmechanica/atlasmechanica) | Actual shipped vs planned features; models, source and solver abstractions; code/content license; programmatic access? | Avoid duplicating an emerging open design atlas; identify actual API/evidence gaps |
| **P0** | [RoboticWorx](https://roboticworx.io/pages/mechanisms) | Which 126 plates? What are strengths/watch-outs? Are AI-generated animations mechanically reliable? Is structured export available? | High-quality interactive presentation, caution on unvalidated visuals |
| **P0** | [BYU dataset 74](https://scholarsarchive.byu.edu/data/74/) | What variables, geometries, dimensional units, sample count, experimental vs simulated? | E2/E3 mechanism evidence, scalable force/displacement and strain schema |
| **P0** | [BYU dataset 107](https://scholarsarchive.byu.edu/data/107/) | What CSV columns, test methods, specimen materials, data conditions? | Folded beam, chevron, variable-stiffness spring evidence; CC BY attribution |
| **P1** | [MIT LINKS](https://decode.mit.edu/projects/links/) / [GitHub](https://github.com/ahnobari/links) | Actual license, dataset representation, topology generation, trajectory labeling, retrieval method | Algorithmic linkage data and instance/pattern identity |
| **P1** | [Cornell KMODDL](https://engineering.library.cornell.edu/kmoddl/) | Public metadata, source dates, embedded media rights, exact linkages | Classical source lineage and historical names |
| **P1** | [507 Movements](https://507movements.com/about.html) | Public-domain original text vs website animation/image rights; how index is organized | Unique named mechanism families and historical motion primitives |
| **P1** | [Soft Robotics Toolkit](https://softroboticstoolkit.com/) | Components, CAD, fabrication recipes, tests, licensing by content | F13 taxonomy, fabrication conditions |
| **P1** | [Mechanical Library](https://mechanical-library.org/) | Mechanism inventory, file formats, printability, source license | Human-friendly visual presentation and 3D examples |
| **P1** | [Open Dynamic Robot Initiative](https://github.com/open-dynamic-robot-initiative/open_robot_actuator_hardware) | Available CAD, exact mechanical modules, file licenses, assembly issues | Real robot mechanical compositions and design constraints |
| **P1** | [Open-Source Leg](https://opensourceleg.org/hardware/) | Mechanical CAD and component provenance; series elasticity, actuators | F04/F09/F11 integrations |
| **P1** | [Babin & Gosselin 2021](https://doi.org/10.1146/annurev-control-061520-010405) | Exhaustive architectural categories; cited mechanisms and design principles | Underactuation, adaptive grippers and robot hand architecture |
| **P1** | [Gripper systematic review 2023](https://www.mdpi.com/2218-6581/12/1/5) | Reproducible architecture/actuation classification | Cross-map F08/F12/F13 |
| **P1** | [Variable Transmissions survey](https://ramagazine.ieee.org/2025/06/24/variable-transmission-mechanisms-for-robotic-applications-a-review-survey/) | Named mechanical architectures and comparison criteria | Dynamic gear ratio, robot actuation terms |
| **P2** | [Compliant gripper review 2025](https://www.sciencedirect.com/science/article/pii/S0094114X24003276) | How 1,009 papers were searched and 239 mapped; underlying data available? | Research keywords, synthesis method dimensions |
| **P2** | [NASA-STD-5017B](https://ntrs.nasa.gov/citations/20220014671) | Requirements and verification practices relevant to mechanism metadata | Future evidence/verification language |
| **P2** | [Recent 2026 research](https://doi.org/10.1371/journal.pone.0340272), [2026 gripper review](https://pmc.ncbi.nlm.nih.gov/articles/PMC13667752/) | New examples not covered by older catalogs | Modern F01/F08/F09 coverage |

**Auditing a site does not mean ingesting its content.** For every source above, produce a `source_audit.md` and rights decision, then a small hand-curated candidate list.

### A3. Standard audit template (fill for each source)

```yaml
source_id: s01_iisc_m2d2
url: https://mecheng.iisc.ac.in/m2d2/CMcollection/
owner: Indian Institute of Science - M2D2 Laboratory
kind: [visual_catalog, research_collection, cad_links]
last_checked: 2026-11-07
coverage:
  categories: []
  approximate_records: null
  robotic_relevance: null
  uniqueness: null
technical_assets:
  text: unknown
  images: unknown
  animation: unknown
  parametric_cad: unknown
  mesh: unknown
  fea: unknown
  measurements: unknown
api:
  supported: unknown
  evidence_url: null
rights:
  website_terms: unknown
  metadata_reuse: review_required
  text_reuse: review_required
  images_reuse: review_required
  cad_reuse: review_required
  measured_data_reuse: review_required
  patentee_check: review_required
proposed_use:
  learn_from: [function_taxonomy, topology_distinction]
  link_to: [individual_model_pages]
  independently_author: [summaries, relationship_claims]
  import_after_approval: []
quality:
  provenance_completeness: unknown
  dimensions_units: unknown
  simulation_vs_test_clarity: unknown
  accuracy_issues: []
open_questions: []
reviewer: null
review_status: needs_deep_audit
```

### A4. Weighted audit rubric

Score each source 0–5 on **robotics/mechanical breadth (15%)**, **unique/representative design value (15%)**, **structured metadata (15%)**, **engineering evidence (20%)**, **legal reuse clarity (15%)**, **programmatic access (10%)**, and **current maintenance (10%)**. Report missing data separately; do not convert an unclear license into a numeric “safe to import” score. An otherwise useful source can be rejected from hosting if rights are unverified.

### A5. Source findings deliverables

- `research/source_registry.yaml`: all source URLs, owners and status.
- `research/source_audits/<id>.md`: rights, fields, strengths and lessons learned.
- `research/coverage_matrix.md`: family x source x subfamily.
- `research/keyword_dictionary.yaml`: canonical labels, aliases, synonyms, competitor search terms, multilingual optional.
- `research/asset_rights.md`: per-source/per-asset permissions and gaps.
- `research/competitor_matrix.md`: query types, results, API/MCP, explanations, provenance, CAD, evidence, human interaction.
- `research/candidate_mechanisms.yaml`: candidate entries with `not_ingested`/`approved` status.

---

## 3. Workstream B — Define and validate the ontology

### B1. Freeze a provisional 18-family browse structure

Family IDs: `F01 compliant`, `F02 rigid linkages`, `F03 joints/guides`, `F04 gears/reducers`, `F05 tendon/cable/belt`, `F06 motion conversion`, `F07 cams/indexing`, `F08 underactuation/differentials`, `F09 elasticity/damping`, `F10 clutches/brakes/locks`, `F11 serial/parallel kinematics`, `F12 gripping/end-effectors`, `F13 soft/continuum`, `F14 locomotion`, `F15 deployable/reconfigurable`, `F16 bio-inspired/metamaterials`, `F17 passive alignment`, `F18 micro/precision`.

Use the detailed named subfamilies in the specification as the initial ontology seed. Each will receive `id`, `parent`, `definition`, `inclusion_rules`, `exclusion_rules`, `aliases`, and `examples`.

### B2. Resolve naming and overlap

- Every canonical mechanism pattern gets one stable `mech.*` identifier, even if it appears in 3 families.
- Label archetype/variant/implementation/assembly/principle explicitly.
- Distinguish **input motion** vs **actuation source** (cam is a transmission geometry, motor is an energy source).
- Separate **structural design** (e.g. tendon linkage) from **task role** (e.g. underactuated gripper).
- Distinguish **claimed self-locking** from measured non-backdrivability under specific loads.
- Formalize “no backlash” for elastic motion vs joint backlash and clarify hysteresis and flexure drift.
- Treat manufactured geometry, material and test conditions as implementation-level fields.
- Preserve `unknown`, `not_applicable`, and `not_verified` as distinct states.

### B3. Canonical relation definitions and checks

Implement relation predicates from specification, with guards:

- `is_variant_of` cannot form a cycle.
- `alternative_to` requires shared functional context and explicit tradeoffs; not automatically interchangeable.
- `validated_by` must target a real evidence record, not an opinion.
- `unsuitable_when` must identify the condition and source or review basis.
- `composed_of` links assemblies to parts/components, with cardinality or optionality when known.
- `derived_from` documents lineage, not legal ownership.

**Target:** at least 20 manually reviewed cross-family relationships by the first corpus milestone; target 2 useful relations per reviewed entry as coverage grows.

### B4. Taxonomy quality test

Ask two mechanical reviewers to independently classify 30 entries spanning borderline cases (Fin Ray, flexure gripper, planetary reducer, remote-center compliance, series elastic joint). Compare agreement, adjudicate ambiguities, revise definitions and keep a decision log.

**Exit gate:** all 18 families have definitions, subfamilies, non-overlapping IDs, examples, cross-family policy and documented facets. No unresolved conceptual blocker to corpus authoring.

---

## 4. Workstream C — Build the first structured corpus

### C1. Target and balance

**First useful milestone:** 100–150 reviewed mechanism pattern records across **all 18 families**, with at least 4 representatives per family and deeper coverage of widely used core families. A practical distribution for the *first 130* records:

| Family | Initial target |
|---|---:|
| F01 Compliant mechanisms | 15 |
| F02 Rigid linkages | 12 |
| F03 Joints & guides | 10 |
| F04 Gears & reducers | 10 |
| F05 Cables/tendons/belts | 8 |
| F06 Motion converters | 8 |
| F07 Cams/indexing | 6 |
| F08 Underactuation/differentials | 8 |
| F09 Springs/damping | 7 |
| F10 Clutches/brakes/locks | 6 |
| F11 Kinematic architectures | 7 |
| F12 End-effectors | 8 |
| F13 Soft/continuum | 5 |
| F14 Locomotion | 5 |
| F15 Deployable/reconfigurable | 5 |
| F16 Bio-inspired/metamaterials | 4 |
| F17 Passive alignment | 4 |
| F18 Precision/MEMS | 4 |
| **Total** | **132** |

This is a **coverage allocation**, not fabricated entries. Rebalance when actual source availability is known. The initial 18-family catalog can launch with fewer entries only if coverage gaps are clearly marked and results not overstated.

### C2. Mandatory fields for a reviewed V1 entry

- Stable ID, canonical name and aliases.
- Entity type and family/subfamily/facets.
- Mechanical function(s) and input/output mechanical behavior.
- Brief independently authored explanation of working principle.
- Typical applications and explicit selection criteria.
- Known limitations, stress/fatigue/manufacturing considerations or `not_yet_evaluated`.
- Two comparison relationships where sensible (or `no_validated_alternative_recorded`).
- At least one credible primary/technical source URL; multiple when source claims differ.
- Evidence level and last verification date.
- Source/asset rights status; image/CAD as external links unless approved.
- Unknowns and prerequisites for engineering assessment.

**Do not require fabricated numeric stiffness, angular travel or fatigue life.** Quantitative claims are optional until independently sourced.

### C3. Data entry workflow

1. Source candidate identified (candidate list).
2. De-duplicate against canonical patterns and aliases.
3. Create a draft record with link-only external assets.
4. Write mechanism summary and extract supported classification facets.
5. Attach explicit source references to claims and relationship assertions.
6. Run automated schema, link and naming checks.
7. Mechanical reviewer validates function and critical limitations.
8. Mark `reviewed`; publish versioned record; keep change history.
9. Accept feedback/errata via contributions.

### C4. Rights-safe illustration plan

- **MVP:** neutral original schematics created from first-principles geometry, links to source animations and creator CAD.
- **Later:** use properly licensed CAD/3D only, keeping attribution and original license; generate own parametric reconstructions only after IP checks.
- Avoid reusing AI-generated animations that have no accompanying mechanical validation as if they were verified kinematics.

### C5. Initial quality metrics

- 100% valid schema and resolvable stable IDs.
- At least 90% reviewed entries with one strong cited source.
- At least 80% with documented constraints or explicit evidence gaps.
- All entries have type, functions, input/output behavior or a reason it does not apply.
- At least 75% with meaningful comparison/related links.
- Zero hosted third-party assets with unknown rights.
- Family coverage dashboard distinguishes reviewed patterns vs variants vs implementations.

---

## 5. Workstream D — Architecture & agent-queryability

### D1. Proposed implementation stack

| Concern | MVP choice | Why |
|---|---|---|
| Canonical editing | YAML/JSON files in Git | Reviewable and versionable |
| Data contract | JSON Schema, semver | Prevent field drift |
| Data import | Python validation / normalized ETL | Source-specific parsers and tests |
| Storage/search | PostgreSQL, text search, JSONB; optional pgvector | Typed constraints, aliases and basic relationships without premature graph DB |
| Backend | FastAPI or equivalent | OpenAPI, typed validation and portability |
| Agent access | MCP server calling the same query/compare services | No platform-specific data silos |
| Web frontend | Simple catalog/compare UI | Human accessibility and QA |
| Assets | Link-first; optional licensed S3-compatible object storage | Clear rights and predictable costs |
| Deployment | Managed DB + small service | Simple operation and logging |

The precise language/framework is an implementation preference, not a foundational requirement. The mechanism data contract is the durable asset.

### D2. Search implementation passes

**Pass 1:** deterministic facets + keyword BM25/FTS + alias normalization + basic relationships; build an independently judged query set.

**Pass 2:** optional embedding retrieval for descriptions and natural-language intent expansion; re-rank by documented function/constraints. Evaluate against pass 1 before enabling.

**Pass 3:** conditional mechanism recommendation and structured comparisons; explain rejected candidates and exact unmet or unknown constraints.

**Pass 4:** richer graph reasoning, quantitative ranges and context-aware ranking only when measured data is available.

### D3. REST and MCP work items

- Implement `GET /v1/families`, `GET /v1/mechanisms/{id}`, `POST /v1/search`, `POST /v1/compare`, and alternatives/constraints/sources endpoints.
- MCP tools: `search_mechanisms`, `get_mechanism`, `compare_mechanisms`, `find_alternatives`, `get_design_constraints`, `get_mechanism_sources`, `list_mechanism_taxonomy`.
- Return machine-readable `reason_codes`, source refs, evidence tier, exclusions, unknown parameters, dataset version and links.
- Supply minimal usage examples for ChatGPT-compatible MCP clients, Claude-compatible MCP clients and a generic HTTP agent, **without depending on one platform**.
- Explicitly document inputs, JSON examples, quotas, tool descriptions and error handling.

### D4. Must-pass tests

- Function query retrieves expected candidates across family boundaries.
- Hard numerical constraint filters do not treat `unknown` as `pass`.
- Compare result identifies a truly different family where appropriate.
- Input/output motion queries do not mix energy source with transformation mechanism.
- Missing data is never filled with a plausible number by generative text.
- Source links resolve and evidence claims are traceable.
- Same query and dataset version returns deterministic core ranking when user weights are fixed.
- MCP and REST call the same core engine and return equivalent data.
- Schema migration keeps stable IDs usable.

---

## 6. Workstream E — Evaluate usefulness for humans and agents

### E1. Create a 30–50 query benchmark

Include 5–8 queries in each group:

1. **Function discovery:** “convert continuous rotation to interrupted motion”, “grip without a dedicated actuator per finger”.
2. **Constraint-heavy design:** “low backlash, small angular travel, monolithic, manufactured from a sheet”.
3. **Alternative finding:** “replace a leadscrew with a compact transmission”, “bearing alternative for precision pivot”.
4. **Cross-family ambiguity:** compliant gripper vs underactuated rigid finger vs soft gripper.
5. **Evidence questions:** “what force vs displacement data exists?”, “which recommendation is experimentally validated?”.
6. **Negative/uncertain:** contradictory requirements, inappropriate loads, missing environment, unavailable data.
7. **Robotic application:** leg drive, docking compliance, micro-positioning, tendon transmission.

Every query receives: intent, required facets, acceptable gold candidates, known misleading candidates, hard exclusions, expected source evidence and reviewer notes.

### E2. Comparison experiments

For each benchmark question run:

- **Baseline A:** agent with no external database.
- **Baseline B:** agent with a general internet/document search (if available).
- **Treatment:** the same agent with MDI MCP/search access.

Evaluate **selection correctness, constraint violations, alternative diversity, citation quality, completeness of uncertainty, time/latency and tool use**. A blinded mechanical engineer reviews candidate shortlists. A successful integration requires measurable improvement without excessive calls or misleading confidence.

### E3. Three tangible demonstration workflows

1. **Low-backlash precision hinge:** compare cross-axis pivot, cartwheel flexure, notch flexure and conventional bearing. Output a reasoned selection, not just a model.
2. **Adaptive low-cost gripper:** compare compliant jaw, underactuated linkage and soft gripper, with stated missing force/geometry/material inputs.
3. **Compact robot leg motion:** compare linkage architectures and actuator transmission choices, and identify design tradeoffs.

The later CAD step may use FreeCAD merely as an example to demonstrate retrieval → architecture choice → geometry design; the product itself remains independent.

### E4. Exit criteria

- Reviewers judge MDI-assisted shortlists more suitable or better evidenced than no-database baselines on a predefined majority of tests (threshold set before running tests).
- Zero unflagged violations of explicit, testable hard requirements in a curated safety/constraint benchmark.
- Improvements not explained solely by verbose answers or source-count inflation.
- Real agents consistently call the tools when needed; log and analyze missed tool opportunities.

If benefit is not demonstrated, revise schema, search behavior or integration before scaling to thousands of entries.

---

## 7. Workstream F — Community, rights, scaling and partnerships

- Publish contributing rules, schema docs, review standards and a source-rights policy.
- Add `suggest-mechanism`, `report-error`, `add-source`, `propose-relation` issue templates.
- Build a public coverage dashboard and make unreviewed status visible.
- Introduce source partnerships to host licensed CAD/FEA and data (IISc M2D2, BYU researchers, open robotics projects are initial outreach candidates—not established partners).
- Add systematic import pipelines only after rights and accuracy checks.
- Track changes in upstream links, licenses, papers and versions.
- Explore upstream contributions rather than assuming every external dataset must be mirrored.
- Keep user private design queries private by default; publish clear telemetry behavior.

---

## 8. Backlog: first GitHub epics and issues

### Epic 1 — Source research (P0)

- [ ] Create source registry for S01–S25, with owners and URLs.
- [ ] Audit IISc M2D2 collection and specifically Model 16; map all functional categories and CAD/FEA links.
- [ ] Audit mechanisms.ln.gy taxonomy, dataset counts, source attribution and actual API/exports.
- [ ] Audit Atlas Mechanica source/model architecture, implemented functions and roadmap.
- [ ] Audit MIT LINKS code/data/rights, including what a distinct mechanism record means.
- [ ] Audit BYU CC BY 4.0 datasets and map at least one quantitative curve to a candidate implementation.
- [ ] Audit Soft Robotics Toolkit, RoboticWorx, Cornell KMODDL and 507 Movements.
- [ ] Compile literature and design-specific keyword dictionary.
- [ ] Publish competitor/source gap matrix and legal/rights triage.

### Epic 2 — Ontology and schema (P0)

- [ ] Define 18 families and 1–3-level subfamilies with canonical IDs.
- [ ] Define entity levels pattern/variant/implementation/assembly/principle.
- [ ] Define facets, unit conventions, unknown/not-applicable values.
- [ ] Define 15–20 relationship predicates and constraints.
- [ ] Create source, asset and claim evidence schemas.
- [ ] Publish 30 borderline classification examples and reviewer policy.
- [ ] Unit-test schema and relationship cycles.

### Epic 3 — Seed corpus (P0)

- [ ] Draft and review 20 cross-family pilot records.
- [ ] Attach citations, aliases, functions, motion and limitations to pilots.
- [ ] Annotate first 20+ explicit cross-family comparison relationships.
- [ ] Expand to 50 reviewed records and validate search coverage.
- [ ] Expand to ~132 reviewed records using the balanced family allocation.
- [ ] Add rights-cleared visuals or source links for representative entries.
- [ ] Run independent engineering QA and publish completeness dashboard.

### Epic 4 — Backend and MCP (P0)

- [ ] Create Git-based canonical data and CI validation.
- [ ] Implement normalized DB import + search index.
- [ ] Implement REST search, mechanism detail, alternatives and compare.
- [ ] Implement typed MCP tools using shared service logic.
- [ ] Implement explainable ranking and fail-closed handling of hard constraints.
- [ ] Publish OpenAPI, sample agent calls and a minimal public UI.

### Epic 5 — Evidence and evaluation (P1)

- [ ] Create 30–50 benchmark queries with independently accepted answers.
- [ ] Evaluate lexical + facet retrieval before embedding retrieval.
- [ ] Run with/without MDI agent experiments with the same model.
- [ ] Human engineer review and error analysis.
- [ ] Produce three end-to-end demonstrations with technical caveats.
- [ ] Publish quantified before/after report; revise based on failed examples.

### Epic 6 — Scale and later modules (P2, not yet designed)

- [ ] Add community contributions and governance.
- [ ] Seek licensed geometry and experiment imports.
- [ ] Expand family depth and evidence coverage.
- [ ] Validate demand for engineering constraint calculations and paid APIs.
- [ ] Scope component compatibility, failure corpus and manufacturing intelligence.
- [ ] Decide whether solver integrations/optimization justify implementation.

---

## 9. Sequencing, milestones and deliverables

These are **dependency-based milestones, not ungrounded development-time estimates**.

| Milestone | Required deliverable | Exit criteria |
|---|---|---|
| M0: Source intelligence | Source audits + competitor matrix + licensing triage | Priority sources understood well enough to avoid obvious rights/feature mistakes |
| M1: Ontology | 18-family hierarchy, facets, relations, schema v0.1 | Borderline examples classify consistently; stable IDs defined |
| M2: Corpus pilot | 20 reviewed records across multiple families | Searchable, cited, constraints and alternatives present |
| M3: Cross-family seed | 100–150 reviewed records; initial target 132 | Broad family coverage, QA and rights checks passed |
| M4: Agent MVP | REST + MCP + website | Real tools can find/compare/retrieve and expose sources/unknowns |
| M5: Evidence of utility | Benchmarks and comparative agent trials | Improvement vs baseline demonstrated or failure diagnosis documented |
| M6: Growth | Community process, permissible source partnerships, deeper corpus | Sustainable new reviewed contribution path |
| M7: Commercial extension | Validated paid use case and implementation decision | Buyers and quantifiable value identified; no premature general-purpose solver promise |

### Proposed go/no-go reviews

**After M0:** Is there a meaningful gap versus mechanisms.ln.gy, Atlas Mechanica, RoboticWorx and source tool APIs? If not, narrow to explicit engineering decision evidence.

**After M3/M4:** Do design agents reliably use the database? If not, fix tool schema/integration rather than increasing raw catalog size.

**After M5:** Do recommendations improve technically? If not, avoid monetizing an unproven selection layer.

---

## 10. Risks and research questions to keep visible

- **Is “largest database” coherent?** Count unique mechanism patterns separately from randomly generated instances, animations and actual validated designs. Publish definitions publicly.
- **Which existing corpus can be reused?** Many assets are copyrighted, even when published or downloadable. Never equate public visibility to licensing permission.
- **How to prevent hallucinated specifications?** Engineering performance needs context, units, conditions and evidence; missing values should remain unknown.
- **How to deal with very broad families?** Browse taxonomy plus orthogonal facets and entity-type flags, not a single mutually exclusive tree.
- **Does cross-family “alternative” create false equivalence?** Always contextualize and record constraints.
- **Do search platforms already solve the need?** Check the current product, not just a landing page; the competition is changing rapidly.
- **Would free database usage lead to paid demand?** Validate later through real workflow value and computation-heavy checks, not assumed willingness to pay.
- **What about patents?** Published mechanisms can still be patented; patent review should accompany claims about commercial manufacturability.
- **How will the product maintain accuracy?** Engineering-review workflow, provenance, periodic audit, corrections and versioning.
- **How to build a community without becoming a link farm?** Require structured functions, alternatives, constraints and source evidence with contributions.

---

## 11. First next actions (in order)

1. **Run the detailed P0 source audit** on IISc M2D2 (especially #16), mechanisms.ln.gy, Atlas Mechanica, RoboticWorx and two BYU datasets; produce a matrix of names/functions/keywords/assets/rights/API availability.
2. **Compile the canonical ontology draft** for all 18 families, listing each subfamily with definitions and classification rules; connect 20 cross-family mechanism alternatives.
3. **Create a 20-entry multi-family data pilot** with source-backed description, function, input/output, alternatives and limitations. Include at least: flexural pivot, compliant gripper, rigid four-bar, linear guide, planetary reducer, cycloidal reducer, timing belt, tendon differential, lead screw, Geneva, latch, series elastic joint, Delta architecture, soft bender, rocker–bogie, scissor deployable, Fin Ray, RCC device and precision folded-beam guide.
4. **Build a local query prototype** over those 20 records, without an LLM ranking dependency. Test ambiguous and constraint-rich questions.
5. **Expose REST + MCP** and run a small head-to-head test with AI agents. Use the outcomes to prioritize additional corpus content and decide on engineering evidence depth.

---

## 12. Source reference index

For complete source notes, links, licensing caveats and specific findings, see **Section 9 and Section 16** of [`01_PROJECT_SPECIFICATION.md`](01_PROJECT_SPECIFICATION.md). Especially:

- IISc M2D2 home — https://mecheng.iisc.ac.in/m2d2/CMcollection/
- IISc M2D2 Model 16 — https://mecheng.iisc.ac.in/m2d2/CMcollection/16.html
- IISc M2D2 About — https://mecheng.iisc.ac.in/m2d2/CMcollection/about.html
- Mechanisms index & taxonomy — https://mechanisms.ln.gy/ ; https://mechanisms.ln.gy/taxonomy/
- Atlas Mechanica — https://atlasmechanica.com/ ; https://github.com/atlasmechanica/atlasmechanica
- RoboticWorx — https://roboticworx.io/pages/mechanisms
- MIT LINKS — https://decode.mit.edu/projects/links/
- BYU compliant scaling data — https://scholarsarchive.byu.edu/data/74/
- BYU force/displacement data — https://scholarsarchive.byu.edu/data/107/
- Soft Robotics Toolkit — https://softroboticstoolkit.com/
- Cornell KMODDL — https://engineering.library.cornell.edu/kmoddl/
- 507 Mechanical Movements — https://507movements.com/about.html
- Mechanical Library — https://mechanical-library.org/
- Open Dynamic Robot Initiative — https://github.com/open-dynamic-robot-initiative/open_robot_actuator_hardware
- Open-Source Leg — https://opensourceleg.org/hardware/

---

*This plan deliberately distinguishes initial source reconnaissance (completed) from exhaustive audit, licensing evaluation, dataset extraction, implementation and validation (future work).*
