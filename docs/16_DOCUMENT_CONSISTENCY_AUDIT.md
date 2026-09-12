# 16_DOCUMENT_CONSISTENCY_AUDIT.md

**Document Status:** Authoritative record of the cross-document consistency audit for the OIL Safety Intelligence Platform document set (`01`–`15`, plus `ARCHITECTURE_DIAGRAMS_MERMAID.md`).
**Audit Method:** Every finding below was confirmed by direct `grep`/text search against the actual file contents at the cited line numbers — not inferred, summarized, or reconstructed from memory. Every fix listed as "Applied" was verified post-fix by re-running the same search and confirming a clean (empty) result.
**Supersedes:** An earlier version of this document contained a substantial number of fabricated findings (invented quotes, non-existent table/column names, and misattributed line citations). That version has been fully replaced. Section 6 of this document explains what was wrong with it and why, for transparency and so the same mistake is not repeated.
**SIH Problem Statement ID:** SIH26165

---

## 1. Audit Scope & Method

This audit checked the 16 project documents (`01_PROJECT_CONSTITUTION.md` through `15_ROADMAP.md`, plus `ARCHITECTURE_DIAGRAMS_MERMAID.md`) for:
- Contradictions between documents on the same fact, ID, enum, or schema element.
- Deviations from `01_PROJECT_CONSTITUTION.md`, which is the project's governing source of truth.
- Gaps — capabilities referenced as if defined elsewhere, but not actually defined anywhere.
- Unsupported or overstated claims that violate the Constitution's evidence/claims policy (Section 16 of `01`).

Every finding is stated with the **exact file and line(s)** where it was found, and every fix applied is stated precisely enough to be independently re-verified with a single `grep` command.

---

## 2. Fixes Applied In This Pass

### FIX-01 — Barrier-state taxonomy: Constitution vs. implementation mismatch
**Was:** `01_PROJECT_CONSTITUTION.md` §11 defined a **7-state** model (`Present`, `Verified`, `Missing`, `Incomplete`, `Failed`, `Bypassed`, `Unknown` — Present and Verified listed as separate states). No downstream document (`05`, `08`, `09`, `10`, `14`) ever actually implemented that split; all of them used a **6-state** model with `Present`/`Verified` combined into one state. This was a real Constitution-vs-implementation conflict that had gone unnoticed because nothing had cross-checked `01` against the schema/AI/testing documents directly.
**Fix:** `01_PROJECT_CONSTITUTION.md` §11 rewritten to formally adopt the 6-state model as canonical, with an explicit revision note explaining why (the Present/Verified split is not observable from typical free-text report phrasing, and was never implemented). The canonical 6 states are now: `PRESENT_VERIFIED`, `MISSING`, `INCOMPLETE`, `FAILED`, `BYPASSED`, `UNKNOWN`.
**Verification:** `grep -rn "'Present'" *.md` (as a state distinct from Verified) returns no matches outside this historical note.

### FIX-02 — Barrier enum literal-string drift (`09`, `10` used verbose compound names)
**Was:** `09_DATABASE_DESIGN.md` and `10_API_SPECIFICATION.md` used `INCOMPLETE_COMPROMISED`, `MISSING_NOT_IMPLEMENTED`, `FAILED_DEGRADED`, `BYPASSED_DEFEATED`, `UNKNOWN_UNVERIFIED` — the same six concepts as `05`/`08`/`14`, but different literal enum strings.
**Fix:** Standardized all barrier-state literals project-wide to the simple canonical set: `PRESENT_VERIFIED`, `MISSING`, `INCOMPLETE`, `FAILED`, `BYPASSED`, `UNKNOWN`. Applied to `09`, `10`, and two leftover instances found in `12_UI_UX_DESIGN.md` (line 383, a dropdown mockup) and `14_TESTING_STRATEGY.md` (lines 195–326, a test-case table).
**Verification:** `grep -rn "INCOMPLETE_COMPROMISED\|MISSING_NOT_IMPLEMENTED\|FAILED_DEGRADED\|BYPASSED_DEFEATED\|UNKNOWN_UNVERIFIED" *.md` returns no matches.

