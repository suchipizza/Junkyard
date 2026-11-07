# Mechanical Design Intelligence
## Agent-Native Mechanism Knowledge Base — Project Specification & Long-Term Vision

**Version:** 0.1 · **Date:** 7 November 2026 · **Status:** Founding concept / research and architecture plan  
**Working name:** Mechanical Design Intelligence (MDI); brand and repository name not decided.  
**Related document:** [`02_RESEARCH_AND_BUILD_PLAN.md`](02_RESEARCH_AND_BUILD_PLAN.md)

---

## 1. Executive summary

Build an **independent, open, agent-queryable database of mechanical mechanisms and mechanical design solutions**, usable by any AI platform, hardware-design agent, CAD assistant, engineering developer, roboticist, or human engineer.

The first product is **a broad mechanism knowledge base**, *not* an AI CAD platform, a robot-design service, a simulation solver, or an electronics tool. Its primary advantage is to help agents and humans find and compare mechanisms by **what physical task they accomplish**, not only by names, diagrams, or keywords.

The founding thesis: as AI-powered hardware creation becomes mainstream, agents will need dependable external engineering knowledge to select physical architectures, identify alternatives, reason about constraints, and link to source CAD and technical evidence. The product becomes a **cross-platform mechanical-design intelligence layer** delivered through a website, documented JSON data, a REST API, and an MCP server. No exclusivity to ChatGPT, Claude, FreeCAD, Blender, Schematik, Flux, or any particular environment.

**Initial scope:** an inventory and searchable corpus spanning 18 mechanical mechanism families, with compliant mechanisms as an important but not exclusive branch. **Later scope:** component compatibility, materials, constraints, engineering calculations, failure evidence, manufacturing, structural/dynamic simulation and optimization. These later modules are documented but **not yet specified for implementation**.

**Core product promise:** *Describe the motion or mechanical behavior you need; retrieve traceable candidate mechanisms, plausible alternatives, applicability conditions, limitations and supporting references in a format an agent can act on.*

### What makes this different

1. **Function-first:** natural language and structured queries beginning with an engineering need (e.g. “backlash-free limited-angle pivot with no assembly”).
2. **Decision-oriented:** suitability, alternative mechanisms, constraints, failure modes, missing input conditions; not just an illustration.
3. **Cross-family:** compares rigid linkages, flexures, soft mechanisms, gears, tendon mechanisms, etc., when their functions overlap.
4. **Evidence-aware:** citations on each engineering assertion; separates general knowledge from tested performance, numerical simulation and speculative suitability.
5. **Interoperable:** one independent canonical dataset behind human UI, JSON export, REST/OpenAPI and MCP.
6. **Extensible:** future integrations can attach geometry, experiments, material data and computational checks without redesigning the corpus.

