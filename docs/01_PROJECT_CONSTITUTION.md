# 01_PROJECT_CONSTITUTION

**Working Name:** OIL Safety Intelligence Platform *(working name — not a formally finalized product name)*
**SIH Problem Statement:** SIH26165
**Organization:** Oil India Limited (OIL)
**Category:** Software
**Theme:** Smart Automation
**Team:** Tech Smashers
**Document Status:** Authoritative — governs all other project documents
**Document Owner:** Whole team; changes require the process in Section 20

---

## 1. Document Purpose

This constitution exists because a hackathon team under deadline pressure will, by default, drift: one member will start describing the system as "predicting fatalities," another will quietly assume a real OIL dataset exists, a third will hard-code a database schema before the AI architecture is agreed. Each drift is small and reasonable in isolation. Together, across ten documents and six people, they produce an inconsistent product that cannot survive a judge's first follow-up question.

This document is the single highest-level source of truth for the project. Every other document in this set (`02` through `16`) must remain consistent with what is written here. Where a lower-level document appears to conflict with this constitution, the conflict is resolved using the process in **Section 20 — Change Management**, not by silently overriding either document.

This constitution is implementation-agnostic by design. It defines *what* the product is, *why* it exists, *what it must and must not do*, and *what principles govern every decision below it*. It deliberately does not specify ML model names, database schemas, API contracts, or UI layouts — those belong to `08_AI_ARCHITECTURE`, `09_DATABASE_DESIGN`, `10_API_SPECIFICATION`, and `12_UI_UX_DESIGN` respectively, and must themselves remain consistent with the principles set out here.

Any team member, or any AI agent assisting the team, should be able to read this single file and correctly answer: what are we building, why, what must it do, what must it never do, and how do we decide when we're unsure.

---

## 2. Product Identity

| Field | Value |
|---|---|
| Product name | **OIL Safety Intelligence Platform** *(working name)* |
| SIH Problem Statement ID | SIH26165 |
| Organization | Oil India Limited (OIL) |
| Category | Software |
| Theme | Smart Automation |
| Team | Tech Smashers |

**One-line product definition:** An AI/NLP-powered platform that reads OIL's free-text Unsafe-Act, Unsafe-Condition, and Near-Miss safety reports and converts them into structured, explainable, and actionable Serious Injury & Fatality (SIF) intelligence for HSE teams.

**Product mission:** To help OIL's HSE function see the SIF potential that is already present — but currently hidden — inside its existing safety-reporting stream, with evidence attached, so that intervention can happen before a serious injury or fatality occurs rather than after.

**Product vision:** A future in which no high-potential precursor pattern sits unnoticed in a report queue for a full review cycle, because an explainable AI layer surfaces it continuously, and HSE teams spend their attention on the sites and activities where fatal potential is demonstrably highest.

---

## 3. Problem Definition

OIL collects a large and growing volume of Unsafe-Act (UA), Unsafe-Condition (UC), Near-Miss, and related safety observations, primarily as **free-text narratives** written by workers and supervisors in their own words. This is the problem's ground truth, and it must not be restated or softened in any downstream document:

- The reports are **unstructured text**, not clean structured data. The same underlying situation ("no gas test before confined-space entry") can be phrased dozens of different ways across dozens of reports.
- The **volume is large enough** that no human team can give every report the depth of attention it deserves within a short time window.
- Today, this volume is **triaged manually, at periodic intervals** (e.g. monthly or quarterly), per the official problem statement. This means a dangerous signal present in a report today may not receive analytical attention until the next triage cycle.
- Buried inside this text volume are **SIF (Serious Injury & Fatality) precursors** — situations that, whether or not anyone was actually hurt, carried real potential for a severe or fatal outcome. These precursors do not announce themselves; a report that says "no injury" can still describe a near-fatal situation.
- Because manual review is periodic and effort-constrained, **recurring precursor patterns** (the same activity, site, hazard, and barrier failure appearing again and again) are difficult to notice at the individual-report level, even though they represent the clearest actionable signal available.
- HSE teams consequently struggle to **prioritize** where to intervene first: raw incident counts and report volume are poor proxies for where fatal potential is actually concentrated.

This is a text-understanding-and-prioritization problem before it is a machine-learning problem. Any solution document that frames this primarily as "build a classifier" without addressing the volume, manual-review, and prioritization dimensions has drifted from the actual problem.

---

## 4. Solution Definition

