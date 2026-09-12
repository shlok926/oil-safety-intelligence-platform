# Documentation Index

This folder contains the complete product and technical documentation for the
**OIL Safety Intelligence Platform** (SIH26165, Team Tech Smashers).

**Start here → [`01_PROJECT_CONSTITUTION.md`](01_PROJECT_CONSTITUTION.md)** — the governing source of truth for the entire project. Every other document must remain consistent with it.

| # | File | Purpose |
|---|---|---|
| 01 | `01_PROJECT_CONSTITUTION.md` | Governing principles, canonical taxonomies, claims/evidence policy |
| 02 | `02_PRODUCT_BLUEPRINT.md` | Product overview, personas, JTBD, modules, MVP |
| 03 | `03_PROBLEM_STATEMENT.md` | SIH26165 problem breakdown |
| 04 | `04_MARKET_RESEARCH.md` | Landscape & differentiation |
| 05 | `05_DATA_STRATEGY_AND_LABELING.md` | Data categories & labeling approach |
| 06 | `06_TECHNICAL_REQUIREMENTS.md` | **Authoritative requirement ID register** |
| 07 | `07_SYSTEM_ARCHITECTURE.md` | Component architecture |
| 08 | `08_AI_ARCHITECTURE.md` | NLP/ML pipeline design |
| 09 | `09_DATABASE_DESIGN.md` | Schema & enums |
| 10 | `10_API_SPECIFICATION.md` | REST contracts |
| 11 | `11_SECURITY_ARCHITECTURE.md` | RBAC, PII, audit trail |
| 12 | `12_UI_UX_DESIGN.md` | Screens & design tokens |
| 13 | `13_DEPLOYMENT.md` | Environments & CI/CD |
| 14 | `14_TESTING_STRATEGY.md` | Test strategy & AI evaluation |
| 15 | `15_ROADMAP.md` | Phased delivery plan |
| 16 | `16_DOCUMENT_CONSISTENCY_AUDIT.md` | Evidence-verified audit & fix log |
| — | `ARCHITECTURE_DIAGRAMS_MERMAID.md` | Consolidated diagrams |

## Before Editing Any Document

1. Check `06_TECHNICAL_REQUIREMENTS.md` before introducing or changing any requirement ID.
2. Grep the whole folder before renaming any enum, table, or field:
   ```bash
   grep -rn "YOUR_TERM" .
   ```
3. See [`../CONTRIBUTING.md`](../CONTRIBUTING.md) for the full documentation change process.