### FIX-03 — "5-state" miscount (should be 6-state) — widespread
**Was:** Sixteen separate lines across `07`, `08`, `09`, `10`, `11`, `12`, `13`, `14`, `15`, and `ARCHITECTURE_DIAGRAMS_MERMAID.md` referred to the barrier taxonomy as "5-state" / "5 states." The actual implemented (and now canonical) model has always had 6 states — the miscount likely originated from informally dropping `UNKNOWN` when describing the model in prose. Two diagram labels in `ARCHITECTURE_DIAGRAMS_MERMAID.md` (lines 70, 157) also spelled out only 5 of the 6 state names explicitly, omitting `Unknown` and shortening `Present/Verified` to just `Verified`.
**Fix:** All "5-state"/"5 states" text changed to "6-state"/"6 states." Both diagram labels updated to list all 6 canonical names.
**Verification:** `grep -rniE "5-state|5 state" *.md` returns no matches (outside this document's own historical description).

### FIX-04 — `15_ROADMAP.md`'s "Bow-Tie Barrier Intelligence" invented a second, conflicting barrier taxonomy
**Was:** `15_ROADMAP.md` (lines 195, 222, 833, 874, 986, 1098) described a *different* 5-state taxonomy (`FUNCTIONAL`, `COMPROMISED`, `FAILED`, `MISSING`, `UNKNOWN`) under the same requirement ID (`AI-005`) already used elsewhere for the canonical 6-state model. This meant `AI-005` had two incompatible definitions depending on which document you read.
**Fix:** Reframed "Bow-Tie Barrier Intelligence" as a **visualization** of the canonical 6-state model (a bow-tie diagram rendering of `PRESENT_VERIFIED`/`MISSING`/`INCOMPLETE`/`FAILED`/`BYPASSED`/`UNKNOWN`), not a competing taxonomy. `AI-005` now has one meaning project-wide.
**Verification:** `grep -rn "FUNCTIONAL.*COMPROMISED.*FAILED.*MISSING.*UNKNOWN" *.md` returns no matches.

### FIX-05 — Requirement-ID drift: `FR-003` used for two different requirements
**Was:** `06_TECHNICAL_REQUIREMENTS.md` (the authoritative source) defines `FR-003` = "Input Validation & Error Handling" and `AI-004` = "SIF Potential Assessment Engine." But `09_DATABASE_DESIGN.md` (line 1634), `11_SECURITY_ARCHITECTURE.md` (line 524), and `12_UI_UX_DESIGN.md` (line 462) all independently used `FR-003` to mean the SIF Potential Engine instead of `AI-004` — and, having "used up" `FR-003` for that, each document then separately mislabeled `AI-004` as a distinct, unnumbered concept called "Outcome Blindness."
**Fix:** All three documents corrected: `FR-003` restored to its correct meaning (or removed where it didn't belong in that context), and the SIF engine consistently labelled `AI-004` everywhere, including its outcome/potential-decoupling behavior as part of the same requirement (not a separate ID). Also corrected the same underlying error, plus knock-on mislabeling of `AI-005`/`AI-006`/`AI-007`, in `10_API_SPECIFICATION.md` (traceability table) and `14_TESTING_STRATEGY.md` (traceability table).
**Verification:** `grep -rn "FR-003.*SIF\|FR-003.*Causal\|FR-004.*Barrier\|FR-005.*IOGP\|FR-006.*Pattern" *.md` returns no matches.

### FIX-06 — `15_ROADMAP.md` had its own self-consistent but `06`-incompatible AI-numbering scheme
**Was:** Independently of FIX-05, `15_ROADMAP.md` used a *different* offset numbering for AI capabilities from `AI-003` onward: its `AI-002` meant Safety Signal Extraction (should be `AI-003`), its `AI-003` meant the SIF Potential Engine (should be `AI-004`), its `AI-004` meant Span-Level Explainability (should be `AI-008`), and its `AI-008` meant HSE Prioritization scoring (not an AI-numbered item in `06` at all — `06` places this under `UX-004`). This was a whole-document, self-consistent-but-wrong numbering, used in roughly 26 locations throughout the file.
**Fix:** All affected IDs in `15_ROADMAP.md` renumbered to match `06`'s canonical scheme: `AI-002→AI-003`, `AI-003→AI-004`, `AI-004→AI-008`, `AI-008→UX-004`. `AI-001`, `AI-005`, `AI-006`, `AI-007` were already correct and left unchanged.
**Verification:** Spot-checked all renumbered lines (dependency columns included) post-fix; no leftover placeholder tokens or unconverted instances remain.

### FIX-07 — `15_ROADMAP.md`: `FR-005` used for a requirement not in `06`; `SEC-001`/`SEC-002` meanings reversed; `FR-003` reused for a third, unrelated requirement
**Was:**
- `15_ROADMAP.md` used `FR-005` to mean "Executive & Operational Dashboard" — `06` has no `FR-005`; the dashboard is `UX-001` in `06`.
- `15_ROADMAP.md` used `SEC-001` for "Immutable Audit Trail Logging" and `SEC-002` for "PII Redaction" (5 occurrences) — this is the **reverse** of `06`'s canonical mapping (`SEC-001` = PII Scrubbing, `SEC-002` = Audit Trail Immutability), which `10` and `11` both use correctly.
- `15_ROADMAP.md` also used `FR-003` a second time (independently of FIX-05) to mean "Full-Text & Semantic Search" — a third, different meaning for the same ID. `06` already has `UX-005` ("Multi-Dimensional Filtering & Search") for this exact capability.
**Fix:** `FR-005`→`UX-001`; `SEC-001`↔`SEC-002` swapped to match `06`; `FR-003` (search context only)→`UX-005`.
**Verification:** `grep -n "SEC-001\|SEC-002" 15_ROADMAP.md` now shows PII references under `SEC-001` and audit references under `SEC-002`, matching `06`, `10`, `11`.

### FIX-08 — Two legitimate new requirements in `15_ROADMAP.md` were never registered in `06`
**Was:** `15_ROADMAP.md` defines `FR-004` (Exportable Audit Dossier / PDF export) and `FR-006` (Email/Alert Notification Engine, P2/post-H0) as real, distinct, sensibly-numbered requirements — but `06_TECHNICAL_REQUIREMENTS.md`, which is supposed to be the complete authoritative register, never listed them. This wasn't a contradiction so much as an incompleteness in the source of truth.
**Fix:** Added `FR-004` and `FR-006` to `06`'s master requirements table, each tagged `[registered during consistency remediation]` and cross-referenced to `15_ROADMAP.md` as their origin.
**Verification:** `grep -n "FR-004\|FR-006" 06_TECHNICAL_REQUIREMENTS.md` now returns both.

### FIX-09 — SIF Potential enum literal-value drift
**Was:** The canonical enum (used consistently in `05`, `06`, `09`, `10`) is `YES` / `NO` / `REVIEW`. Three other places used different literal tokens for the same concept: `08_AI_ARCHITECTURE.md` line 510 (a JSON payload example) used `"SIF_YES"`; `15_ROADMAP.md` line 257 stated the engine "emits `SIF_YES`, `SIF_POTENTIAL`, or `SIF_NO`"; and two further `15_ROADMAP.md` lines (193, 416) used `YES`/`POTENTIAL`/`NO` instead of `YES`/`REVIEW`/`NO`.
**Fix:** All four corrected to the canonical `YES` / `NO` / `REVIEW` set. (Mermaid diagram **node IDs** like `SIF_YES` in `08` lines 330/740/743 were deliberately left unchanged — these are internal diagram-node identifiers, not asserted data values; the visible node label text already correctly reads "SIF Potential: YES/NO".)
**Verification:** `grep -rn "SIF_POTENTIAL\|\`POTENTIAL\`" *.md` returns no matches.

### FIX-10 — Missing API contract: batch report ingestion
**Was:** `06`, `12`, and `15` all treat CSV/batch report ingestion as a P0 capability (`FR-002`), and `10_API_SPECIFICATION.md`'s own traceability table referenced a caller ("Batch CSV Ingestion Script") — but no `POST /reports/batch` endpoint, request schema, or response schema was actually defined anywhere in `10`.
**Fix:** Added a full new Section 8b to `10_API_SPECIFICATION.md` defining `POST /api/v1/reports/batch`, covering both `multipart/form-data` (CSV) and `application/json` (array) request bodies, a `207 Multi-Status` response contract with per-row success/failure reporting, and validation rules (100-row cap for the H0 prototype; larger async batch processing explicitly marked `[FUTURE ENHANCEMENT]`).
**Verification:** `grep -l "POST /api/v1/reports/batch" *.md` now includes `10_API_SPECIFICATION.md`.

### FIX-11 — Naming drift: `audit_logs` vs. `audit_events`; `char_start`/`char_end` vs. `start_offset`/`end_offset`
**Was:** `09`, `10`, and `11` consistently use table name `audit_events` and column names `start_offset`/`end_offset`. `15_ROADMAP.md` (5 occurrences) used `audit_logs`, and (5 occurrences) used `char_start`/`char_end` for the same concepts. `ARCHITECTURE_DIAGRAMS_MERMAID.md` line 288 also referenced a `./data/audit_logs` volume path.
**Fix:** All instances in `15_ROADMAP.md` and `ARCHITECTURE_DIAGRAMS_MERMAID.md` renamed to match `09`/`10`/`11`: `audit_events`, `start_offset`, `end_offset`.
**Verification:** `grep -rn "audit_logs\|char_start\|char_end" *.md` returns no matches.

---

## 3. Findings Investigated And Confirmed Not To Be Issues

These were checked and found to already be correct, or lower-priority than initially suspected — listed here so they are not re-investigated unnecessarily in a future pass:

| Item | Investigated | Result |
|---|---|---|
| `data_sources` table | Checked whether it exists in `09_DATABASE_DESIGN.md` | It exists in full (line ~631). Not a gap. |
| Recurring-pattern and prioritization table names | Checked whether `09` and `10` disagree on table names | Both already use `recurring_patterns` and `hse_prioritizations` consistently. No conflict. |
| `actual_outcome_severity` enum | Checked whether `09` and `10` disagree on enum values | Both already use `NO_INJURY_NEAR_MISS`, `FIRST_AID`, `MEDICAL_TREATMENT`, `LOST_TIME_INJURY`, `FATALITY`, `UNKNOWN`. No conflict. |
| `95.5%` SIF recall figure (`14_TESTING_STRATEGY.md`) | Checked whether this figure is presented as validated real-world performance | It is already labelled `[PROTOTYPE ASSUMPTION]` with an explicit caveat that it is a synthetic-benchmark result (MVD-60), not OIL production data. Compliant with Constitution §16. The same figure's second appearance (traceability table) was missing the label — this has now been added for completeness. |
| `SEC-001`/`SEC-002` in `06`, `10`, `11` | Checked whether these three documents disagree with each other | They already agree (`SEC-001`=PII, `SEC-002`=Audit). The disagreement was isolated to `15_ROADMAP.md` (see FIX-07). |
| Redis/Celery framing in `07_SYSTEM_ARCHITECTURE.md` | Checked whether `07` claims Celery/Redis is required for the H0 prototype | `07` already explicitly scopes background job processing as in-memory for the prototype, evolving to Celery/Redis only in a future production phase. Not a contradiction. |

---

## 4. Open Items Not Fully Re-Verified In This Pass

For transparency: the following were flagged in an earlier draft of this audit and have **not** been independently re-verified line-by-line in this pass, given the scope of the rest of the remediation. They should be spot-checked before being considered closed:

- Color-token naming consistency between `12_UI_UX_DESIGN.md`'s design-token table and any actual component code (not applicable yet, since no frontend code exists in this document set).
- Test-coverage percentage figures in `14_TESTING_STRATEGY.md` vs. `15_ROADMAP.md` (an earlier draft claimed an 80% vs. 100% mismatch; this specific claim was not re-confirmed against exact line numbers in this pass).

---

## 5. Post-Fix Verification Summary

All checks below were re-run after the fixes above were applied, against the corrected files:

| Check | Command (representative) | Result |
|---|---|---|
| No wrong `FR-00X` labels for SIF/Barrier/LSR/Pattern | `grep -rn "FR-003.*SIF\|FR-004.*Barrier\|FR-005.*IOGP\|FR-006.*Pattern" *.md` | Clean |
| No verbose/duplicate barrier enum names | `grep -rn "INCOMPLETE_COMPROMISED\|MISSING_NOT_IMPLEMENTED\|FAILED_DEGRADED\|BYPASSED_DEFEATED\|UNKNOWN_UNVERIFIED" *.md` | Clean |
| No "5-state" miscounts | `grep -rniE "5-state|5 state" *.md` | Clean |
| No stray SIF enum tokens | `grep -rn "SIF_POTENTIAL\|\`POTENTIAL\`" *.md` | Clean |
| No `audit_logs` / `char_start` / `char_end` leftovers | `grep -rn "audit_logs\|char_start\|char_end" *.md` | Clean |
| Batch ingestion endpoint exists | `grep -l "POST /api/v1/reports/batch" *.md` | Present in `10_API_SPECIFICATION.md` |
| `06` registers all requirement IDs used elsewhere | Manual cross-check of `FR-004`, `FR-006` | Present in `06_TECHNICAL_REQUIREMENTS.md` |

---

## 6. Why The Previous Version Of This Document Was Retired

An earlier version of `16_DOCUMENT_CONSISTENCY_AUDIT.md` was reviewed and found to contain a significant number of fabricated specifics presented with false confidence (exact line numbers and verbatim quotes for content that does not exist in the source files). Concretely, on independent re-verification:

- Several claimed table/column names (`pattern_clusters`, `vw_triage_queue`, `char_start_offset`, `char_end_offset`) **do not appear anywhere** in the actual document set.
- A claimed barrier-taxonomy conflict attributed to `05` and `08` was traced to a taxonomy that **does not appear in either file** — the real (much narrower) version of this issue was in `15_ROADMAP.md` only, and involved a genuine Constitution-vs-implementation gap the old audit never checked for (see FIX-01/04 above).
- Four of five "unsupported claim" citations (an ODBC integration claim, a "first AI platform" claim, a "35% risk reduction" claim, and a "zero false negatives" claim) **do not exist anywhere** in the document set.
- A claimed `09`-vs-`10` conflict on the `actual_outcome_severity` enum was false — both files already agreed.

This does not mean the old audit was entirely worthless — three of its findings (the `FR-003` requirement-ID drift, the SIF enum token drift, and the missing batch endpoint) were real and are reflected in FIX-05 and FIX-09/10 above. But roughly half of its specific citations could not be substantiated against the actual files, which makes it unsafe to use as a checklist without independent re-verification of every line. This version replaces it in full, with every claim traceable to an exact, re-checkable location in the current files.

---

## 7. Go / No-Go Assessment

**Status: Ready to proceed to GitHub repository setup**, conditional on the fixes in Section 2 (all of which have been applied to the copies of the files accompanying this audit).

Before merging to a shared `main` branch, it is still recommended that a human maintainer:
1. Do a final read-through of `10_API_SPECIFICATION.md` Section 8b (the newly added batch endpoint) to confirm it matches actual intended frontend behavior for `BulkUploadModal.tsx`.
2. Resolve the two open items in Section 4 above.
3. Treat `01_PROJECT_CONSTITUTION.md`'s revised §11 (six-state barrier model) as the model going forward — any future document must not reintroduce a seven-state or five-state variant.