The product transforms a raw report into structured safety intelligence through the following high-level flow. Each stage below is a *responsibility*, not an implementation prescription — the concrete techniques, models, and services used to fulfil each responsibility belong in `07_SYSTEM_ARCHITECTURE` and `08_AI_ARCHITECTURE`.

```mermaid
flowchart LR
    A[Raw Safety Reports] --> B[NLP Processing / Preprocessing]
    B --> C[Safety Signal Extraction]
    C --> D[SIF Potential Engine]
    D --> E[Explainability / Evidence]
    E --> F[Barrier Failure Analysis]
    F --> G[IOGP Life-Saving Rule Mapping]
    G --> H[Recurring Pattern Discovery]
    H --> I[HSE Prioritization]
    I --> J[Dashboard / Actionable Insight]
```

**Raw Safety Reports.** The system's input boundary: free-text UA, UC, near-miss, and (where available) incident narratives, plus whatever basic metadata accompanies them (date, site, report type). Nothing about the report's content is assumed or normalized before this stage.

**NLP Processing / Preprocessing.** The raw narrative is cleaned and prepared for analysis — this is where inconsistent spelling, abbreviations, and sentence structure are handled so that every later stage receives text in a consistent, analyzable form. This stage does not yet make any safety judgment; it only prepares the text.

**Safety Signal Extraction.** The prepared text is scanned for the conceptual categories defined in **Section 10** — hazard, activity, location, exposure, control/barrier status, and so on. This stage's responsibility is to turn language into structured, typed signals, including correctly handling negation (distinguishing "test completed" from "test not completed").

**SIF Potential Engine.** The extracted signals are combined to assess whether the reported situation carried potential for serious injury or fatality — independent of what actually happened. This stage's responsibility is defined precisely in **Section 9** and must never be described as predicting a future event.

**Explainability / Evidence.** Every SIF Potential judgment is accompanied by the specific signals and phrases that justify it. This stage's responsibility is to make the engine's reasoning inspectable, not just its conclusion.

**Barrier Failure Analysis.** The system identifies which specific safety barriers or controls were present, missing, incomplete, or failed in the reported situation, per the barrier states defined in **Section 11**. This is a distinct responsibility from SIF Potential itself — barrier status is *evidence toward*, not a synonym for, SIF Potential.

**IOGP Life-Saving Rule Mapping.** Where the extracted signals correspond to one or more of the IOGP Life-Saving Rule categories, the system tags the report accordingly, with the reasoning behind the tag visible. This mapping is evidence-based, not a keyword lookup — see **Section 12**.

**Recurring Pattern Discovery.** Across many reports, the system surfaces combinations of activity, location, hazard, and barrier failure that recur more than an isolated incident would suggest, per the philosophy in **Section 13**. This stage's output is organizational, not per-report.

**HSE Prioritization.** The system ranks sites, activities, and recurring patterns by their concentration of SIF potential (not raw report volume), so that HSE attention goes where fatal potential is demonstrably highest, per **Section 14**.

**Dashboard / Actionable Insight.** All of the above is presented through an interface that lets HSE explore individual reports, recurring patterns, and prioritized hotspots, and record their own review decisions. The dashboard is a presentation and decision-support layer — it does not make decisions on HSE's behalf.

---

## 5. Core Product Principles

These principles govern every design and implementation decision made anywhere in this project. Where a later document must choose between two reasonable options, these principles — in the priority order given in **Section 24** — decide.

