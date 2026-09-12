# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to a documentation-first versioning scheme while in
its pre-implementation phase (semantic versioning will apply once code ships).

## [Unreleased]

### Planned
- H0 hackathon prototype implementation per `docs/15_ROADMAP.md`.

## [0.2.0] — Documentation Consistency Remediation

### Fixed
- `01_PROJECT_CONSTITUTION.md`: Barrier-state taxonomy formally reduced from a
  never-implemented 7-state model to the actually-implemented, now-canonical
  6-state model (`PRESENT_VERIFIED`, `MISSING`, `INCOMPLETE`, `FAILED`,
  `BYPASSED`, `UNKNOWN`).
- `09_DATABASE_DESIGN.md`, `10_API_SPECIFICATION.md`, `12_UI_UX_DESIGN.md`,
  `14_TESTING_STRATEGY.md`: Standardized barrier enum literal values (removed
  verbose compound variants).
- Project-wide: corrected "5-state" miscount to "6-state" (16 locations).
- `15_ROADMAP.md`: Resolved a self-consistent-but-incompatible AI-capability
  numbering scheme (`AI-002`–`AI-008`) against the authoritative register in
  `06_TECHNICAL_REQUIREMENTS.md`; fixed reversed `SEC-001`/`SEC-002` mapping;
  fixed a `FR-003` triple-collision; renamed `audit_logs`→`audit_events` and
  `char_start`/`char_end`→`start_offset`/`end_offset` to match `09`/`10`/`11`.
- `09_DATABASE_DESIGN.md`, `11_SECURITY_ARCHITECTURE.md`, `12_UI_UX_DESIGN.md`:
  Corrected `FR-003` being used to mean the SIF Potential Engine; restored to
  `AI-004` per `06_TECHNICAL_REQUIREMENTS.md`.
- `08_AI_ARCHITECTURE.md`, `15_ROADMAP.md`: Standardized SIF Potential enum
  literal values to the canonical `YES` / `NO` / `REVIEW`.
- `10_API_SPECIFICATION.md`: Added the previously-missing
  `POST /api/v1/reports/batch` endpoint contract (request/response schema,
  validation rules).
- `06_TECHNICAL_REQUIREMENTS.md`: Registered two previously-unregistered
  requirements originating in `15_ROADMAP.md` (`FR-004` Audit Dossier Export,
  `FR-006` Notification Engine).

### Changed
- `16_DOCUMENT_CONSISTENCY_AUDIT.md`: Fully rewritten. The previous version
  contained a significant number of fabricated findings (invented quotes,
  non-existent table/column names); it has been replaced with a version in
  which every finding is tied to an exact, re-checkable file/line citation.

## [0.1.0] — Initial Documentation Set

### Added
- `01_PROJECT_CONSTITUTION.md` through `15_ROADMAP.md`, plus
  `ARCHITECTURE_DIAGRAMS_MERMAID.md` — full product and technical
  documentation set for the OIL Safety Intelligence Platform prototype,
  built for Smart India Hackathon 2026, problem statement SIH26165.