**Important competitive reality:** [mechanisms.ln.gy](https://mechanisms.ln.gy/about/) reports **4,060** indexed mechanisms and already has an extensive faceted taxonomy; [MIT LINKS](https://decode.mit.edu/projects/links/) describes **100 million** generated planar linkages. “Largest” must be qualified. The long-term ambition is the **most extensive *agent-usable, evidence-linked, cross-family* mechanical decision corpus**, not an immediate claim to most raw geometric instances. Source definitions and figures should be periodically rechecked.

---

## 2. Why this should exist

### 2.1 Emerging workflow

A person describes a hardware idea to an AI assistant → the assistant consults the mechanism database and engineering references → the assistant creates parametric geometry through a supported CAD integration → electronics and control may be designed with separate tools → the design is checked and revised → parts and boards are manufactured and physically tested.

**Illustrative workflow:** “Design a printable, low-backlash gripper for fragile irregular objects.” A cross-platform AI agent queries the knowledge base for candidate compliant jaws, four-bar fingers, underactuated tendon systems and soft grippers; compares the need for fabrication, actuation, stroke and forces; then starts CAD generation. The MDI library supplies retrieval and decisions, **not a guarantee of safe or successful fabricated hardware**.

### 2.2 User groups

| Group | Job-to-be-done | Initial value |
|---|---|---|
| AI hardware agents and platform builders | Find relevant mechanical solutions during generation | Structured tools, stable IDs, machine-readable constraints and alternatives |
| Robotics developers | Compare architecture choices for grippers, joints, transmissions and locomotion | Cross-family functional search, references, CAD links |
| Mechanical engineers | Discover known mechanism variants and design tradeoffs faster | Technical explanations, provenance, classification |
| CAD/copilot tool creators | Add trustworthy engineering knowledge without building it in-house | Independent REST/MCP and data exports |
| Researchers, teachers, students | Explore solutions and follow primary literature | Visual mechanisms, lineage, source links, taxonomies |
| Makers and hardware founders | Select concepts before prototyping | Approachable functional queries and honest unknowns |

### 2.3 Explicit non-goals for V1

- No general-purpose mechanical engineering chatbot that invents unreferenced advice.
- No claim to replace professional mechanical analysis, engineering judgment or testing.
- No arbitrary topology generation, FEA, fatigue prediction, modal analysis or certification in the first release.
- No electronics, firmware or PCB authoring; remain platform-agnostic.
- No full rehosting of third-party CAD/animations without verified rights.
- No “AI ranking” that quietly overrides user constraints or hides uncertainty.

---

## 3. Product surfaces

**A. Public mechanism explorer:** visual catalog, taxonomy tree, functional search, comparison pages, relationship navigation, direct links to primary sources and permitted CAD files. Visualizations have provenance and do not imply validated physics.

**B. Open structured corpus:** versioned mechanism records with stable identifiers, human-readable YAML/JSON, schema validation, evidence fields and contribution guidelines.

**C. Agent interfaces:** REST/OpenAPI and MCP capabilities built on one search/decision engine. Tools return structured data, alternatives, exclusions, confidence and missing requirements; integrations should work with *any* compliant client.

**D. Optional integration examples:** prompts, API snippets and workflows connecting to CAD/robotics tooling. A FreeCAD demonstration is a convenient first reference, not a dependency or exclusive integration.

**E. Community contribution layer:** propose a mechanism, source, correction, cross-family relationship, tested result, CAD link or failure mode through a reviewed contribution process.

### Example user questions

- Find a mechanism that converts rotary actuation into near-linear jaw closure with a compact footprint.
- What can replace a conventional bearing when backlash is unacceptable and motion is limited?
- Compare a flexural parallelogram, linear bearing and guide linkage for precision translation.
- Which low-part-count mechanisms distribute one actuator input among three contact points?
- Which mechanisms provide an over-center lock or discrete bistable positions?
- Which walking linkages provide a roughly level foot trajectory?
- What plausible alternatives exist to a worm gearbox for reduction and holding?
- Which mechanisms are topology-optimized and what evidence demonstrates their benefit over simpler designs?

---

## 4. Taxonomy: 18 families, subfamilies and example members

**Taxonomy principle:** the family tree is for discoverability, **not** an exclusive scientific classification. Every entry also receives independent facets for function, input/output motion, topology, compliance, actuation, manufacturing and evidence. A gripper can be a compliant, underactuated, linkage-based and soft mechanism at once; cross-cutting facets prevent forced duplication.

### F01 — Compliant mechanisms & flexures

**Subfamilies:** concentrated-compliance flexure joints; distributed-compliance linkages; flexural pivots and rotary stages; flexural linear guides and suspensions; displacement/force amplifiers; path and direction changers; compliant grippers, clamps and crimpers; bistable/multistable and snap-through; contact-aided compliant mechanisms; constant-force/negative-stiffness mechanisms; compliant transmissions; topology-optimized compliant architectures.

**Examples:** notch flexure, cross-axis flexural pivot, cartwheel hinge, leaf-spring parallelogram, folded-beam suspension, compliant four-bar, compliant gripper, compliant displacement amplifier, bistable beam, compliant clutch.

**Cross-family links:** F03 (replaces revolute/prismatic joints), F02 (compliant analogue of linkages), F09 (elasticity), F12 (gripping), F15 (deployable and multistable structures), F18 (precision/MEMS).

### F02 — Rigid-body linkages

**Subfamilies:** four-bar chains; five- and six-bar chains; slider-cranks; straight-line and path-generation linkages; pantographs and motion amplifiers; toggle/wedge/scissor linkages; spatial and overconstrained linkages; leg and gait linkages; coupler-curve mechanisms.

**Examples:** Grashof four-bar, Watt, Stephenson, Peaucellier–Lipkin, Chebyshev, Hoeken, Sarrus, Bennett, pantograph, Klann, Jansen.

**Cross-family links:** F06 (rotation/translation conversion), F11 (closed-loop robot architecture), F14 (walking), F01 (compliant analogues), F15 (scissors).

### F03 — Joints, bearings, pivots & linear guides

**Subfamilies:** revolute; prismatic; spherical/universal; cylindrical and helical; planar; bearing arrangements; preloaded guides; remote-center joints; flexible and misalignment-compensating couplings; flexural joint alternatives.

**Examples:** pin joint, crossed-roller slide, ball-joint, universal joint, Oldham coupling, linear guide, cross-axis flexure pivot.

**Cross-family links:** F01 (flexure alternatives), F11 (kinematic chains), F17 (alignment), F18 (precision).

### F04 — Gears, reducers & geared differentials

**Subfamilies:** spur/helical/herringbone; bevel and hypoid; worm and screw gear; planetary/epicyclic; cycloidal; strain-wave/harmonic; non-circular gears; gear differentials; variable-ratio gear trains.

**Examples:** planetary reducer, cycloidal reducer, strain-wave drive, worm wheel, non-circular gear pair.

**Cross-family links:** F05 (alternative power transmission), F08 (differential/adaptive allocation), F10 (self-lock/holding), F14 (drivetrains).

### F05 — Tendon, cable, belt & chain drives

**Subfamilies:** timing-belt and V-belt trains; chain and sprocket; capstan; Bowden-cable transmission; tendon routing; cable differentials; pulley block and tackle; cable-driven parallel actuation; flexible shaft drives.

**Examples:** antagonistic tendons, remote tendon drive, cable differential, timing belt stage, capstan reduction.

**Cross-family links:** F08 (underactuation), F12 (robotic hands), F13 (continuum), F04 (transmission alternatives).

### F06 — Motion converters: rotary ↔ linear and other transformations

**Subfamilies:** screw/nut (lead, ball, roller); rack-and-pinion; slider-crank; Scotch yoke; cam-based motion conversion; wedge and toggle converters; eccentric; rotary-to-oscillatory; reciprocating-to-rotary.

**Examples:** ball screw, rack-and-pinion, slider-crank, Scotch yoke, eccentric follower.

**Cross-family links:** F02 (linkages), F07 (cams), F04 (gearing), F01 (compliant displacement amplifiers).

### F07 — Cams, indexing & intermittent motion

**Subfamilies:** radial and conjugate cams; barrel/globoidal cams; face cams; followers and closure; Geneva drives; ratchet/pawl indexers; escapements; dwell/indexing mechanisms; intermittent gear trains.

**Examples:** Geneva mechanism, roller cam, barrel cam, escapement, ratchet indexer.

**Cross-family links:** F06 (motion conversion), F10 (locks and pawls), F02 (motion sequencing).

### F08 — Underactuation, mechanical differentials & coupling

**Subfamilies:** tendon differential; whiffletree and lever redistribution; linkage-based adaptive fingers; gear differentials; differential springs; coupled digits/joints; passive adaptive force distribution; variable-ratio mechanisms.

**Examples:** whiffletree gripper, underactuated two-phalanx finger, cable differential, adaptive linkage gripper.

**Cross-family links:** F12 (grippers), F05 (tendons), F04 (differentials), F09 (elastic return).

### F09 — Springs, compliance, damping & variable stiffness

**Subfamilies:** coil/leaf/torsion springs; constant-force springs; series-elastic actuators; parallel-elastic elements; antagonistic stiffness systems; variable-stiffness transmissions; dampers and vibration isolation; negative-stiffness/energy storage.

**Examples:** series elastic joint, torsion spring return, variable-stiffness antagonistic pair, elastic counterbalance.

**Cross-family links:** F01 (integrated flexures), F10 (energy-loaded latches), F14 (suspension), F16 (mechanical metamaterials).

### F10 — Clutches, brakes, ratchets & locking

**Subfamilies:** friction and jaw clutches; sprag/roller one-way clutches; wrap-spring clutches; torque limiters; band/disc brakes; detents; pawl/ratchet; over-center locks; quick-release and self-locking devices.

**Examples:** slip clutch, sprag clutch, over-center latch, detent, torque-limiting coupling.

**Cross-family links:** F07 (indexing), F04 (gear trains), F01 (bistable compliant locking), F17 (docking retention).

### F11 — Serial, parallel & hybrid kinematic architectures

**Subfamilies:** serial chains; parallel planar mechanisms; Delta and translational parallel mechanisms; Stewart–Gough platforms; spherical wrists; hybrid chains; remote-center-of-motion and constrained-motion systems.

**Examples:** Delta mechanism, Stewart platform, spherical parallel wrist, RCM linkage.

**Cross-family links:** F02 (linkages), F03 (joint selection), F12 (manipulation), F18 (precision stages).

### F12 — Grippers and end-effectors

**Subfamilies:** parallel-jaw and angular; three-finger; underactuated multi-finger; compliant fingers; suction/adhesion; granular and layer jamming; mechanical expansion grippers; magnetic and needle grippers; adaptive fingertips; tool exchange.

**Examples:** parallel-jaw gripper, Fin Ray finger, tendon hand, suction cup array, jamming gripper.

**Cross-family links:** F01, F08, F13, F17 and F05. “Gripper” is often an **assembly/function** built from other mechanisms, not a mutually exclusive structural archetype.

### F13 — Soft and continuum robotics mechanisms

**Subfamilies:** pneumatic networks; bellows; fluidic elastomer actuators; fiber-reinforced soft actuators; tendon-driven continuum backbones; concentric tubes; soft pneumatic/hydraulic fingers; jamming and phase-change stiffness; electroactive soft actuation.

**Examples:** PneuNet bender, McKibben-type muscle, concentric-tube continuum device, tendon backbone, soft suction.

**Cross-family links:** F12 (gripping), F09 (variable stiffness), F05 (tendon actuation), F16 (materials/structures).

### F14 — Locomotion, steering & suspension mechanisms

**Subfamilies:** leg linkage gaits; crank-leg/hybrid wheel-leg; four-wheel steering and Ackermann; differential steering; omni/Mecanum wheel geometries; rocker–bogie; tracks; hopping/stored energy; climbing and adhesion; active/passive suspensions.

**Examples:** rocker–bogie, Jansen linkage, Klann leg, differential wheel mechanism, wheel–leg transformation.

**Cross-family links:** F02 (leg linkages), F09 (suspension), F04/F05 (drivetrains), F15 (reconfigurability).

### F15 — Deployable, origami, morphing & reconfigurable

**Subfamilies:** scissor expansions; telescoping assemblies; fold-core origami (Miura, waterbomb); kirigami; Hoberman/spherical deployables; shape morphing; multi-stable deployables; metamorphic/reconfigurable linkages.

**Examples:** scissor extender, Miura-ori folding sheet, Hoberman sphere, deployable tensegrity.

**Cross-family links:** F01 (bistability), F02 (scissor), F16 (lattice/tensegrity), F14 (shape-changing locomotion).

### F16 — Bio-inspired mechanisms & mechanical metamaterials

**Subfamilies:** auxetic and anisotropic lattices; tensegrity; Fin Ray effect; gecko-inspired dry adhesion; biological tendon arrangements; energy-absorbing architected structures; flapping-wing transmissions; directional friction.

**Examples:** auxetic lattice, tensegrity cell, Fin Ray finger structure, asymmetric friction pad.

**Cross-family links:** F01 (compliance), F12 (grasping), F13 (soft bodies), F15 (deployables). Many entries are **structures or design principles**, not conventional mechanisms: mark their entity type explicitly.

### F17 — Passive alignment, insertion, docking & contact adaptation

**Subfamilies:** remote-center compliance; floating wrists; compliant insertion devices; passive centering and funnel alignment; spring-loaded couplings; docking latches; mechanical search/guide features; breakaway interfaces.

**Examples:** remote-center compliance device, floating insertion head, self-centering coupler, compliant docking probe.

**Cross-family links:** F03 (joints/guides), F01 (compliant versions), F10 (latches), F12 (assembly tooling).

### F18 — Micro-mechanisms and precision stages

**Subfamilies:** MEMS flexures; piezoelectric flexure stages; stick-slip and inertial drives; inchworm mechanisms; microgrippers; electrostatic comb-drive mechanisms; precision XY/XYZ stages; compound flexure amplifiers.

**Examples:** folded-beam suspension, XY flexural stage, inchworm piezo drive, microgripper, comb drive.

**Cross-family links:** F01 (flexures), F06 (motion amplification), F09 (elastic stiffness), F11 (precision parallel stages).

### Future taxonomy hygiene

Some families capture physical **construction principles** (compliance), some capture **kinematic archetypes** (linkages), some capture **system roles** (grippers), and some capture **application domains** (locomotion). This is acceptable for a browse taxonomy, but the canonical database must also store orthogonal facets and distinguish `mechanism_pattern`, `mechanism_variant`, `implementation`, `component`, `assembly`, and `structural_principle` to avoid double-counting and misleading comparisons.

---

## 5. Mechanism relationships: the central intellectual property of the dataset

Mechanism entries should form a graph, not isolated cards. Every relationship is directional where relevant and ideally has a **reason, context, evidence, confidence and reviewer**.

### Proposed relation predicates

`is_variant_of`, `implements_function`, `same_function_as`, `alternative_to`, `replaces`, `composed_of`, `uses_component`, `transmits_to`, `can_be_combined_with`, `has_compliant_analogue`, `has_rigid_analogue`, `shares_kinematic_topology_with`, `requires`, `constrained_by`, `suitable_for`, `unsuitable_when`, `documented_in`, `validated_by`, `reported_failure`, `has_manufacturing_route`, `derived_from`.

### Initial manually curated relationship examples

| From | Relation | To | Conditions / note |
|---|---|---|---|
| Cross-axis flexural pivot | alternative_to | Rolling-element revolute bearing | Limited angular travel, elastic restoring torque; do not imply equivalent load capacity |
| Compliant parallelogram | alternative_to | Linear rail guide | Limited travel vs rolling-element design; stiffness trade-offs |
| Compliant four-bar | has_rigid_analogue | Rigid four-bar | Similar functional pattern, different stress/kinematic characteristics |
| Cartwheel flexure | alternative_to | Notch flexure | Compare axis drift, angular range, stress and fabrication |
| Planetary reducer | alternative_to | Cycloidal reducer | Compare reduction ratio, backlash, stiffness, cost, geometry |
| Strain-wave reducer | alternative_to | Cycloidal reducer | Precision robot joint; different loading, life and shock considerations |
| Ball screw | alternative_to | Rack-and-pinion | Linear conversion, travel and efficiency conditions differ |
| Lead screw | alternative_to | Ball screw | Efficiency, backdrive, cost and lubrication are not equivalent |
| Geneva drive | alternative_to | Cam-driven indexing | Discrete indexing; consider shock, dwell and speed |
| Slider-crank | alternative_to | Scotch yoke | Conversion to reciprocating motion; side loads/friction differ |
| Tendon differential | enables | Underactuated adaptive gripper | Distributes displacement/forces by tendon routing |
| Whiffletree linkage | enables | Adaptive multi-contact gripper | Passive load sharing under suitable configuration |
| Flexure hinge | is_variant_of | Compliant rotary guidance | Family relationship |
| PneuNet bender | implements_function | Soft bending actuation | Depends on material and pressure system |
| Remote-center compliance | suitable_for | Passive peg-in-hole alignment | Depends on insertion geometry and force envelope |
| Rocker–bogie | suitable_for | Passive terrain adaptation | Specific chassis and stability conditions |
| Miura fold | is_variant_of | Origami deployable structures | Geometric family, not a universal actuator |
| Fin Ray finger | composed_of | Compliant structural elements | Composition depends on specific design |
| Series elastic joint | can_be_combined_with | Planetary transmission | Depends on mechanical integration |
| Folded-beam suspension | is_variant_of | Flexural linear guidance | Precision motion, limited range |

**Key rule:** `alternative_to` must never mean “drop-in equivalent.” Attach `same_function`, `comparison_dimensions`, `applicability_conditions` and `exclusions`. An AI must be able to say “not comparable without more information.”

---

## 6. Orthogonal, agent-queryable classification facets

A single mechanism record should use these dimensions, many multi-valued:

1. **Entity type:** archetype/variant/implementation/assembly/component/principle.
2. **Canonical class & aliases:** terms, named inventors, multilingual synonyms, acronym expansion.
3. **Mechanical functions:** guide, transmit torque, amplify motion, change direction, grip, hold, self-align, index, reduce backlash, return energy, etc.
4. **Input/output:** rotary/linear/oscillatory/path/force/displacement/pressure; axes and direction relation.
5. **Mobility & topology:** DOF (plus compliance-dependent effective mobility), planar/spherical/spatial, open/closed chain, links/joints.
6. **Compliance architecture:** rigid/compliant/hybrid/continuum; concentrated/distributed; passive/active.
7. **Mechanical behavior:** bistable, self-locking, backdrivable, intermittent, constant-ratio, variable-ratio, underactuated, redundant, overconstrained.
8. **Performance characteristics:** stroke, angular range, transmission ratio, force/stiffness, mechanical advantage, efficiency, backlash, precision, hysteresis, frequency, damping—**only with units and conditions**.
9. **Constraints & failure modes:** load, fatigue, strain, contact pressure, temperature, friction/wear, buckling, resonance, lubrication, assembly alignment, contamination.
10. **Fabrication and materials:** printable, injection molding, laser-cut, machined, MEMS, monolithic, assembly steps; material-dependent.
11. **Scale:** MEMS, miniature, human-scale, industrial; avoid arbitrary promises of scale independence.
12. **Actuation interface:** motor/servo/tendon/pneumatic/hydraulic/piezo/manual/spring; separate driving source from intrinsic transmission.
13. **Applications & environments:** robot hand, precision stage, leg, surgical, industrial assembly, outdoor/dust/water, etc.
14. **Design maturity:** conceptual, published, simulated, prototype-tested, repeat-tested, deployed.
15. **Source evidence:** original citation, measured vs calculated vs quoted, applicable geometry, confidence, date.
16. **Rights:** media license, CAD license, data license and host permission, independently of article access.

**Unknown != zero != false.** Record missing dimensions as `null`/`unknown` with `verification_status`, not invented numerical values.

---

## 7. Data model and canonical granularity

### Entity levels

- **Pattern:** “Cross-axis flexural pivot” as a generalized mechanism concept.
- **Variant:** a specific topology/geometry family described in literature.
- **Implementation:** a documented design with geometry, material, source and configuration.
- **Evidence record:** a paper, CAD file, FEA model, physical test or manufacturer report tied to a variant/implementation.
- **Design relationship:** separately versioned statements linking mechanisms with conditions and sources.

This prevents counting 100 million random linkage instantiations as 100 million uniquely distinct mechanism types.

### Core entities / tables

`mechanisms`, `mechanism_names`, `families`, `subfamilies`, `functions`, `mechanism_facets`, `relations`, `constraints`, `source_documents`, `source_assets`, `claims`, `claim_evidence`, `implementations`, `measurements`, `licenses`, `review_events`.

### Example canonical entry (illustrative, not an experimentally qualified design)

```json
{
  "id": "mech.cross_axis_flexural_pivot",
  "schema_version": "0.1.0",
  "entity_type": "mechanism_pattern",
  "canonical_name": "Cross-axis flexural pivot",
  "aliases": ["crossed-strip flexure pivot"],
  "families": ["F01", "F03", "F18"],
  "subfamilies": ["flexural_rotary_joints"],
  "functions": ["limited_angle_rotary_guidance", "reduce_joint_backlash"],
  "input_motion": ["torque"],
  "output_motion": ["limited_angular_rotation"],
  "topology": {"compliance": "distributed", "primary_behavior": "elastic_rotation"},
  "qualitative_properties": [
    {"key": "sliding_joint_friction", "value": "absent_in_ideal_flexure"},
    {"key": "restoring_torque", "value": "present"}
  ],
  "quantitative_limits": [],
  "typical_constraints": [
    "angular_range_geometry_dependent",
    "stress_and_fatigue_must_be_checked",
    "axis_drift_and_parasitic_motion_may_matter"
  ],
  "relations": [
    {"predicate": "alternative_to", "target": "mech.revolute_bearing", "context": "limited_angle_low_backlash_guidance"},
    {"predicate": "same_function_as", "target": "mech.notch_flexure", "context": "elastic_rotary_guidance"}
  ],
  "sources": [],
  "evidence_level": "general_reference_only",
  "review_status": "draft",
  "rights_status": "original_descriptive_record",
  "updated_at": "2026-11-07"
}
```

**Claims should eventually be first-class records.** A numeric figure such as “±10°” cannot appear without geometry, material, load case, source and the type of evidence establishing it. Design rules may be expressed as inequalities, but validity ranges must travel with those rules.

### Suggested evidence tiers

| Tier | Description | Allowed wording |
|---|---|---|
| E0 | Curated concept, not independently checked | “Potential candidate; verify” |
| E1 | Primary literature, textbook, or reputable documented mechanism | “Documented in [source]” |
| E2 | Reproducible analytical calculation / FEA tied to geometry and assumptions | “Calculated/simulated for these inputs” |
| E3 | Measured physical experiment with test details | “Measured under these conditions” |
| E4 | Replicated or field-validated behavior with broader conditions | “Replicated/validated within the cited operating envelope” |

Evidence strength is **not** a universal mechanism quality score. A mechanism can be well established but poorly suited to a particular task.

---

## 8. Search, reasoning and agent interfaces

### Search pipeline

1. **Extract intent:** needed function, motion, constraints, exclusions, environment, preferences, incomplete inputs.
2. **Retrieve:** deterministic taxonomy/attribute filters + full-text lexical search + optional semantic retrieval + relationship expansion.
3. **Apply hard constraints:** reject or flag candidates that provably fail requirements; do not confuse unknown with pass.
4. **Compare:** transparent rationale using explicit user priorities (e.g. no gears, monolithic, 3D printable, minimum backlash).
5. **Report:** candidate list, tradeoffs, documented alternatives, source links, excluded candidates and **unknowns**.
6. **Continue:** request missing parameters only when they block meaningful selection; otherwise return conditional options.

**Ranking design:** avoid a single black-box “best” mechanism. Keep hard filters separate from ranking. Initial weighted relevance combines function match, constraint match, evidence completeness and design maturity, with adjustable priorities. Do not rank “high evidence” ahead of functional fit by default. Return the explanation for every included/excluded candidate.

### Suggested REST endpoints

```text
GET  /v1/families
GET  /v1/mechanisms/{id}
GET  /v1/mechanisms?family=F01&function=rotary_guidance
POST /v1/search
POST /v1/compare
GET  /v1/mechanisms/{id}/alternatives
GET  /v1/mechanisms/{id}/constraints
GET  /v1/mechanisms/{id}/sources
GET  /v1/schema
```

### Suggested MCP tools

- `search_mechanisms(requirements, filters, limit)` — function-first retrieval.
- `get_mechanism(mechanism_id)` — full canonical record.
- `compare_mechanisms(ids, application_context, criteria)` — tradeoffs and evidence.
- `find_alternatives(mechanism_id, requirements)` — cross-family candidates.
- `get_design_constraints(mechanism_id, context)` — known constraints, applicability and unknowns.
- `get_mechanism_sources(mechanism_id, asset_types)` — primary literature, permitted CAD and related evidence.
- `list_mechanism_taxonomy()` — tool discovery and classification.

**Example MCP response envelope:**

```json
{
  "query": {"function": "rotary_guidance", "backlash": "minimize", "travel": "small"},
  "matches": [{
    "id": "mech.cross_axis_flexural_pivot",
    "selection_reason": ["elastic rotary guidance", "no conventional sliding joint"],
    "limitations": ["travel is limited", "restoring torque", "fatigue check"],
    "conditional_fit": true,
    "evidence": [],
    "unverified": ["required torque", "angular range", "material", "life cycles"]
  }],
  "requires_engineering_validation": true
}
```

### Architectural choice

**Start simple:** human-editable YAML/JSON in Git + validation scripts → PostgreSQL (full-text, JSONB, optionally pgvector) → one backend exposing REST and MCP → thin searchable website. A separate graph database is **not required for MVP**; adjacency/relationship tables in Postgres are enough. Add richer graph infrastructure only if query complexity demands it.

**Proposed repo structure:**

```text
mechanical-design-intelligence/
  data/mechanisms/{family}/{stable-id}.yaml
  data/sources/{source-id}.yaml
  schemas/mechanism.schema.json
  schemas/relation.schema.json
  taxonomies/families.yaml
  taxonomies/functions.yaml
  api/openapi.yaml
  server/search/
  server/mcp/
  web/
  examples/agent-workflows/
  tests/schema/
  tests/queries/
  docs/contributing.md
  docs/source-rights-policy.md
  docs/evidence-standard.md
```

Core engineering: automated schema validation, units normalization (SI internally), duplicate/alias handling, citation integrity tests, versioning, update provenance, API versioning, query tests, rate limits, caching, and structured feedback logging with privacy safeguards.

---

## 9. Source landscape: initial verified reconnaissance

The following are **sources reviewed at an initial reconnaissance level on 7 November 2026**, not an exhaustive legal, data-quality or API audit. “Take” means use the *underlying ideas/taxonomic concepts, citations, independent annotations or licensed assets where allowed*—**not automatic copying**. The detailed follow-up audit and rights checks are planned in [`02_RESEARCH_AND_BUILD_PLAN.md`](02_RESEARCH_AND_BUILD_PLAN.md).

| ID | Source | What is useful | Extract/learn initially | Rights or diligence note |
|---|---|---|---|---|
| S01 | [IISc M2D2 compliant mechanism collection](https://mecheng.iisc.ac.in/m2d2/CMcollection/) | Functional categories, individual models, illustrations/video, links to CAD/FEA | Category concepts: grippers, clamps, clutches, crimpers, displacement amplifiers, suspensions, path/direction changers, shape changers, bistable and contact-aided | Site footer states all rights reserved; download availability does not establish permission to redistribute |
| S02 | [IISc Model 16 — compliant gripper](https://mecheng.iisc.ac.in/m2d2/CMcollection/16.html) | Specific topology-optimized gripper, linked CAD, physical/digitized model | Model function: pulling a central left input bar draws right contact points together; **design lesson:** optimization can produce unnecessarily complex forms | Link, analyze, cite; do not copy CAD or images into product until licensing cleared |
| S03 | [IISc collection — About](https://mecheng.iisc.ac.in/m2d2/CMcollection/about.html) | Topology focus, model/FEA/video structure | Separate general topology from scaled/geometric implementation; keep provenance | Explicit original paper attribution may need additional primary-reference research |
| S04 | [mechanisms.ln.gy — index](https://mechanisms.ln.gy/) | 4,060-entry classical mechanisms browser | Names, functional breadth, alias discovery; competitor research | Animations derived from Nguyen Duc Thang; inspect reuse/API/terms separately |
| S05 | [mechanisms.ln.gy — taxonomy](https://mechanisms.ln.gy/taxonomy/) | Multidimensional classification including archetype, motion, behavior, topology, DOF | **Important benchmark:** many of our planned facets already exist; differentiate via source-backed engineering choices, alternatives, programmatic tool access | Do not copy taxonomy text wholesale; independent design and licensing review |
| S06 | [mechanisms.ln.gy — about](https://mechanisms.ln.gy/about/) | Sources and provenance of large animated corpus | Classical bibliographic leads: Sclater, Artobolevsky, Chironis, Reuleaux, Brown, Nguyen Duc Thang | Site taxonomy LLM-assisted with ongoing verification; assess accuracy |
| S07 | [RoboticWorx Mechanism Atlas](https://roboticworx.io/pages/mechanisms) | 126 illustrated mechanisms in 19 sets, motion/strengths/watch-outs UI | Design inspiration for interactive plate and comparison fields | Creator says plates were AI-generated; technical validation and asset rights need independent checking |
| S08 | [MIT LINKS project](https://decode.mit.edu/projects/links/) and [code](https://github.com/ahnobari/links) | 100 million generated planar linkage instances, coupler-path generation | Separate topology, instance and trajectory; possible future quantitative trajectory lookup | Examine actual repository/data license and download terms before reuse; not interchangeable with 100M mechanism types |
| S09 | [Cornell KMODDL](https://engineering.library.cornell.edu/kmoddl/) | Historic Reuleaux machines and multimedia | Classical mechanism naming, historical lineage, cross-references | Rights of digitized media may differ from underlying public-domain engineering ideas |
| S10 | [507 Mechanical Movements](https://507movements.com/about.html) | Historic movement types, original book illustrations and proprietary animations | Historical archetypes and motion transformation vocabulary | Site explicitly prohibits reproducing animations; older underlying book is public domain in many jurisdictions but digitizations need separate review |
| S11 | [Atlas Mechanica](https://atlasmechanica.com/) and [repository](https://github.com/atlasmechanica/atlasmechanica) | Open atlas with subject/source/model relationships, interactive kinematics, planned function-based solution search | Architectural reference and **emerging direct competitor**; its repo displays Apache-2.0 for code | Audit exact code vs content rights and roadmap; do not assume feature gaps |
| S12 | [Mechanical Library](https://mechanical-library.org/) | Physical demonstrations, 3D, printable and Lego models | Accessible explanation structure and motion illustrations | Review per-asset licensing and authorship |
| S13 | [Harvard Soft Robotics Toolkit](https://softroboticstoolkit.com/) and [lab overview](https://biodesign.seas.harvard.edu/soft-robotics-toolkit) | Soft actuators, sensors, fabrication docs, design files | Soft/continuum subfamilies; fields for fabrication and operating medium | “Open source” is not a substitute for per-component license inventory |
| S14 | [BYU Compliant Parallel-Guiding Scaling Data (2025)](https://scholarsarchive.byu.edu/data/74/) | Force/displacement and strain vs size in compliant parallel guides | Excellent example for implementation-linked **quantitative evidence** | Listed **CC BY 4.0**, with attribution obligations; verify file-level coverage and scientific assumptions |
| S15 | [BYU Scalable Flat In-Plane-Motion Mechanical Springs data (2026)](https://scholarsarchive.byu.edu/data/107/) | CSV force/displacement datasets for folded-beam, chevron, interlaced, canted and variable-stiffness spring arrangements | Subfamily labels, curves, validation schema | Listed **CC BY 4.0**, with attribution; verify metadata and reuse context |
| S16 | [BYU Compliant Mechanisms & Robotics research](https://robotics.byu.edu/research-labs/) | Research lineage and discovery links | Identify primary publications, authors, working nomenclature | Paper/CAD rights vary by publication |
| S17 | [Mechanisms for Robotic Grasping and Manipulation (2021)](https://doi.org/10.1146/annurev-control-061520-010405) | Taxonomy of fingers, transmissions, underactuation and mechanical intelligence | Map gripper concepts to actual mechanism architecture | Copyrighted review; summarize independently and cite |
| S18 | [Current Designs of Robotic Arm Grippers (2023)](https://www.mdpi.com/2218-6581/12/1/5) | Systematic gripper taxonomy by design and actuation | Independent cross-check of F08/F12/F13 and keyword expansion | Confirm article-specific Creative Commons license for any reused tables/figures |
| S19 | [Variable Transmission Mechanisms for Robotics (2025)](https://ramagazine.ieee.org/2025/06/24/variable-transmission-mechanisms-for-robotic-applications-a-review-survey/) | Survey of variable transmission architectures | Expand F04/F08/F09 and compare kinematic vs actuation distinctions | Use source for literature discovery and independently written syntheses |
| S20 | [Systematic review of compliant grippers (2025)](https://www.sciencedirect.com/science/article/pii/S0094114X24003276) | Reviews >1,000 manuscripts, different synthesis and actuation methods | Search methodology, gap hypotheses, application vocabulary | Data available on request; not an open bulk download by default |
| S21 | [Open Dynamic Robot Initiative actuator hardware](https://github.com/open-dynamic-robot-initiative/open_robot_actuator_hardware) | Real actuator and robot hardware assemblies, belts, drives and mechanics | Trace mechanisms to practical robotic integrations and known issues | Repo mechanics page lists BSD 3-Clause; inspect subfolders/assets for exceptions |
| S22 | [Open-Source Leg hardware](https://opensourceleg.org/hardware/) | Documented assemblies and accessible manufacturing | Downstream use cases for serial joints, transmissions and elasticity | Model assets and software may have different licenses |
| S23 | [NASA Mechanism Design/Development Standard](https://ntrs.nasa.gov/citations/20220014671) | Requirements and verification language | Future validation and engineering evidence policy | Not a substitute for certification; initially reference only |
| S24 | [Monolithic scalable compliant mechanisms (2026)](https://doi.org/10.1371/journal.pone.0340272) | Recent compliant-mechanism design research | New types/scale thinking for F01 | Check paper and supplemental data license independently |
| S25 | [Adaptive robotic grippers review (2026)](https://pmc.ncbi.nlm.nih.gov/articles/PMC13667752/) | Compliance routes: underactuated, soft, variable stiffness | Cross-family conceptual model and vocabulary | Cite as research, verify individual license if reusing figures |

### Specific insights from compliant mechanism sources

**IISc M2D2 is an especially valuable *functional ontology seed*.** Its home page groups mechanisms by the engineering role achieved; it makes the case that an index should include *function* rather than merely “compliant” as a category. The site links, according to its About page, photos, videos, FEA and CAD for models, but does **not** grant blanket redistribution permission. [S01–S03]

**Model 16 is a useful warning against over-optimizing geometry.** The source itself notes that its topology-optimized gripper is more complicated than necessary despite illustrating an interesting solution. Add `complexity_penalty`, `simpler_alternative` and `manufacturability_risks` as possible **evidence-backed** comparison dimensions, not fabricated scores. [S02]

**BYU data demonstrates the next level of differentiation.** Some entries may be connected to measured or modeled load–displacement and strain datasets, not just descriptive records. The 2025 parallel-guiding and 2026 SFIMS datasets are particularly useful for learning how to represent a *test condition + measured curve + reference + license*. [S14–S15]

**The strongest competitor lesson:** mechanisms.ln.gy already does sophisticated faceted search and Atlas Mechanica is explicitly moving toward relationship-linked models and function-based solution discovery. We should not claim novelty in taxonomy, interactive visualizations or “mechanism alternatives” without testing competitors' current APIs and capabilities. [S04–S06, S11]

---

## 10. Data sourcing, intellectual property and quality policy

1. Maintain a **source registry** with owner, URL, provenance, publication, retrieval date, assets available, license evidence, restrictions, import eligibility and notes.
2. Distinguish **linking**, **independently writing factual descriptions**, **reuse of source text**, **hosting of images**, **hosting CAD**, **import of numerical datasets**, and **embedding third-party content** as distinct rights questions.
3. Default to linking to source CAD/media unless express license or permission supports redistribution; preserve creators and literature references.
4. Do not use images or animations from sites that prohibit it. For example, 507movements.com explicitly restricts its own animations.
5. Academic paper availability is not equivalent to permission to copy figures, CAD or associated files. A downloadable asset is not automatically open licensed.
6. Avoid blind web scraping and bulk redistribution; review site terms, robots instructions, database rights (especially in Europe), patents, and applicable license conditions. Seek legal review when commercializing high-volume material.
7. Record **mechanical design IP risk** separately from copyright: mechanisms may be subject to active patents even when general principles are published.
8. AI-assisted extraction can produce drafts but **never** grant itself source authority or a verified evidence tier. Engineering-focused review is required.
9. For critical engineering assertions, trace source → claim → supporting measurement/calculation → validity conditions.
10. Keep an honest audit trail: who verified a fact, which publication/version, what changed, and when.

**Licensing hypothesis (not a final decision):** public mechanism facts and independently authored annotations could use CC BY 4.0 (or CC0 for original metadata where appropriate), code could use Apache-2.0 or MIT, while licensed third-party assets retain their original license. Do not relicense source content as if it were ours. This choice requires an explicit project licensing decision.

---

## 11. Competitive positioning and strategic choices

### What to avoid

- Another static collection of 3D models with no function-based retrieval.
- Another educational animation catalog competing on volume with 4,060-index sources.
- Another hardware building platform competing with CAD/PCB/schematic authoring.
- A recommendation chatbot whose explanations sound authoritative but have no traceable evidence.

### What to pursue

- Agent-first **query contracts**, not an MCP wrapper bolted on to a website.
- Mechanics-specific disambiguation: `DOF`, `stroke`, `backdrivability`, `backlash`, `precision`, `printability`, `fatigue` have distinct meanings.
- Comparison and conditional alternatives across family boundaries.
- Primary-source linking, evidence tiering and separately recorded verified implementations.
- Measurable uplift in AI-generated mechanical architecture decisions versus agent-only baselines.
- Public contributions and a credible technical review process.

**Moat hypothesis:** cumulative mechanism relationships + evidence-linked implementations + contribution/review network + workflow integration. An MCP endpoint alone has little defensibility, and curated source links alone are easy to imitate.

---

## 12. Free product, potential commercial strategy, and future modules

### Initial free/open product

- Discover, search, filter and compare general mechanism types.
- Browse 18 families and subfamilies.
- Open mechanism schema, baseline data, source links and alternatives.
- Free public MCP/REST usage within reasonable limits.
- Community corrections and contributions.

A generous free mechanism layer is the **adoption funnel** and platform-independent integration surface. Rate limits and licenses must not make experimentation impractical.

### Potential paid offering (hypothesis, validate later)

Sell **engineering assistance with higher verification or computational cost**, not access to generic mechanism names. Potential paid interfaces: batch selection and enterprise data governance, verified parametric implementation datasets, traceable design checks, source-backed comparison reports, constraints calculators, hosted engineering compute and auditable design histories.

### Future modules (recorded now; scoping deferred)

| Module | Problem solved | Future evidence/computational dependency |
|---|---|---|
| Hardware Compatibility Graph | Will parts/subsystems work together? | Vendor specs, connectors, mechanical interfaces, standards, test reports |
| Engineering Constraints API | What loads, deflections, tolerances and operating envelopes matter? | Validated equations, geometry, materials, boundary conditions |
| Component Selection Engine | Which actuator, bearing, screw, sensor, etc. best suits the design? | Current catalog and compatibility data |
| Design Failure Database | What fails in similar designs and why? | Published incidents, lab outcomes, anonymized contributions, context |
| Manufacturing Rules API | What can be reliably fabricated by a given process? | Process- and vendor-specific rules, experimental validation |
| Parametric CAD & implementation library | Generate configurable candidate geometry | Reliable parametric models and ownership/right-to-use |
| Structural / joints / links mechanics | Static strength, compliance, contact, buckling and elastic behavior | Geometry, loads, materials, validated solvers |
| Vibration & dynamic analysis | Modal response, resonance, dynamic loads | Mass/inertia, damping, boundary conditions, solver integration |
| Fatigue & durability analysis | Estimated life under cyclic loads | Material S–N/strain-life data, uncertainty, loading histories |
| Topology & multidisciplinary optimization | Generate improved designs under constraints | Solvers, validation, compute infrastructure, manufacturing constraints |
| Simulation & sim-to-real evidence | Compare predicted and measured mechanism performance | Experiments, reproducible models, calibration, field feedback |

Modules above are **roadmap possibilities**, not promises. Their economics, liability, technical scope and interfaces should be decided only after the mechanism corpus demonstrates adoption and value.

### Sustainable business hypotheses to test

- Who will pay: CAD agent vendors, AI hardware platforms, robotics developers, design/CAE integrators, engineering teams?
- For what measurable outcome: reduced concept search time, fewer bad choices, lower iteration costs, better design auditability?
- Which data must stay open to drive trust, and which services justify paid usage?
- Are API fees attractive compared with per-seat engineering tools, cloud simulation and professional services?
- Can evidence and deployment outcomes create a compounding data advantage without locking contributors out?

---

## 13. Success criteria and product risks

### North-star metric

**Proportion of representative mechanical design questions where an agent using MDI produces a better-evidenced and technically suitable shortlist than the same agent without MDI**, independently reviewed.

### Leading indicators

- Coverage by family/subfamily/function (not raw row count alone).
- Percent of entries with primary citation, alternatives, constraints and reviewed classification.
- Share of natural-language queries returning relevant, explainable candidates.
- Incorrect recommendation / hard-constraint violation rate.
- Citation accuracy and numerical-claim validity.
- MCP tool-call success, latency and cost.
- External platform integrations, repeat API use and contributions.

### Risks / mitigations

| Risk | Mitigation |
|---|---|
| Extensive existing catalogs already exist | Specialize in cross-platform **engineering decision data and verified provenance** |
| Agents never call tools | Test real agents; publish workflow examples; measure before/after; optimize tool affordances |
| LLM invents specs or generalizes beyond evidence | Typed claims, units, review levels, unknown fields, hard constraints, explanations |
| Rights to CAD/images are unclear | Link-first, per-asset license policy, own diagrams where feasible |
| Taxonomy becomes contradictory | Orthogonal facets, stable entity levels, graph constraints, review process |
| One family dominates the dataset | Minimum representation across all 18 + coverage dashboard |
| Need for costly engineering validation becomes overwhelming | V1 is information/selection; precise calculations are later scoped services |
| API vendor/platform dependency | Portable schema, REST and MCP, transparent ranking logic and open data |

---

## 14. Delivery phases (overview)

**Phase 0 — Source intelligence:** systematic search, capability/licensing evaluation, competitor feature tests, bibliography and candidate pool.  
**Phase 1 — Ontology:** settle 18-family taxonomy, subfamilies, facets, relationship predicates, entity identity and evidence standards.  
**Phase 2 — Seed corpus:** reviewed representative entries across all 18 families, especially core linkages, compliant, transmissions, joints and underactuation.  
**Phase 3 — Agent-native architecture:** structured data, search engine, REST and MCP, samples, reproducible tests, website.  
**Phase 4 — Validate usefulness:** query benchmark, human engineering review, head-to-head tests with/without the database, real tool integrations.  
**Phase 5 — Scale and community:** rights-safe imports, contribution workflow, richer CAD/experimental evidence and source partnerships.  
**Phase 6 — Later paid engineering services:** only after adoption and measurable high-value user needs.

See the **separate detailed execution plan** for tasks, criteria and outputs.

---

## 15. Open decisions and key questions

1. Is the principal unit a *mechanism family*, a *mechanism type*, or a *design pattern*? Proposed answer: stable mechanism patterns plus separate variants/instances.
2. Should “robot-specific” be a filter or a scope restriction? Proposed answer: **filter**; classic mechanisms remain useful to robots.
3. Which assets can be distributed versus only referenced? Must be proven per source/license.
4. How much correctness is required before an entry is searchable? Proposed minimum: canonical name, function, family, summary, source, constraints/unknowns and review status.
5. How should alternative ranking be evaluated? Proposed: independently curated test queries and engineer judgments, with transparent hard filters.
6. Which source partnerships could unlock rights-cleared CAD/FEA artifacts? Prioritize IISc and BYU outreach if feasible.
7. What counts as “largest”? Clearly publish *unique reviewed mechanism types, variants, tested implementations and families* separately.
8. Which adjacent families are missing? Fluid machines, pumps and valves, coupling mechanisms, fastening and material-handling devices may justify future taxonomy extensions or cross-cutting subfamilies. Do not arbitrarily freeze the taxonomy at 18.
9. Is the adoption driver a public explorer, coding-agent workflow, CAD plugin, or MCP registry? Measure it.
10. Does the free database produce measurable better decisions? This is the first major go/no-go question.

---

## 16. Reference bibliography — direct links

All URLs below were inspected at least at their landing, index or article-description level in the initial November 2026 reconnaissance. Deeper technical and rights assessments remain tasks, not completed audits.

**Mechanism catalogs, repositories and competitors**

- [S01] IISc M2D2 Compliant Mechanism Collection — https://mecheng.iisc.ac.in/m2d2/CMcollection/
- [S02] IISc M2D2 Model 16 — https://mecheng.iisc.ac.in/m2d2/CMcollection/16.html
- [S03] IISc M2D2 About — https://mecheng.iisc.ac.in/m2d2/CMcollection/about.html
- [S04] Mechanisms index — https://mechanisms.ln.gy/
- [S05] Mechanisms taxonomy — https://mechanisms.ln.gy/taxonomy/
- [S06] Mechanisms about — https://mechanisms.ln.gy/about/
- [S07] RoboticWorx Mechanism Atlas — https://roboticworx.io/pages/mechanisms
- [S08] MIT LINKS — https://decode.mit.edu/projects/links/ ; source https://github.com/ahnobari/links
- [S09] Cornell KMODDL — https://engineering.library.cornell.edu/kmoddl/
- [S10] 507 Mechanical Movements — https://507movements.com/about.html
- [S11] Atlas Mechanica — https://atlasmechanica.com/ ; code https://github.com/atlasmechanica/atlasmechanica
- [S12] Mechanical Library — https://mechanical-library.org/

**Compliant, soft and robotic research/data**

- [S13] Harvard Soft Robotics Toolkit — https://softroboticstoolkit.com/ ; lab description https://biodesign.seas.harvard.edu/soft-robotics-toolkit
- [S14] BYU Compliant Parallel-Guiding Mechanisms Scaling Data (2025), CC BY 4.0 indicated — https://scholarsarchive.byu.edu/data/74/
- [S15] BYU Scalable Flat In-Plane-Motion Mechanical Springs (2026), CC BY 4.0 indicated — https://scholarsarchive.byu.edu/data/107/
- [S16] BYU Robotics labs / Compliant Mechanisms and Robotics Group — https://robotics.byu.edu/research-labs/
- [S17] Babin & Gosselin, *Mechanisms for Robotic Grasping and Manipulation* (2021) — https://doi.org/10.1146/annurev-control-061520-010405
- [S18] *Current Designs of Robotic Arm Grippers: A Comprehensive Systematic Review* (2023) — https://www.mdpi.com/2218-6581/12/1/5
- [S19] *Variable Transmission Mechanisms for Robotic Applications: A Review* (2025) — https://ramagazine.ieee.org/2025/06/24/variable-transmission-mechanisms-for-robotic-applications-a-review-survey/
- [S20] *Systematic Mapping of Synthesis Methods for Compliant Grippers* (2025) — https://www.sciencedirect.com/science/article/pii/S0094114X24003276
- [S21] Open Dynamic Robot Initiative hardware — https://github.com/open-dynamic-robot-initiative/open_robot_actuator_hardware
- [S22] Open-Source Leg hardware — https://opensourceleg.org/hardware/
- [S23] NASA Design and Development Requirements for Mechanisms / NASA-STD-5017B — https://ntrs.nasa.gov/citations/20220014671
- [S24] *Monolithic Scalable Compliant Mechanisms* (2026) — https://doi.org/10.1371/journal.pone.0340272
- [S25] *Adaptive Robotic Grippers for Intelligent Manipulation* (2026) — https://pmc.ncbi.nlm.nih.gov/articles/PMC13667752/

### Research reading notes

- **IISc 16:** This is not just an example image: it is specifically a topology-optimized compliant gripper in which pulling a bar brings two right-side points together. The source itself flags design complexity. Its linked CAD is external; rights require checking.
- **MIT LINKS:** Public description states 100 million generated 1-DOF planar linkages and associated coupler paths, not 100 million independently verified industrial designs. Future use may be trajectory-nearest-neighbor retrieval, not a first-version knowledge entry import.
- **mechanisms.ln.gy:** reports approximately two dozen classification dimensions and 4,060 illustrated mechanisms, including behavior, topology and input/output motion. It is the closest taxonomy competitor identified so far.
- **BYU data:** Both named datasets display CC BY 4.0 and include numerical data; they offer an excellent test for provenance-rich evidence records.
- **507 movements:** Author states its animations are proprietary and may not be copied; be conservative with digitized images even when the historic book text is old.
- **Atlas Mechanica:** openly documents a separate source/model/subject relationship architecture and a planned by-function solver. It is a priority competitor to monitor.

---

*This document is a project specification and research foundation, not a representation that the database has already been created or that all referenced assets are licensed for reuse.*