1. **Safety-first.** When a technical trade-off pits demo polish or convenience against safety-relevant correctness (e.g. an over-simplified barrier rule that could hide a real gap), safety-relevant correctness wins.
2. **Human-in-the-loop.** No AI output in this system is a final safety decision. Every classification is presented to a human reviewer for accept/correct/reject, and this loop is a product requirement, not an optional feature.
3. **Explainability over black-box decisions.** A SIF Potential label without the evidence behind it is treated as an incomplete output, not a valid one. Every stage that produces a judgment must also produce the reasoning behind it.
4. **Context over keyword-only detection.** The same keyword can describe a safe or unsafe situation depending on surrounding context (permits confirmed vs. permits skipped). Any detection logic that cannot distinguish these two cases is not acceptable, regardless of how simple it would be to ship.
5. **Evidence-backed outputs.** Every output surfaced to HSE — a SIF flag, a barrier-failure claim, an LSR tag, a recurring-pattern claim — must be traceable to specific source text or aggregated report data. No output is presented as a bare assertion.
6. **SIF Potential ≠ future fatality prediction.** The system assesses whether a *reported* situation contained SIF potential. It does not forecast that a fatality will occur. This distinction must be preserved in every document, every UI string, and every conversation with judges — see **Section 9**.
7. **Barrier-aware reasoning.** SIF potential judgments should be grounded in identifiable hazard-exposure-barrier relationships (Section 11), not in vague "this sounds dangerous" pattern-matching untethered to a specific control.
8. **OIL / IOGP domain alignment.** Taxonomies, terminology, and categories used throughout the product (UA/UC/Near-Miss, the nine IOGP Life-Saving Rules) follow established Oil & Gas / HSE industry usage rather than terms invented for engineering convenience.
9. **Prototype-first practicality.** Under the current deadline, a complete, working, end-to-end vertical slice is worth more than a partially-built, more sophisticated architecture. See **Section 21**.
10. **No fabricated data or performance claims.** Every number presented as a real measurement must be a real measurement. Everything else is explicitly labelled illustrative, synthetic, or prototype-stage. See **Section 16**.
11. **Privacy and data minimization.** Safety reports may reference individuals and site-specific vulnerabilities. Each component and role sees only the data it needs, and no more.
12. **Modular architecture.** NLP, signal extraction, SIF reasoning, explainability, barrier analysis, LSR mapping, pattern discovery, and dashboard are conceptually separate components with clear interfaces, so that any one of them can be replaced or improved independently.
13. **Deterministic behavior where safety-critical.** Where a safety-relevant rule is already well-established and unambiguous (e.g. "confined-space entry with no gas test and no standby person is a barrier failure"), it should be encoded deterministically rather than left entirely to a probabilistic model's discretion.
14. **Clear separation between AI inference and HSE decision-making.** The platform's role is decision *support*. Authorized HSE personnel retain sole authority over safety decisions, interventions, and any action affecting field operations.

---

## 6. Product Boundaries

### The product DOES:

- Ingest UA, UC, Near-Miss, and (where available) incident safety reports.
- Process free-text narratives using NLP.
- Extract safety-relevant signals (hazard, activity, exposure, control/barrier status, etc.).
- Assess whether a reported situation carries SIF potential.
- Provide evidence and reasoning behind every SIF Potential assessment.
- Identify barrier/control issues (missing, incomplete, failed, bypassed).
- Map relevant situations to applicable IOGP Life-Saving Rules.
- Discover recurring precursor patterns across activity, location, hazard, and barrier failure.
- Prioritize sites, activities, and issues by concentration of SIF potential.
- Present all of the above through an interactive dashboard.
- Allow human review and validation of every AI-generated output.

### The product DOES NOT:

- Predict that a specific future accident or fatality will occur.
- Replace HSE professionals or their judgment.
- Autonomously authorize, halt, or otherwise control field operations.
- Claim to be an officially deployed OIL production system.
- Claim access to confidential OIL operational data unless such access is explicitly granted and documented.
- Fabricate, imply, or extrapolate OIL-specific statistics, incident counts, or performance figures.
- Make medical, legal, or regulatory-compliance determinations.
- Present prototype assumptions, synthetic data, or illustrative examples as verified OIL facts.
- Claim official IOGP certification or endorsement of any kind.
- Describe itself, in any document or demo, as "predicting fatalities" or "predicting accidents."

---

## 7. MVP / Prototype Constitution

The prototype must demonstrate one complete, working, end-to-end vertical slice:

```mermaid
flowchart LR
    S[Sample Safety Report] --> N[NLP Processing]
    N --> X[Signal Extraction]
    X --> P[SIF Potential Classification]
    P --> EV[Explainable Evidence]
    EV --> BF[Barrier Failure]
    BF --> LSR[IOGP LSR Mapping]
    LSR --> PAT[Recurring Pattern Example]
    PAT --> DASH[HSE Dashboard]
```

| Tier | Scope |
|---|---|
| **MUST HAVE** | Ingest one pasted/uploaded report; run NLP preprocessing and signal extraction; produce a SIF Potential classification with evidence; identify barrier status; map to at least one IOGP Life-Saving Rule; display all of this on a dashboard view; allow a human reviewer to accept/correct/reject the result. |
| **SHOULD HAVE** | A pre-loaded set of representative/synthetic reports demonstrating at least one recurring pattern; a site/activity ranking view by SIF-potential concentration; visible confidence indicators on AI outputs. |
| **NICE TO HAVE** | Trend-over-time view; multiple simultaneous LSR tags per report; a visual (even if non-functional) representation of role-based access; export of a report's structured record. |
| **OUT OF SCOPE FOR CURRENT PROTOTYPE** | Real integration with any OIL system; production-grade authentication/RBAC backend; large-scale model training or fine-tuning on real labelled data; multi-language support; mobile applications; anything requiring OIL-confidential data or infrastructure access. |

The prototype must prioritize a working end-to-end flow over enterprise-grade infrastructure. A fully working MUST HAVE tier, demoed live, outperforms a partially-working SHOULD HAVE or NICE TO HAVE tier for the purposes of this deadline.

---

## 8. AI / Safety Intelligence Principles

- **Contextual NLP, not keyword-only logic.** Detection must account for negation, context, and phrasing variation (Section 5, Principle 4). A keyword filter alone does not satisfy this constitution.
- **Hybrid rule + ML approach where appropriate.** Known, unambiguous safety relationships should be encoded as explicit rules; ambiguous or highly variable language should be handled by a learned model. Neither approach alone is treated as sufficient on its own.
- **Structured safety signals.** All AI output that feeds later stages (barrier analysis, LSR mapping, pattern discovery) must pass through the structured signal categories in Section 10, not remain as free-form model text.
- **Evidence extraction.** Every classification-producing component must also emit the specific evidence that produced its output, per Section 5, Principle 3.
- **Confidence / uncertainty handling.** AI outputs carry an explicit confidence indicator rather than being presented as certain. Low-confidence outputs should be visibly distinguished from high-confidence ones in every downstream document and UI.
- **False-positive awareness.** The system should be designed with the understanding that some reports will be flagged incorrectly, and that human review exists specifically to catch this.
- **False-negative awareness.** Given the asymmetric cost of missing a real SIF precursor versus raising an unnecessary review, the system should be tuned to disfavor silently dropping ambiguous cases, favoring visibility (with appropriate confidence labelling) over silence.
- **Human review.** No AI classification is final; see Section 5, Principle 2.
- **Traceability.** Every structured output must be traceable back to the original report text and, at the aggregate level, back to the individual reports that contributed to a pattern claim.
- **Deterministic domain rules where appropriate.** See Section 5, Principle 13. Specific model architecture choices belong in `08_AI_ARCHITECTURE`, not here.

---

## 9. SIF Potential Definition

**SIF Potential**, within this product, is an assessment of whether a reported situation — as described in the report's text — contained the potential for a serious injury or fatality, based on the hazard, exposure, and barrier-status evidence present in that report.

The following clarifications are binding on every other document:

- **Actual injury outcome does not automatically determine SIF Potential.** A report stating "no injury" can still carry HIGH SIF Potential if the underlying hazard-exposure-barrier combination was dangerous. A report describing a minor injury does not automatically carry HIGH SIF Potential if the underlying mechanism had no realistic path to a severe outcome.
- **A near miss can carry high SIF Potential.** Near-miss reports are a primary, not secondary, source of SIF Potential evidence, precisely because they capture dangerous situations before any actual harm occurs.
- **High SIF Potential requires contextual safety evidence** — a real hazard, confirmed or plausible exposure, and an identifiable barrier gap — not a single alarming-sounding word in isolation.
- **The engine must explain why it flagged the report.** A SIF Potential output with no accompanying evidence is treated as an incomplete, non-compliant output under this constitution (Section 5, Principle 3).

### Actual Outcome vs. Potential Consequence

| | Actual Outcome | Potential Consequence |
|---|---|---|
| **What it describes** | What really happened to a person, as stated in the report. | What could reasonably have happened, given the hazard-exposure-barrier combination present. |
| **Timeframe** | Backward-looking; already occurred. | Forward-looking at the moment of the report; a "what if" grounded in the actual evidence present. |
| **Can be absent** | Yes — many reports state no injury occurred. | No — a real hazard-exposure combination always has *some* potential consequence, even if low. |
| **Drives SIF Potential?** | No, not directly. | Yes — this is the primary basis for the SIF Potential assessment. |

---

## 10. Safety Signal Taxonomy

The following are the conceptual signal categories the system may extract from a report. These are conceptual categories, not a database schema — concrete field names, types, and storage belong in `09_DATABASE_DESIGN`.

| Category | What It Captures |
|---|---|
| Hazard | The energy source or danger present (e.g. confined space, live equipment, height). |
| Activity | The task being performed when the observation occurred. |
| Location | The site or specific area where the event occurred. |
| Equipment | The machine, tool, or asset involved. |
| Worker Exposure | Whether and how a person was in contact with, or proximate to, the hazard. |
| Unsafe Act | A person's action that increased risk. |
| Unsafe Condition | An environmental or equipment state that increased risk. |
| Safety Control | Any named measure intended to reduce risk (procedure, PPE, permit, etc.). |
| Barrier | A control considered specifically in its role of standing between a hazard and a consequence. |
| Barrier Status | Whether a given barrier was present, verified, missing, incomplete, failed, or bypassed — see Section 11. |
| Critical Control Failure | A failure specifically involving a control identified as critical to preventing a severe outcome. |
| Context / Negation | Whether a control or action is asserted as present or explicitly stated as absent/incomplete. |
| Potential Consequence | The plausible severe outcome implied by the hazard-exposure-barrier combination. |
| Actual Outcome | The real, stated result of the event (injury, damage, or none). |
| Intervention | Any action taken to stop or correct the situation once noticed (e.g. "supervisor stopped the work"). |

---

## 11. Barrier Philosophy

A **barrier** is a control evaluated specifically in its role of standing between a hazard and a person. Not every named safety control is automatically treated as a "barrier" in a given report — a control is a barrier *relative to* a specific hazard-consequence pathway it is meant to interrupt. This distinction must be preserved: the system should not claim every mentioned control is a barrier without an identifiable hazard it is protecting against.

Barrier status is recorded using the following six mutually-exclusive states — this is the single canonical taxonomy for the entire project; no document may define a different count or a different set of state names:

| State | Meaning |
|---|---|
| Present / Verified | The control is mentioned as existing/available **and** nothing in the text contradicts it having been effective — in free-text safety narratives, a control that is stated as done ("gas test completed," "isolation confirmed") is treated as both present and verified, since reporters rarely distinguish "it was there" from "it was checked" in separate clauses. Splitting this into two states was found, in practice, to add taxonomy complexity without adding extractable signal from real report text. |
| Missing | The control was required but never established at all. |
| Incomplete | The control was partially applied but not fully completed. |
| Failed | The control existed and was applied but did not hold or work as intended. |
| Bypassed | The control existed but was deliberately overridden or disabled. |
| Unknown | The report does not provide enough information to determine status. |

**Revision note (Change Management, Section 20):** An earlier draft of this constitution separated `Present` and `Verified` into two states (seven total). That draft was superseded by the six-state model above after implementation across `05`, `08`, `09`, `10`, and `14` showed the split was not observable from typical free-text phrasing and was never actually implemented as distinct states anywhere downstream. The six-state model is the one authoritative model, effective immediately; any reference elsewhere in this document set to a seven-state or five-state barrier taxonomy is an error to be corrected to match this section.

Barrier status matters to SIF Potential assessment because the gap between a hazard and a severe consequence is, in almost every real case, exactly the barrier that should have — but didn't — close it. A HIGH SIF Potential judgment should, wherever possible, be traceable to a specific barrier state rather than to hazard language alone.

---

## 12. IOGP Life-Saving Rules

The IOGP Life-Saving Rules are a fixed, externally-defined taxonomy (nine rules) identifying the activity categories most associated with fatalities in the Oil & Gas industry. This product's role is to **map** relevant reported situations to the applicable rule(s) — not to define, modify, or reinterpret the rules themselves.

This mapping must be **evidence- and context-based**: it should be produced from the combination of extracted hazard, activity, and barrier signals (Sections 10–11) for a given report, not from matching a single keyword against a rule's name. A report can validly map to more than one rule where the underlying situation genuinely spans more than one category.

This product is **not** an official OIL implementation of the IOGP framework and **is not** an IOGP-certified tool of any kind. Any document, dashboard label, or demo statement implying official IOGP certification or endorsement violates this constitution.

---

## 13. Pattern Discovery Philosophy

This product maintains a clear conceptual separation between two different questions:

- **Individual report analysis** asks: *"Why is this specific report potentially serious?"* — answered by the SIF Potential Engine, Explainability, and Barrier Failure Analysis stages, for one report at a time.
- **Cross-report pattern analysis** asks: *"What precursor, activity, location, or barrier failure is recurring across many reports?"* — answered by the Recurring Pattern Discovery stage, operating over the accumulated report history.

These are genuinely different outputs and must not be conflated in any document or UI: a single alarming report is not itself a "pattern," and a named pattern is not reducible to any one report within it.

Pattern discovery should consider multiple dimensions together — frequency, recurrence over time, activity, location/site, hazard type, and barrier-failure type — and, where time-series data is available, trend direction. **Frequency alone must not be treated as equivalent to risk.** A pattern that occurs less often but concentrates around a higher-severity hazard-barrier combination may warrant more attention than a more frequent but lower-severity pattern. This nuance must be preserved wherever pattern results are ranked or displayed.

---

## 14. HSE Prioritization Philosophy

This product provides **decision support**, not decision authority. Its role in prioritization is to help HSE identify:

- Individual reports with high SIF potential.
- Recurring precursor patterns worth investigating.
- Barrier-failure hotspots (specific controls failing repeatedly, and where).
- High-priority activities and sites, ranked by concentration of SIF potential rather than raw report volume.
- Areas that appear to warrant review or intervention based on the above.

**Final safety decisions, interventions, and any action affecting field operations remain the sole responsibility of authorized HSE personnel at all times.** No part of this product's output should be described, in any document or demo, as automatically triggering an operational action.

---

## 15. Data & Dataset Principles

All data used anywhere in this project must be classified into exactly one of the following categories, and that classification must be visible wherever the data is used:

| Category | Definition | Usage Rule |
|---|---|---|
| **A. Official OIL data** | Real, OIL-provided operational data. | Requires explicit, documented authorized access. Must not be assumed to exist for this prototype unless such access is actually granted. |
| **B. Public datasets** | Published, non-OIL safety/incident datasets (e.g. from research literature). | May be used for prototype experimentation and model development, always cited to their actual source. |
| **C. Synthetic / representative demo data** | Fictional reports created to demonstrate the product's behavior. | Allowed for demonstration; must be visibly labelled as representative/synthetic wherever displayed. |
| **D. Manually labelled prototype data** | A small set of example reports labelled by the team for testing. | Allowed if the labelling method and labeller are explicitly documented; must not be presented as expert-validated ground truth unless it genuinely is. |

**Synthetic, public, or non-OIL data must never be represented as actual OIL operational data**, in any document, demo, or conversation with judges or stakeholders.

---

## 16. Claims & Evidence Policy

This policy governs every claim made in the PPT, README, dashboard, other documentation, live demo, and code comments, without exception.

**Never claim, unless verified and supported by actual evidence:**

- Production deployment at OIL.
- Validated OIL-specific model accuracy, precision, recall, or any other performance metric.
- Access to confidential OIL data.
- Official OIL endorsement of the product.
- Official IOGP certification of the product.
- Specific business or safety impact numbers (e.g. "reduces incidents by X%," "saves N lives").

**Any prototype-stage metric that is shown must be explicitly labelled as one of:**

- *Prototype result*
- *Experimental result*
- *Illustrative*
- *Synthetic-data result*

An unlabelled number in any document or demo asset is treated as a defect in that document, to be corrected before it is shown to anyone outside the team.

---

## 17. Research & External Knowledge Policy

External research, published papers, industry standards (including the IOGP Life-Saving Rules framework), and market research are used to **inform design decisions** — they justify why an approach is reasonable, not what OIL specifically does or has.

Relevant research areas for this project include: PSIF/SIF identification methods, NLP applied to safety/incident reports, near-miss classification, incident/pattern extraction from free text, barrier and control analysis, the IOGP Life-Saving Rules framework, and the broader HSE-software landscape.

**Rule:** a finding from external research may be cited to justify *why our design choice is reasonable*. It must never be restated as an *OIL-specific fact* or as *our own prototype's measured result*, unless the source itself is explicitly about OIL or our own measurement explicitly reproduces it. Every citation of external research in any document should make clear whether it is general domain-knowledge support or a literal OIL-specific claim (it should almost always be the former).

---

## 18. Architecture Governance

The following architectural principles are binding on `07_SYSTEM_ARCHITECTURE` and `08_AI_ARCHITECTURE`; this section states the principles only — the actual component diagrams, technology choices, and interface contracts belong in those documents, not here.

- **Modular components.** NLP preprocessing, signal extraction, SIF reasoning, explainability, barrier analysis, LSR mapping, pattern discovery, and the dashboard are separate components with defined interfaces between them.
- **Clear separation of concerns.** No single component should silently take on another component's responsibility (e.g. the dashboard must not perform its own ad hoc SIF classification independent of the SIF Potential Engine).
- **APIs / interfaces between major components.** Each component's inputs and outputs are explicit and documented, enabling independent development and testing.
- **Replaceable AI models.** The specific model or technique used inside any AI component should be swappable without requiring changes to the components around it.
- **Testability.** Each component should be testable in isolation, using representative or synthetic inputs where real data is unavailable.
- **Observability.** The system should make it possible to see what happened at each pipeline stage for a given report, supporting the traceability principle in Section 8.
- **Security.** Access to components and data follows the principles in `11_SECURITY_ARCHITECTURE`, itself governed by Section 15 (data classification) and Section 5, Principle 11 (data minimization).
- **Maintainability.** Prefer clear, well-documented implementations over clever but opaque ones, especially in safety-reasoning components.
- **Prototype simplicity.** Under the current deadline, architectural elegance that delays a working end-to-end demo is deprioritized — see Section 21 and Section 24.

---

## 19. Documentation Governance

| Document | Authoritative For |
|---|---|
| `01_PROJECT_CONSTITUTION` | Principles, scope, boundaries, and claims policy governing every other document. |
| `02_PRODUCT_BLUEPRINT` | Product capabilities and feature-level definition, consistent with this constitution. |
| `03_PROBLEM_STATEMENT` | The official PS requirements, kept distinct from our own proposed design choices. |
| `04_MARKET_RESEARCH` | Landscape/competitive context, subject to the Research & External Knowledge Policy (Section 17). |
| `06_TECHNICAL_REQUIREMENTS` | Functional and non-functional requirements derived from this constitution and the product blueprint. |
| `07_SYSTEM_ARCHITECTURE` | System components, their responsibilities, and how they connect. |
| `08_AI_ARCHITECTURE` | AI/NLP model choices, pipeline implementation details, and AI-specific design decisions. |
| `09_DATABASE_DESIGN` | The concrete data model and schema implementing the taxonomies defined here. |
| `10_API_SPECIFICATION` | API contracts between components and to the frontend. |
| `11_SECURITY_ARCHITECTURE` | Authentication, authorization, encryption, and audit-logging design. |
| `12_UI_UX_DESIGN` | Dashboard and interface behavior and layout. |
| `13_DEPLOYMENT` | Infrastructure and deployment approach for the prototype and any future environment. |
| `14_TESTING_STRATEGY` | Validation and testing approach across components. |
| `15_ROADMAP` | Implementation sequencing and future-enhancement planning. |
| `16_DOCUMENT_CONSISTENCY_AUDIT` | Verifying that all documents remain consistent with this constitution and each other. |

**No lower-level document may silently contradict this constitution.** Where a document must deviate (for a good, specific reason), the deviation must be flagged explicitly in that document and resolved through Section 20.

---

## 20. Change Management

When a technical or product decision appears to conflict with this constitution:

1. **Identify the conflict** explicitly — state which principle, boundary, or definition is in tension with the proposed decision.
2. **Determine whether the constitution should change**, or whether the proposed decision should be adjusted to fit the constitution instead. Changing the constitution should be rare and deliberate, not a convenience.
3. **Update affected documents** so that every document referencing the changed area reflects the same, single version of the truth.
4. **Run a consistency check** (see `16_DOCUMENT_CONSISTENCY_AUDIT`) across the full document set after any constitutional change.
5. **Record the decision** — what changed, why, and when — so the team has a memory of why the current state is what it is, rather than relying on recollection under deadline pressure.

Uncontrolled architecture or scope drift — a document quietly diverging from this constitution without going through the above — is treated as a defect to be corrected, not a minor inconsistency to be tolerated.

---

## 21. Prototype Deadline Rules

The team has a working prototype due tomorrow morning. Under this constraint, the following rules apply and take precedence over general software-engineering best practice where the two conflict:

- **Prioritize end-to-end functionality** over the completeness of any single stage. A pipeline where every stage runs, even simply, beats a pipeline where one stage is sophisticated and the rest are missing.
- **Prioritize demonstrable core intelligence** — SIF Potential + Evidence + Barrier + LSR mapping on at least one real, live-processed report — over supporting infrastructure.
- **Avoid unnecessary enterprise complexity.** Do not build multi-service deployment, full RBAC backends, or production-grade infrastructure for tomorrow's demo; represent these visually or conceptually if needed (Section 7).
- **Prefer working simple implementations over unfinished sophisticated ones.** A rule-based barrier check that works beats a half-trained model that doesn't.
- **Use modular code** so today's simple implementation of any stage can be replaced later without rewriting the stages around it (Section 18).
- **Mock external integrations where required**, and label every mock clearly in code comments and in the UI.
- **Never present a mocked or synthetic result as measured model performance.** This rule is absolute and follows directly from Section 16 — deadline pressure is not an exception to the Claims & Evidence Policy.

---

## 22. Definition of Done

For the current prototype milestone, "done" means all of the following are true simultaneously:

- The application runs without manual workarounds.
- A sample safety report can be ingested (pasted or uploaded).
- NLP processing executes on that report.
- Safety signals are extracted and visible.
- A SIF Potential classification is produced.
- Evidence for that classification is displayed.
- Barrier information (status per identified barrier) is shown.
- At least one IOGP Life-Saving Rule mapping is shown, with reasoning.
- A recurring-pattern example is demonstrated (using representative/synthetic multi-report data if needed, clearly labelled as such).
- An HSE prioritization/dashboard view is visible and reflects the above.
- Errors are handled gracefully rather than crashing the demo.
- All demo/synthetic data is clearly and visibly labelled as such, per Section 15.
- A README with setup instructions exists and has been verified to actually work from a clean environment.

A prototype missing any of the above is not yet "done," regardless of how polished the completed parts look.

---

## 23. Risks & Guardrails

| Risk | Guardrail |
|---|---|
| False positives (AI flags a report HSE disagrees with) | Human-in-the-loop review (Section 5, Principle 2) catches this before any action is taken; false positives are treated as an expected, manageable cost, not a system failure. |
| False negatives (AI misses a real precursor) | Tune toward recall over precision for ambiguous cases (Section 8); never silently drop a low-confidence signal — surface it with its confidence level instead. |
| Insufficient labelled data | Rely on the hybrid rule + ML approach (Section 8) and human-review feedback loop rather than assuming a large labelled dataset exists; document this limitation openly. |
| Domain ambiguity (unclear or unusual report wording) | Default to lower confidence and explicit "Unknown" states (Section 11) rather than forcing a confident-sounding but unjustified classification. |
| Keyword-only detection creeping in | Any detection logic must handle the negation/context test in Section 5, Principle 4 before it is accepted into the pipeline. |
| Data leakage (evaluation data overlapping training data) | Keep any labelled example sets clearly partitioned and documented in `14_TESTING_STRATEGY`. |
| Hallucinated explanations (evidence that doesn't match the source text) | Explainability output must be extracted from, or directly traceable to, the actual report text — never independently generated prose describing the model's "reasoning" without a text anchor. |
| Fabricated metrics | Governed absolutely by Section 16; any unlabelled number is a defect. |
| Over-reliance on AI | Structurally prevented by Section 5, Principle 2 and Section 14 — the product is decision support, not decision authority, by design, not by disclaimer alone. |
| Privacy / security gaps | Governed by Section 5, Principle 11 and `11_SECURITY_ARCHITECTURE`; data minimization and access control are default, not optional. |
| Prototype assumptions mistaken for production claims | Governed absolutely by Sections 15 and 16; every demo asset and document must carry the appropriate label. |

---

## 24. Decision-Making Rules

When multiple reasonable implementation choices exist, resolve the choice using this priority order, highest first:

1. **SIH PS alignment** — does this choice serve what the official problem statement actually asks for?
2. **Safety correctness** — does this choice risk hiding or misrepresenting a real safety signal?
3. **Explainability** — does this choice preserve the ability to show evidence behind every output?
4. **End-to-end prototype functionality** — does this choice help the full pipeline run, live, tomorrow?
5. **Simplicity** — is this the simplest approach that satisfies the above four?
6. **Maintainability** — can the team understand and modify this after the hackathon?
7. **Extensibility** — does this choice avoid closing off reasonable future improvements?
8. **Performance** — is this choice fast enough for a live demo?
9. **Enterprise-scale optimization** — lowest priority; **do not optimize for enterprise scale at the expense of having a working demonstration tomorrow.**

Where two choices tie at a given priority level, move to the next level down to break the tie.

---

## 25. Final Product Constitution Summary

**North Star:**

> Turn unstructured safety reports into explainable SIF intelligence that helps HSE understand what happened, why it matters, which barriers are involved, which Life-Saving Rule applies, what patterns are recurring, and where intervention should be prioritized.

Every document, every line of code, and every claim made about this product should trace back, without contradiction, to this constitution.